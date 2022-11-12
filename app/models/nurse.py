from enum import unique
from app.extensions import db


class Nurse(db.Model):
    '''
    Nurse
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True, doc='用户名')
    password = db.Column(db.String(20), nullable=False, doc='密码')
    
    name = db.Column(db.String(20), nullable=False, doc='姓名')
    gender = db.Column(db.Integer, nullable=False, doc='性别')
    tel = db.Column(db.Integer, nullable=False, doc='联系方式')
    department = db.Column(db.Integer, nullable=False, doc='科室（通常是儿科）')
    
    status = db.Column(db.Integer, nullable=False, doc='工作状态')  # 0: 离职  1: 在职  ...
