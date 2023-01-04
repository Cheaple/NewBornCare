"""
Flask Extensions
"""
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

meta = MetaData()
db = SQLAlchemy(metadata=meta)
swagger = Swagger()
