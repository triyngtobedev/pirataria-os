from app import db
from app.models.schemas import Produto
from .base import BaseRepository


class ProdutoRepository(BaseRepository):
    model = Produto

    @classmethod
    def find_by_name(cls, studio_id, nome):
        return Produto.query.filter(
            Produto.studio_id == studio_id,
            Produto.is_active == True,
            Produto.nome.ilike(f'%{nome}%')
        ).first()

    @classmethod
    def favoritos(cls, studio_id):
        return Produto.query.filter_by(
            studio_id=studio_id,
            is_active=True,
            favorito=True
        ).order_by(Produto.created_at.desc()).all()

    @classmethod
    def estoque_baixo(cls, studio_id, limite=3):
        return Produto.query.filter(
            Produto.studio_id == studio_id,
            Produto.is_active == True,
            Produto.quantidade <= limite
        ).order_by(Produto.quantidade).all()

    @classmethod
    def total_ativo(cls, studio_id):
        return Produto.query.filter_by(
            studio_id=studio_id,
            is_active=True
        ).count()

    @classmethod
    def ajustar_estoque(cls, produto_id, nova_quantidade):
        produto = cls.get_by_id(produto_id)
        if produto:
            produto.quantidade = nova_quantidade
            db.session.commit()
        return produto
