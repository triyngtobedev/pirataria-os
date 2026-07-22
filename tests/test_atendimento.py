def test_listar_atendimentos(client, auth_client, atendimento):
    resp = client.get('/atendimento/')
    assert resp.status_code == 200
    assert b'Maria' in resp.data


def test_novo_atendimento(client, auth_client, app, produto):
    resp = client.post('/atendimento/novo', data={
        'cliente': 'João',
        'procedimento': 'Piercing Orelha',
        'joia_utilizada': produto.nome,
        'valor': 120,
        'forma_pagamento': 'Pix',
        'piercer': 'Digão',
    }, follow_redirects=True)
    assert resp.status_code == 200

    with app.app_context():
        from app import db
        from app.models.schemas import Atendimento, Produto
        a = Atendimento.query.filter_by(cliente='João').first()
        assert a is not None
        assert a.valor == 120

        p = db.session.get(Produto, produto.id)
        assert p.quantidade == 9  # was 10, decremented by 1


def test_novo_atendimento_sem_cliente(client, auth_client):
    resp = client.post('/atendimento/novo', data={
        'cliente': '',
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b'obrigat' in resp.data.lower()


def test_excluir_atendimento(client, auth_client, app, atendimento):
    resp = client.get(f'/atendimento/excluir/{atendimento.id}', follow_redirects=True)
    assert resp.status_code == 200

    with app.app_context():
        from app import db
        from app.models.schemas import Atendimento
        a = db.session.get(Atendimento, atendimento.id)
        assert a is not None
        assert a.is_active is False


def test_soft_delete_atendimento_repo(app, atendimento):
    from app.services.atendimento_service import AtendimentoService
    with app.app_context():
        AtendimentoService.excluir(atendimento.id)
        from app import db
        from app.models.schemas import Atendimento
        a = db.session.get(Atendimento, atendimento.id)
        assert a is not None
        assert a.is_active is False
        assert a.deleted_at is not None
