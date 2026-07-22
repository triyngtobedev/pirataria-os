from app import db
from app.repositories.atendimento_repo import AtendimentoRepository
from app.repositories.produto_repo import ProdutoRepository
from app.repositories.stock_movement_repo import StockMovementRepository
from app.services.activity_service import ActivityService


class AtendimentoService:

    @staticmethod
    def listar(studio_id):
        return AtendimentoRepository.list_by_studio(studio_id)

    @staticmethod
    def listar_produtos(studio_id):
        return ProdutoRepository.list_by_studio(studio_id)

    @staticmethod
    def registrar(studio_id, dados, user_id=None):
        a = AtendimentoRepository.create(studio_id=studio_id, **dados)
        db.session.flush()

        joia = dados.get('joia_utilizada', '')
        if joia:
            produto = ProdutoRepository.find_by_name(studio_id, joia)
            if produto and produto.quantidade > 0:
                saldo_anterior = produto.quantidade
                produto.quantidade -= 1

                StockMovementRepository.registrar(
                    studio_id=studio_id,
                    produto_id=produto.id,
                    tipo='saida',
                    quantidade=1,
                    saldo_anterior=saldo_anterior,
                    saldo_posterior=produto.quantidade,
                    motivo=f'Atendimento: {dados.get("cliente", "")}',
                    created_by_id=user_id,
                )

        db.session.commit()

        ActivityService.log(
            studio_id=studio_id, user_id=user_id,
            acao='criar', entidade='atendimento', entidade_id=a.id,
            descricao=f'Atendimento de {dados.get("cliente", "")} - R$ {dados.get("valor", 0)}'
        )

        return a

    @staticmethod
    def excluir(atendimento_id, user_id=None):
        a = AtendimentoRepository.get_by_id(atendimento_id)
        if a:
            sid = a.studio_id
            cliente = a.cliente
            AtendimentoRepository.soft_delete(a)
            ActivityService.log(
                studio_id=sid, user_id=user_id,
                acao='excluir', entidade='atendimento', entidade_id=atendimento_id,
                descricao=f'Atendimento de {cliente} removido'
            )
