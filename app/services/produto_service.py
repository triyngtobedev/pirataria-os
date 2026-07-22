from app import db
from app.repositories.produto_repo import ProdutoRepository
from app.repositories.stock_movement_repo import StockMovementRepository
from app.services.activity_service import ActivityService


class ProdutoService:

    @staticmethod
    def listar(studio_id, favoritos_only=False):
        if favoritos_only:
            return ProdutoRepository.favoritos(studio_id)
        return ProdutoRepository.list_by_studio(
            studio_id,
            order_by=ProdutoRepository.model.favorito.desc()
        )

    @staticmethod
    def criar(studio_id, dados, foto='', user_id=None):
        p = ProdutoRepository.create(studio_id=studio_id, **dados)
        p.foto = foto
        db.session.commit()

        if p.quantidade > 0:
            StockMovementRepository.registrar(
                studio_id=studio_id,
                produto_id=p.id,
                tipo='entrada',
                quantidade=p.quantidade,
                saldo_anterior=0,
                saldo_posterior=p.quantidade,
                motivo='Cadastro inicial',
                created_by_id=user_id,
            )
            db.session.commit()

        ActivityService.log(
            studio_id=studio_id, user_id=user_id,
            acao='criar', entidade='produto', entidade_id=p.id,
            descricao=f'Produto "{p.nome}" criado'
        )
        return p

    @staticmethod
    def atualizar(produto_id, dados, foto='', user_id=None):
        p = ProdutoRepository.get_by_id(produto_id)
        if not p or not p.is_active:
            return None

        for key, value in dados.items():
            if hasattr(p, key):
                setattr(p, key, value)
        if foto:
            p.foto = foto
        db.session.commit()

        ActivityService.log(
            studio_id=p.studio_id, user_id=user_id,
            acao='atualizar', entidade='produto', entidade_id=p.id,
            descricao=f'Produto "{p.nome}" atualizado'
        )
        return p

    @staticmethod
    def favoritar(produto_id):
        p = ProdutoRepository.get_by_id(produto_id)
        if p:
            p.favorito = not p.favorito
            db.session.commit()
        return p

    @staticmethod
    def excluir(produto_id, user_id=None):
        p = ProdutoRepository.get_by_id(produto_id)
        if p:
            nome = p.nome
            sid = p.studio_id
            ProdutoRepository.soft_delete(p)
            ActivityService.log(
                studio_id=sid, user_id=user_id,
                acao='excluir', entidade='produto', entidade_id=produto_id,
                descricao=f'Produto "{nome}" removido'
            )

    @staticmethod
    def get_by_id(produto_id):
        return ProdutoRepository.get_by_id(produto_id)

    @staticmethod
    def estoque_baixo(studio_id, limite=3):
        return ProdutoRepository.estoque_baixo(studio_id, limite=limite)

    @staticmethod
    def total_ativo(studio_id):
        return ProdutoRepository.total_ativo(studio_id)
