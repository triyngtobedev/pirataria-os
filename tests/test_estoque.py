def test_listar_estoque(client, auth_client, produto):
    resp = client.get('/estoque/')
    assert resp.status_code == 200
    assert b'Argola' in resp.data


def test_adicionar_produto(client, auth_client, app):
    resp = client.post('/estoque/adicionar', data={
        'nome': 'Nova Joia',
        'tipo_joia': 'Barbell',
        'material': 'Aço',
        'quantidade': 5,
        'custo': 20,
        'valor_venda': 80,
    }, follow_redirects=True)
    assert resp.status_code == 200

    with app.app_context():
        from app.models.schemas import Produto
        p = Produto.query.filter_by(nome='Nova Joia').first()
        assert p is not None
        assert p.quantidade == 5


def test_adicionar_sem_nome(client, auth_client):
    resp = client.post('/estoque/adicionar', data={
        'nome': '',
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b'obrigat' in resp.data.lower()


def test_favoritar_produto(client, auth_client, app, produto):
    resp = client.get(f'/estoque/favoritar/{produto.id}', follow_redirects=True)
    assert resp.status_code == 200

    with app.app_context():
        from app import db
        from app.models.schemas import Produto
        p = db.session.get(Produto, produto.id)
        assert p.favorito is True


def test_excluir_produto(client, auth_client, app, produto):
    resp = client.get(f'/estoque/excluir/{produto.id}', follow_redirects=True)
    assert resp.status_code == 200

    with app.app_context():
        from app import db
        from app.models.schemas import Produto
        p = db.session.get(Produto, produto.id)
        assert p is not None
        assert p.is_active is False


def test_estoque_baixo_repos(app, db, studio_user):
    from app.repositories.produto_repo import ProdutoRepository
    s, u = studio_user
    with app.app_context():
        baixo = ProdutoRepository.estoque_baixo(s.id, limite=5)
        assert len(baixo) == 0
