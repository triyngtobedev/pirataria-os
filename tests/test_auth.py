def test_login_page(client):
    resp = client.get('/auth/login')
    assert resp.status_code == 200
    assert b'Email' in resp.data


def test_register(client, app):
    resp = client.post('/auth/register', data={
        'studio_nome': 'Novo Studio',
        'nome': 'Lucas',
        'email': 'lucas@test.com',
        'password': '123456',
    }, follow_redirects=True)
    assert resp.status_code == 200

    with app.app_context():
        from app.models.schemas import User
        user = User.query.filter_by(email='lucas@test.com').first()
        assert user is not None
        assert user.role == 'admin'
        assert user.is_active is True


def test_register_duplicate_email(client, app):
    client.post('/auth/register', data={
        'studio_nome': 'Studio 1',
        'nome': 'User 1',
        'email': 'dup@test.com',
        'password': '123456',
    })
    resp = client.post('/auth/register', data={
        'studio_nome': 'Studio 2',
        'nome': 'User 2',
        'email': 'dup@test.com',
        'password': '123456',
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b'cadastrado' in resp.data.lower() or b'Email' in resp.data


def test_login_success(client, studio_user):
    s, u = studio_user
    resp = client.post('/auth/login', data={
        'email': u.email,
        'password': '123456',
    }, follow_redirects=True)
    assert resp.status_code == 200


def test_login_wrong_password(client, studio_user):
    s, u = studio_user
    resp = client.post('/auth/login', data={
        'email': u.email,
        'password': 'wrong',
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b'inv' in resp.data.lower() or b'senha' in resp.data.lower()


def test_logout(client, auth_client):
    resp = client.get('/auth/logout', follow_redirects=True)
    assert resp.status_code == 200
