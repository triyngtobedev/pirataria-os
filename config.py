import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'pirataria-dev-key-change-in-production')
    _DB_URL = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(os.path.dirname(__file__), 'app', 'data', 'pirataria.db')
    )
    SQLALCHEMY_DATABASE_URI = _DB_URL.replace('postgres://', 'postgresql://', 1) if _DB_URL and _DB_URL.startswith('postgres://') else _DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

class ProductionConfig(Config):
    _DB_URL = os.environ.get('DATABASE_URL', 'postgresql://user:pass@localhost/piratariaos')
    SQLALCHEMY_DATABASE_URI = _DB_URL.replace('postgres://', 'postgresql://', 1) if _DB_URL and _DB_URL.startswith('postgres://') else _DB_URL

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
