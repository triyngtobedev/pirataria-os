from app import db
from app.repositories.produto_repo import ProdutoRepository
from app.repositories.stock_movement_repo import StockMovementRepository


class StockService:

    @staticmethod
    def saida(studio_id, produto_id, quantidade, motivo='', created_by_id=None):
        produto = ProdutoRepository.get_by_id(produto_id)
        if not produto or produto.quantidade < quantidade:
            return False, 'Estoque insuficiente.'

        saldo_anterior = produto.quantidade
        produto.quantidade -= quantidade
        saldo_posterior = produto.quantidade

        StockMovementRepository.registrar(
            studio_id=studio_id,
            produto_id=produto_id,
            tipo='saida',
            quantidade=quantidade,
            saldo_anterior=saldo_anterior,
            saldo_posterior=saldo_posterior,
            motivo=motivo,
            created_by_id=created_by_id,
        )
        db.session.commit()
        return True, None

    @staticmethod
    def entrada(studio_id, produto_id, quantidade, motivo='', created_by_id=None):
        produto = ProdutoRepository.get_by_id(produto_id)
        if not produto:
            return False, 'Produto não encontrado.'

        saldo_anterior = produto.quantidade
        produto.quantidade += quantidade
        saldo_posterior = produto.quantidade

        StockMovementRepository.registrar(
            studio_id=studio_id,
            produto_id=produto_id,
            tipo='entrada',
            quantidade=quantidade,
            saldo_anterior=saldo_anterior,
            saldo_posterior=saldo_posterior,
            motivo=motivo,
            created_by_id=created_by_id,
        )
        db.session.commit()
        return True, None

    @staticmethod
    def ajuste(studio_id, produto_id, nova_quantidade, motivo='', created_by_id=None):
        produto = ProdutoRepository.get_by_id(produto_id)
        if not produto:
            return False, 'Produto não encontrado.'

        saldo_anterior = produto.quantidade
        diferenca = nova_quantidade - saldo_anterior
        produto.quantidade = nova_quantidade

        tipo = 'entrada' if diferenca > 0 else 'saida'

        StockMovementRepository.registrar(
            studio_id=studio_id,
            produto_id=produto_id,
            tipo=tipo,
            quantidade=abs(diferenca),
            saldo_anterior=saldo_anterior,
            saldo_posterior=nova_quantidade,
            motivo=motivo or 'Ajuste manual',
            created_by_id=created_by_id,
        )
        db.session.commit()
        return True, None

    @staticmethod
    def historico(studio_id, produto_id=None):
        return StockMovementRepository.historico(studio_id, produto_id=produto_id)
