import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))

    db.init_app(app)
    login_manager.init_app(app)

    from app.blueprints.auth import auth_bp
    from app.blueprints.dashboard import dashboard_bp
    from app.blueprints.estoque import estoque_bp
    from app.blueprints.atendimento import atendimento_bp
    from app.blueprints.insumos import insumos_bp
    from app.blueprints.financeiro import financeiro_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(estoque_bp, url_prefix='/estoque')
    app.register_blueprint(atendimento_bp, url_prefix='/atendimento')
    app.register_blueprint(insumos_bp, url_prefix='/insumos')
    app.register_blueprint(financeiro_bp, url_prefix='/financeiro')

    with app.app_context():
        os.makedirs(os.path.join(os.path.dirname(__file__), 'data'), exist_ok=True)
        os.makedirs(os.path.join(os.path.dirname(__file__), 'static', 'uploads'), exist_ok=True)
        from app.models.schemas import Studio, User, Produto, Atendimento, Insumo
        db.create_all()

    return app
