from app import db
from app.repositories.insumo_repo import InsumoRepository
from app.services.activity_service import ActivityService


class InsumoService:

    @staticmethod
    def listar(studio_id):
        return InsumoRepository.list_by_studio(studio_id)

    @staticmethod
    def criar(studio_id, dados, user_id=None):
        i = InsumoRepository.create(studio_id=studio_id, **dados)
        db.session.commit()
        ActivityService.log(
            studio_id=studio_id, user_id=user_id,
            acao='criar', entidade='insumo', entidade_id=i.id,
            descricao=f'Insumo "{dados.get("nome", "")}" criado'
        )
        return i

    @staticmethod
    def atualizar(insumo_id, dados, user_id=None):
        i = InsumoRepository.get_by_id(insumo_id)
        if not i or not i.is_active:
            return None
        for key, value in dados.items():
            if hasattr(i, key):
                setattr(i, key, value)
        db.session.commit()
        ActivityService.log(
            studio_id=i.studio_id, user_id=user_id,
            acao='atualizar', entidade='insumo', entidade_id=insumo_id,
            descricao=f'Insumo "{i.nome}" atualizado'
        )
        return i

    @staticmethod
    def excluir(insumo_id, user_id=None):
        i = InsumoRepository.get_by_id(insumo_id)
        if i:
            sid = i.studio_id
            nome = i.nome
            InsumoRepository.soft_delete(i)
            ActivityService.log(
                studio_id=sid, user_id=user_id,
                acao='excluir', entidade='insumo', entidade_id=insumo_id,
                descricao=f'Insumo "{nome}" removido'
            )
