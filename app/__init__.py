import os
import logging
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from apscheduler.schedulers.background import BackgroundScheduler
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
migrate = Migrate()
csrf = CSRFProtect()
scheduler = BackgroundScheduler(daemon=True)


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))

    if config_name == 'production':
        if app.config['SECRET_KEY'] == 'pirataria-dev-key-change-in-production':
            raise RuntimeError('SECRET_KEY must be set in production')

    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app.blueprints.auth import auth_bp
    from app.blueprints.dashboard import dashboard_bp
    from app.blueprints.estoque import estoque_bp
    from app.blueprints.atendimento import atendimento_bp
    from app.blueprints.insumos import insumos_bp
    from app.blueprints.financeiro import financeiro_bp
    from app.blueprints.calendar import calendar_bp
    from app.blueprints.notifications import notifications_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(estoque_bp, url_prefix='/estoque')
    app.register_blueprint(atendimento_bp, url_prefix='/atendimento')
    app.register_blueprint(insumos_bp, url_prefix='/insumos')
    app.register_blueprint(financeiro_bp, url_prefix='/financeiro')
    app.register_blueprint(calendar_bp)
    app.register_blueprint(notifications_bp)

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.exception('Internal Server Error: %s', error)
        return render_template('errors/500.html'), 500

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    with app.app_context():
        os.makedirs(os.path.join(os.path.dirname(__file__), 'data'), exist_ok=True)
        os.makedirs(os.path.join(os.path.dirname(__file__), 'static', 'uploads'), exist_ok=True)

    if not scheduler.running and not app.config.get('TESTING'):
        from app.services.sync_service import sync_all_studios

        with app.app_context():
            from app.models.schemas import CalendarIntegration
            integracoes = CalendarIntegration.query.all()
            for integ in integracoes:
                integ.last_sync_at = None
            if integracoes:
                db.session.commit()
                app.logger.info('Reset last_sync_at for %d integrations (full re-sync)', len(integracoes))

        scheduler.add_job(
            sync_all_studios,
            'interval',
            minutes=5,
            id='google_sync',
            replace_existing=True,
            next_run_time=None,
        )
        scheduler.start()
        app.logger.info('APScheduler started: sync every 5 minutes')

    return app