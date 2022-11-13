from pathlib import Path
from app.utils import config

class Config(object):
    """
    General Configs
    """
    SALT = "abcde"

    # SQLALCHEMY DATABASE config
    SQLALCHEMY_DATABASE_URI = config.get_yaml('db.MYSQL', '')
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # JWT config
    JWT_SALT = config.get_yaml('jwt.SALT', 'newborn')
    JWT_EXPIRY = config.get_yaml('jwt.EXPIRY', 24)


class DevelopmentConfig(Config):
    """
    Development Mode
    """
    TYPE = 'dev'
    DEBUG = True


class ProductionConfig(Config):
    """
    Production Mode
    """
    TYPE = 'prod'
    DEBUG = False
    ENV = 'production'


class TestConfig(Config):
    """
    Test mode
    """
    TYPE = 'test'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"


configs = {
    "default": DevelopmentConfig,
    "dev": DevelopmentConfig,
    "prod": ProductionConfig,
    "test": TestConfig
}
