def test_produto_service_criar(app, db, studio_user):
    from app.services.produto_service import ProdutoService
    s, u = studio_user
    with app.app_context():
        p = ProdutoService.criar(
            studio_id=s.id,
            dados={
                'nome': 'Joia Service',
                'tipo_joia': 'Argola',
                'quantidade': 3,
                'custo': 25,
                'valor_venda': 90,
            },
            user_id=u.id,
        )
        assert p.nome == 'Joia Service'
        assert p.quantidade == 3

        from app.models.schemas import StockMovement
        mov = StockMovement.query.filter_by(produto_id=p.id).first()
        assert mov is not None
        assert mov.tipo == 'entrada'
        assert mov.quantidade == 3


def test_stock_service_saida(app, db, studio_user, produto):
    from app.services.stock_service import StockService
    s, u = studio_user
    with app.app_context():
        success, _ = StockService.saida(
            studio_id=s.id,
            produto_id=produto.id,
            quantidade=2,
            motivo='Teste',
            created_by_id=u.id,
        )
        assert success is True

        from app.models.schemas import Produto, StockMovement
        p = db.session.get(Produto, produto.id)
        assert p.quantidade == 8

        mov = StockMovement.query.filter_by(produto_id=produto.id).first()
        assert mov is not None
        assert mov.saldo_anterior == 10
        assert mov.saldo_posterior == 8


def test_stock_service_estoque_insuficiente(app, db, studio_user, produto):
    from app.services.stock_service import StockService
    s, u = studio_user
    with app.app_context():
        success, error = StockService.saida(
            studio_id=s.id,
            produto_id=produto.id,
            quantidade=999,
            created_by_id=u.id,
        )
        assert success is False


def test_atendimento_service_registrar(app, db, studio_user, produto):
    from app.services.atendimento_service import AtendimentoService
    s, u = studio_user
    with app.app_context():
        a = AtendimentoService.registrar(
            studio_id=s.id,
            dados={
                'cliente': 'Teste Service',
                'procedimento': 'Teste',
                'joia_utilizada': produto.nome,
                'valor': 100,
                'forma_pagamento': 'Pix',
                'piercer': 'Digão',
            },
            user_id=u.id,
        )
        assert a.cliente == 'Teste Service'

        from app.models.schemas import Produto
        p = db.session.get(Produto, produto.id)
        assert p.quantidade == 9


def test_user_roles(app, db, studio_user):
    s, u = studio_user
    assert u.role == 'admin'
    assert u.has_permission('atendimento') is True
    assert u.has_permission('financeiro') is True
    assert u.has_permission('usuarios') is True

    from app.models.schemas import Role
    assert Role.has_permission('piercer', 'atendimento') is True
    assert Role.has_permission('piercer', 'financeiro') is False
    assert Role.has_permission('reception', 'atendimento') is True
    assert Role.has_permission('reception', 'estoque') is False
    assert Role.has_permission('financial', 'financeiro') is True
    assert Role.has_permission('financial', 'estoque') is False
