import logging
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.middleware.tenant import inject_studio
from app.models.schemas import PushSubscription

logger = logging.getLogger(__name__)

notifications_bp = Blueprint('notifications', __name__, template_folder='../templates')


@notifications_bp.before_request
def before_request():
    inject_studio()


@notifications_bp.route('/notifications/subscribe', methods=['POST'])
@login_required
def subscribe():
    data = request.get_json(silent=True)
    if not data or not data.get('endpoint'):
        return jsonify({'error': 'endpoint required'}), 400

    existing = PushSubscription.query.filter_by(
        user_id=current_user.id,
        endpoint=data['endpoint'],
    ).first()
    if existing:
        return jsonify({'status': 'already subscribed'})

    sub = PushSubscription(
        studio_id=current_user.studio_id,
        user_id=current_user.id,
        endpoint=data['endpoint'],
        p256dh=data.get('keys', {}).get('p256dh', ''),
        auth=data.get('keys', {}).get('auth', ''),
    )
    db.session.add(sub)
    db.session.commit()
    logger.info('Push subscription saved for user %d', current_user.id)
    return jsonify({'status': 'subscribed'})


@notifications_bp.route('/notifications/vapid-public-key')
def vapid_public_key():
    key = current_app.config.get('VAPID_PUBLIC_KEY', '')
    return jsonify({'publicKey': key, 'claimEmail': current_app.config.get('VAPID_CLAIM_EMAIL', 'admin@piratariaos.com')})
