from sqlalchemy import text

from app.extensions import db


class Admin(db.Model):
    '''
    Administrator
    '''
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        doc="管理员编号")
    username = db.Column(db.String(20), nullable=False, unique=True, doc='用户名')
    password = db.Column(db.String(20), nullable=False, doc='密码')

    name = db.Column(db.String(20), nullable=False, doc='姓名')
    department = db.Column(db.Integer, doc='科室编号')

    # 0: 离职  1: 在职  ...
    status = db.Column(db.Integer, nullable=False, doc='工作状态')

    ifExist = db.Column(
        db.Boolean,
        nullable=False,
        server_default=text('True'),
        doc='记录是否存在')
