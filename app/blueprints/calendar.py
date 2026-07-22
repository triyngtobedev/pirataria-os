import logging
from datetime import datetime, timedelta, timezone

from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, session
from flask_login import login_required, current_user
from google_auth_oauthlib.flow import Flow

from app import db
from app.middleware.tenant import inject_studio
from app.models.schemas import CalendarIntegration, Atendimento
from app.services import google_service

logger = logging.getLogger(__name__)

BRT = timezone(timedelta(hours=-3))

calendar_bp = Blueprint('calendar', __name__, template_folder='../templates')


@calendar_bp.before_request
def before_request():
    inject_studio()


def _get_flow():
    return Flow.from_client_config(
        {
            'web': {
                'client_id': current_app.config['GOOGLE_CLIENT_ID'],
                'client_secret': current_app.config['GOOGLE_CLIENT_SECRET'],
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://oauth2.googleapis.com/token',
                'redirect_uris': [current_app.config['GOOGLE_REDIRECT_URI']],
            }
        },
        scopes=google_service.SCOPES,
        redirect_uri=current_app.config['GOOGLE_REDIRECT_URI'],
    )


@calendar_bp.route('/agenda')
@login_required
def agenda():
    agora = datetime.now(BRT)
    hoje = agora.date()

    todos = Atendimento.query.filter(
        Atendimento.studio_id == current_user.studio_id,
        Atendimento.is_active == True,
    ).all()

    com_data = [a for a in todos if a.scheduled_at]
    sem_data = [a for a in todos if not a.scheduled_at]

    proximos = [a for a in com_data if a.scheduled_at.date() >= hoje]
    proximos.sort(key=lambda a: a.scheduled_at)

    passados = [a for a in com_data if a.scheduled_at.date() < hoje]
    passados.sort(key=lambda a: a.scheduled_at, reverse=True)
    sem_data.sort(key=lambda a: a.created_at, reverse=True)
    passados = sem_data + passados
    passados = passados[:50]

    integration = CalendarIntegration.query.filter_by(studio_id=current_user.studio_id).first()
    return render_template(
        'agenda.html',
        proximos=proximos,
        passados=passados,
        integration=integration,
    )


@calendar_bp.route('/calendar/settings')
@login_required
def settings():
    integration = CalendarIntegration.query.filter_by(studio_id=current_user.studio_id).first()
    return render_template('calendar_settings.html', integration=integration)


@calendar_bp.route('/calendar/connect')
@login_required
def connect():
    if not current_app.config['GOOGLE_CLIENT_ID'] or not current_app.config['GOOGLE_CLIENT_SECRET']:
        flash('Google Calendar não configurado. Configure GOOGLE_CLIENT_ID e GOOGLE_CLIENT_SECRET.', 'danger')
        return redirect(url_for('calendar.settings'))

    integration = CalendarIntegration.query.filter_by(studio_id=current_user.studio_id).first()
    if integration:
        db.session.delete(integration)
        db.session.commit()

    flow = _get_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent',
    )
    session['google_oauth_state'] = state
    return redirect(authorization_url)


@calendar_bp.route('/calendar/callback')
@login_required
def callback():
    flow = _get_flow()
    state = session.pop('google_oauth_state', None)
    auth_url = request.url.replace('http://', 'https://')
    flow.fetch_token(
        authorization_response=auth_url,
        state=state,
    )

    credentials = flow.credentials

    integration = CalendarIntegration.query.filter_by(studio_id=current_user.studio_id).first()
    if not integration:
        integration = CalendarIntegration(studio_id=current_user.studio_id)
        db.session.add(integration)

    integration.access_token = credentials.token
    integration.refresh_token = credentials.refresh_token
    integration.token_expiry = credentials.expiry

    try:
        service = google_service.get_calendar_service(
            integration,
            current_app.config['GOOGLE_CLIENT_ID'],
            current_app.config['GOOGLE_CLIENT_SECRET'],
        )
        about = service.calendars().get(calendarId='primary').execute()
        if not integration.calendar_id:
            integration.calendar_id = about.get('id')
        integration.google_email = about.get('summary')
    except Exception as e:
        logger.warning('Erro ao obter info do calendario: %s', e)

    db.session.commit()
    flash('Google Agenda conectada com sucesso!', 'success')
    return redirect(url_for('calendar.settings'))


@calendar_bp.route('/calendar/calendars')
@login_required
def listar_calendarios():
    integration = CalendarIntegration.query.filter_by(studio_id=current_user.studio_id).first()
    if not integration:
        flash('Conecte o Google Agenda primeiro.', 'danger')
        return redirect(url_for('calendar.settings'))
    try:
        calendarios = google_service.listar_calendarios(
            integration,
            current_app.config['GOOGLE_CLIENT_ID'],
            current_app.config['GOOGLE_CLIENT_SECRET'],
        )
    except Exception as e:
        logger.error('Erro ao listar calendarios: %s', e)
        flash('Erro ao listar calendarios. Reconecte sua conta.', 'danger')
        return redirect(url_for('calendar.settings'))
    return render_template('calendar_pick.html', calendarios=calendarios, integration=integration)


@calendar_bp.route('/calendar/select/<path:calendar_id>')
@login_required
def select_calendar(calendar_id):
    integration = CalendarIntegration.query.filter_by(studio_id=current_user.studio_id).first()
    if not integration:
        flash('Conecte o Google Agenda primeiro.', 'danger')
        return redirect(url_for('calendar.settings'))
    integration.calendar_id = calendar_id
    integration.last_sync_at = None
    deletados = Atendimento.query.filter(
        Atendimento.studio_id == current_user.studio_id,
        Atendimento.google_event_id.isnot(None),
    ).delete(synchronize_session=False)
    db.session.commit()
    flash(f'Calendário trocado! {deletados} eventos antigos removidos.', 'warning')
    return redirect(url_for('calendar.settings'))


@calendar_bp.route('/calendar/tasklists')
@login_required
def listar_tasklists():
    integration = CalendarIntegration.query.filter_by(studio_id=current_user.studio_id).first()
    if not integration:
        flash('Conecte o Google Agenda primeiro.', 'danger')
        return redirect(url_for('calendar.settings'))
    try:
        tasklists = google_service.listar_tasklists(
            integration,
            current_app.config['GOOGLE_CLIENT_ID'],
            current_app.config['GOOGLE_CLIENT_SECRET'],
        )
    except Exception as e:
        logger.error('Erro ao listar listas de tarefas: %s', e)
        flash('Erro ao listar tarefas. Reconecte sua conta Google.', 'danger')
        return redirect(url_for('calendar.settings'))
    return render_template('calendar_tasklists.html', tasklists=tasklists, integration=integration)


@calendar_bp.route('/calendar/select_tasks/<path:list_id>')
@login_required
def select_tasklist(list_id):
    integration = CalendarIntegration.query.filter_by(studio_id=current_user.studio_id).first()
    if not integration:
        flash('Conecte o Google Agenda primeiro.', 'danger')
        return redirect(url_for('calendar.settings'))
    integration.tasks_list_id = list_id
    db.session.commit()
    flash('Lista de tarefas selecionada!', 'success')
    return redirect(url_for('calendar.settings'))


@calendar_bp.route('/calendar/clear')
@login_required
def clear_synced():
    integration = CalendarIntegration.query.filter_by(studio_id=current_user.studio_id).first()
    if not integration:
        flash('Nenhuma integracao encontrada.', 'danger')
        return redirect(url_for('calendar.settings'))
    deletados = Atendimento.query.filter(
        Atendimento.studio_id == current_user.studio_id,
        Atendimento.google_event_id.isnot(None),
    ).delete(synchronize_session=False)
    integration.last_sync_at = None
    db.session.commit()
    flash(f'{deletados} eventos sincronizados removidos.', 'warning')
    return redirect(url_for('calendar.settings'))


@calendar_bp.route('/calendar/disconnect')
@login_required
def disconnect():
    integration = CalendarIntegration.query.filter_by(studio_id=current_user.studio_id).first()
    if integration:
        db.session.delete(integration)
        db.session.commit()
        flash('Google Agenda desconectada.', 'warning')
    return redirect(url_for('calendar.settings'))


@calendar_bp.route('/calendar/sync')
@login_required
def sync_now():
    integration = CalendarIntegration.query.filter_by(studio_id=current_user.studio_id).first()
    if not integration:
        flash('Nenhuma integracao com Google Agenda encontrada.', 'danger')
        return redirect(url_for('calendar.settings'))

    from app.services.sync_service import sync_from_google
    criados, atualizados = sync_from_google(current_user.studio_id)
    flash(f'Sincronizado! {criados} criados, {atualizados} atualizados.', 'info')
    return redirect(url_for('calendar.settings'))
