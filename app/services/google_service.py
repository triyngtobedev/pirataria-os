import logging
from datetime import datetime, timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_calendar_service(integration, client_id, client_secret):
    creds = Credentials(
        token=integration.access_token,
        refresh_token=integration.refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES,
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        integration.access_token = creds.token
        integration.token_expiry = creds.expiry
    from app import db
    db.session.commit()
    return build('calendar', 'v3', credentials=creds)


def criar_evento(integration, client_id, client_secret, cliente, procedimento='', joia='',
                 valor=0, pagamento='', piercer='', data_hora=None):
    service = get_calendar_service(integration, client_id, client_secret)
    calendar_id = integration.calendar_id or 'primary'

    if data_hora and isinstance(data_hora, datetime):
        start = data_hora
        end = start.replace(hour=start.hour + 1)
    else:
        agora = datetime.now(timezone.utc)
        start = agora
        end = agora.replace(hour=agora.hour + 1)

    descricao = ''
    if procedimento:
        descricao += f'Procedimento: {procedimento}\n'
    if joia:
        descricao += f'Joia: {joia}\n'
    if piercer:
        descricao += f'Piercer: {piercer}\n'
    if valor:
        descricao += f'Valor: R$ {valor:.2f}\n'
    if pagamento:
        descricao += f'Pagamento: {pagamento}'

    event = {
        'summary': cliente,
        'description': descricao.strip(),
        'start': {'dateTime': start.isoformat(), 'timeZone': 'America/Sao_Paulo'},
        'end': {'dateTime': end.isoformat(), 'timeZone': 'America/Sao_Paulo'},
    }

    created = service.events().insert(calendarId=calendar_id, body=event).execute()
    return created.get('id')


def atualizar_evento(integration, client_id, client_secret, event_id, cliente=None,
                     procedimento=None, joia=None, valor=None, pagamento=None, piercer=None):
    service = get_calendar_service(integration, client_id, client_secret)
    calendar_id = integration.calendar_id or 'primary'

    event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()

    if cliente is not None:
        event['summary'] = cliente

    partes = []
    if procedimento is not None:
        partes.append(f'Procedimento: {procedimento}')
    if joia is not None:
        partes.append(f'Joia: {joia}')
    if piercer is not None:
        partes.append(f'Piercer: {piercer}')
    if valor is not None:
        partes.append(f'Valor: R$ {valor:.2f}')
    if pagamento is not None:
        partes.append(f'Pagamento: {pagamento}')
    event['description'] = '\n'.join(partes)

    updated = service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()
    return updated.get('id')


def excluir_evento(integration, client_id, client_secret, event_id):
    service = get_calendar_service(integration, client_id, client_secret)
    calendar_id = integration.calendar_id or 'primary'
    try:
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
    except Exception as e:
        logger.warning('Erro ao excluir evento %s: %s', event_id, e)


def listar_mudancas(integration, client_id, client_secret, since):
    service = get_calendar_service(integration, client_id, client_secret)
    calendar_id = integration.calendar_id or 'primary'
    params = {
        'calendarId': calendar_id,
        'orderBy': 'updated',
        'singleEvents': True,
    }
    if since:
        params['updatedMin'] = since.isoformat()
    events_result = service.events().list(**params).execute()
    return events_result.get('items', [])
