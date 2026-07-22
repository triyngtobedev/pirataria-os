from app import db
from app.models.schemas import ActivityLog
from .base import BaseRepository


class ActivityLogRepository(BaseRepository):
    model = ActivityLog

    @classmethod
    def log(cls, studio_id, user_id, acao, entidade, entidade_id=None,
            descricao='', detalhes=''):
        entry = ActivityLog(
            studio_id=studio_id,
            user_id=user_id,
            acao=acao,
            entidade=entidade,
            entidade_id=entidade_id,
            descricao=descricao,
            detalhes=detalhes,
        )
        db.session.add(entry)
        return entry

    @classmethod
    def listar(cls, studio_id, limit=100):
        return ActivityLog.query.filter_by(studio_id=studio_id)\
            .order_by(ActivityLog.created_at.desc()).limit(limit).all()
