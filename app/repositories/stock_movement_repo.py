from app import db
from app.models.schemas import StockMovement
from .base import BaseRepository


class StockMovementRepository(BaseRepository):
    model = StockMovement

    @classmethod
    def registrar(cls, studio_id, produto_id, tipo, quantidade,
                  saldo_anterior, saldo_posterior, motivo='', created_by_id=None):
        mov = StockMovement(
            studio_id=studio_id,
            produto_id=produto_id,
            tipo=tipo,
            quantidade=quantidade,
            saldo_anterior=saldo_anterior,
            saldo_posterior=saldo_posterior,
            motivo=motivo,
            created_by_id=created_by_id,
        )
        db.session.add(mov)
        return mov

    @classmethod
    def historico(cls, studio_id, produto_id=None, limit=100):
        q = StockMovement.query.filter_by(studio_id=studio_id)
        if produto_id:
            q = q.filter_by(produto_id=produto_id)
        return q.order_by(StockMovement.created_at.desc()).limit(limit).all()
