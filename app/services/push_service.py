import json
import logging

from flask import current_app
from pywebpush import webpush, WebPushException

from app import db
from app.models.schemas import PushSubscription

logger = logging.getLogger(__name__)


def send_push(studio_id, titulo, mensagem, link=''):
    subs = PushSubscription.query.filter_by(studio_id=studio_id).all()
    if not subs:
        return

    vapid_private = current_app.config.get('VAPID_PRIVATE_KEY')
    vapid_public = current_app.config.get('VAPID_PUBLIC_KEY')
    if not vapid_private or not vapid_public:
        logger.warning('VAPID keys not configured, skipping push')
        return

    payload = json.dumps({
        'title': titulo,
        'body': mensagem,
        'icon': '/static/icons/icon-192.svg',
        'badge': '/static/icons/icon-192.svg',
        'data': {'url': link or '/'},
    })

    claim_email = current_app.config.get('VAPID_CLAIM_EMAIL', 'admin@piratariaos.com')
    falhas = []
    for sub in subs:
        try:
            webpush(
                subscription_info={
                    'endpoint': sub.endpoint,
                    'keys': {
                        'p256dh': sub.p256dh,
                        'auth': sub.auth,
                    },
                },
                data=payload,
                vapid_private_key=vapid_private,
                vapid_claims={'sub': f'mailto:{claim_email}'},
            )
        except WebPushException as e:
            if e.response and e.response.status_code == 410:
                falhas.append(sub)
            logger.warning('Push falhou para sub %d: %s', sub.id, e)

    for sub in falhas:
        db.session.delete(sub)
    if falhas:
        db.session.commit()
