"""
Flask Extensions
"""
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
swagger = Swagger()
