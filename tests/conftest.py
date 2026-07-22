import os
import tempfile
import pytest


@pytest.fixture(scope='function')
def app():
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.environ['FLASK_ENV'] = 'development'
    os.environ['WTF_CSRF_ENABLED'] = 'False'
    os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'

    from app import create_app, db as _db
    app = create_app('development')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SERVER_NAME'] = 'localhost'

    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.engine.dispose()

    os.close(db_fd)
    try:
        os.unlink(db_path)
    except PermissionError:
        pass


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def db(app):
    from app import db as _db
    return _db


@pytest.fixture(scope='function')
def studio(app, db):
    from app.models.schemas import Studio

    s = Studio(nome='Test Studio', subdomain='test')
    db.session.add(s)
    db.session.commit()
    return s


@pytest.fixture(scope='function')
def studio_user(app, db, studio):
    from app.models.schemas import User

    u = User(
        studio_id=studio.id,
        nome='Admin',
        email='admin@teststudio.com',
        role='admin',
        is_active=True,
    )
    u.set_password('123456')
    db.session.add(u)
    db.session.flush()
    u.created_by_id = u.id
    db.session.commit()

    yield studio, u


@pytest.fixture(scope='function')
def auth_client(app, client, studio_user):
    s, u = studio_user
    client.post('/auth/login', data={
        'email': u.email,
        'password': '123456',
    })
    return client


@pytest.fixture(scope='function')
def produto(app, db, studio_user):
    from app.models.schemas import Produto

    s, u = studio_user

    p = Produto(
        studio_id=s.id,
        nome='Argola Teste 8mm',
        tipo_joia='Argola',
        material='Titânio',
        quantidade=10,
        custo=30.0,
        valor_venda=100.0,
    )
    db.session.add(p)
    db.session.commit()

    yield p


@pytest.fixture(scope='function')
def atendimento(app, db, studio_user):
    from app.models.schemas import Atendimento

    s, u = studio_user

    from datetime import datetime
    a = Atendimento(
        studio_id=s.id,
        cliente='Maria',
        procedimento='Piercing Nariz',
        valor=150.0,
        forma_pagamento='Pix',
        piercer='Digão',
        created_by_id=u.id,
        created_at=datetime.now(),
    )
    db.session.add(a)
    db.session.commit()

    yield a


@pytest.fixture(scope='function')
def insumo(app, db, studio_user):
    from app.models.schemas import Insumo

    s, u = studio_user

    i = Insumo(
        studio_id=s.id,
        nome='Luva M',
        categoria='EPI',
        quantidade=100,
        unidade='unidade',
        custo_unitario=0.50,
    )
    db.session.add(i)
    db.session.commit()

    yield i
