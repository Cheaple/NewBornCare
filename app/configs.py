from pathlib import Path


class Config(object):
    """
    General Configs
    """
    SALT = "abcde"

    # SQLALCHEMY config
    basedir = Path(__file__).resolve().parent
    DATABASE = "newborn.db"
    USERNAME = "admin"
    PASSWORD = "admin"
    SECRET_KEY = "cheaple"
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{Path(basedir).joinpath(DATABASE)}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT config
    JWT_SALT = "abcde"
    JWT_EXPIRY = 24


configs = {
    "default": Config
}
