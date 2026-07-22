from datetime import datetime, timezone
from app import db
from app.models.schemas import Notification
from app.services.push_service import send_push


class NotificationService:

    @staticmethod
    def criar(studio_id, tipo, titulo, mensagem='', link=''):
        n = Notification(
            studio_id=studio_id,
            tipo=tipo,
            titulo=titulo,
            mensagem=mensagem,
            link=link,
        )
        db.session.add(n)
        db.session.commit()
        try:
            send_push(studio_id, titulo, mensagem, link)
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning('Erro ao enviar push: %s', e)
        return n

    @staticmethod
    def listar_nao_lidas(studio_id, limite=10):
        return Notification.query.filter_by(
            studio_id=studio_id, lida=False
        ).order_by(Notification.created_at.desc()).limit(limite).all()

    @staticmethod
    def listar_recentes(studio_id, limite=10):
        return Notification.query.filter_by(
            studio_id=studio_id
        ).order_by(Notification.created_at.desc()).limit(limite).all()

    @staticmethod
    def marcar_lida(notification_id):
        n = db.session.get(Notification, notification_id)
        if n:
            n.lida = True
            db.session.commit()

    @staticmethod
    def contar_nao_lidas(studio_id):
        return Notification.query.filter_by(
            studio_id=studio_id, lida=False
        ).count()
