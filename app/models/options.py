from sqlalchemy import text

from app.extensions import db


class Department(db.Model):
    '''
    科室
    '''
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        doc="科室编号")
    name = db.Column(db.String, unique=True, nullable=False, doc="名称")
    ifExist = db.Column(
        db.Boolean,
        nullable=False,
        server_default=text('True'),
        doc='记录是否存在')


class Vein(db.Model):
    '''
    静脉
    '''
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        doc="静脉编号")
    name = db.Column(db.String, unique=True, nullable=False, doc="名称")
    ifExist = db.Column(
        db.Boolean,
        nullable=False,
        server_default=text('True'),
        doc='记录是否存在')


class Tool(db.Model):
    '''
    输液工具
    '''
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        doc="工具编号")
    name = db.Column(db.String, unique=True, nullable=False, doc="名称")
    ifExist = db.Column(
        db.Boolean,
        nullable=False,
        server_default=text('True'),
        doc='记录是否存在')


class Drug(db.Model):
    '''
    药品
    '''
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        doc="药品编号")
    name = db.Column(db.String, unique=True, nullable=False, doc="名称")
    ifExist = db.Column(
        db.Boolean,
        nullable=False,
        server_default=text('True'),
        doc='记录是否存在')
