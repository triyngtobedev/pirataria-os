import os
from pathlib import Path


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'pirataria-dev-key-change-in-production')
    _DB_URL = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + str(Path(__file__).parent / 'app' / 'data' / 'pirataria.db')
    )
    SQLALCHEMY_DATABASE_URI = _DB_URL.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '')
    GOOGLE_REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI', 'http://localhost:5000/calendar/callback')


class ProductionConfig(Config):
    _DB_URL = os.environ.get('DATABASE_URL', 'postgresql://user:pass@localhost/piratariaos')
    SQLALCHEMY_DATABASE_URI = _DB_URL.replace('postgres://', 'postgresql://', 1)


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
