from app.repositories.activity_log_repo import ActivityLogRepository


class ActivityService:

    @staticmethod
    def log(studio_id, user_id, acao, entidade, entidade_id=None,
            descricao='', detalhes=''):
        return ActivityLogRepository.log(
            studio_id=studio_id,
            user_id=user_id,
            acao=acao,
            entidade=entidade,
            entidade_id=entidade_id,
            descricao=descricao,
            detalhes=detalhes,
        )

    @staticmethod
    def listar(studio_id, limit=100):
        return ActivityLogRepository.listar(studio_id, limit=limit)
