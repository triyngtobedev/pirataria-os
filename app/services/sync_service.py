import logging
from datetime import datetime, timezone

from flask import current_app

from app import db
from app.models.schemas import CalendarIntegration, Atendimento
from app.services import google_service

logger = logging.getLogger(__name__)


def sync_from_google(studio_id):
    integration = CalendarIntegration.query.filter_by(studio_id=studio_id).first()
    if not integration:
        return 0, 0

    client_id = current_app.config['GOOGLE_CLIENT_ID']
    client_secret = current_app.config['GOOGLE_CLIENT_SECRET']
    if not client_id or not client_secret:
        return 0, 0

    since = integration.last_sync_at or datetime.now(timezone.utc).replace(year=2020)
    events = google_service.listar_mudancas(integration, client_id, client_secret, since)
    criados = 0
    atualizados = 0

    for event in events:
        event_id = event.get('id')
        summary = event.get('summary', '')
        description = event.get('description', '')
        start = event.get('start', {})
        start_dt = start.get('dateTime') or start.get('date')

        if not summary and not description:
            continue

        existing = Atendimento.query.filter_by(
            studio_id=studio_id,
            google_event_id=event_id,
        ).first()

        dados = _extrair_dados(summary, description)
        event_updated = event.get('updated', '')
        if event_updated:
            try:
                if isinstance(event_updated, str):
                    event_updated = datetime.fromisoformat(event_updated.replace('Z', '+00:00'))
            except (ValueError, TypeError):
                event_updated = None

        if existing:
            if event_updated and existing.updated_at and event_updated > existing.updated_at.replace(tzinfo=timezone.utc):
                existing.cliente = dados.get('cliente', existing.cliente)
                existing.procedimento = dados.get('procedimento', existing.procedimento)
                existing.joia_utilizada = dados.get('joia', existing.joia_utilizada)
                existing.valor = dados.get('valor', existing.valor)
                existing.forma_pagamento = dados.get('pagamento', existing.forma_pagamento)
                existing.piercer = dados.get('piercer', existing.piercer)
                atualizados += 1
        else:
            scheduled = datetime.fromisoformat(start_dt.replace('Z', '+00:00')) if start_dt else None
            a = Atendimento(
                studio_id=studio_id,
                google_event_id=event_id,
                cliente=dados.get('cliente', summary or 'Sincronizado'),
                procedimento=dados.get('procedimento', ''),
                joia_utilizada=dados.get('joia', ''),
                valor=dados.get('valor', 0),
                forma_pagamento=dados.get('pagamento', ''),
                piercer=dados.get('piercer', ''),
                status='Pago',
                scheduled_at=scheduled,
                created_at=datetime.now(timezone.utc),
            )
            db.session.add(a)
            criados += 1

    integration.last_sync_at = datetime.now(timezone.utc)
    db.session.commit()
    return criados, atualizados


def _extrair_dados(summary, description):
    dados = {'cliente': summary}
    if not description:
        return dados

    mapa = {
        'Procedimento: ': 'procedimento',
        'Joia: ': 'joia',
        'Piercer: ': 'piercer',
        'Valor: R$ ': 'valor',
        'Pagamento: ': 'pagamento',
    }

    for linha in description.split('\n'):
        for prefix, campo in mapa.items():
            if linha.startswith(prefix):
                valor = linha[len(prefix):].strip()
                if campo == 'valor':
                    try:
                        valor = float(valor.replace('.', '').replace(',', '.'))
                    except (ValueError, AttributeError):
                        valor = 0
                dados[campo] = valor
                break

    return dados


def sync_all_studios():
    from app import create_app
    app = create_app()
    with app.app_context():
        integracoes = CalendarIntegration.query.all()
        for integracao in integracoes:
            try:
                criados, atualizados = sync_from_google(integracao.studio_id)
                if criados or atualizados:
                    logger.info('Sync studio %s: %d criados, %d atualizados', integracao.studio_id, criados, atualizados)
            except Exception as e:
                logger.error('Erro sync studio %s: %s', integracao.studio_id, e)
