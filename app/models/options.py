from app.extensions import db

class Department(db.Model):
    '''
    科室
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, doc="科室编号")
    name = db.Column(db.String, unique=True, nullable=False, doc="名称")

class Vein(db.Model):
    '''
    静脉
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, doc="静脉编号")
    name = db.Column(db.String, unique=True, nullable=False, doc="名称")

class Tool(db.Model):
    '''
    输液工具
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, doc="工具编号")
    name = db.Column(db.String, unique=True, nullable=False, doc="名称")

class Drug(db.Model):
    '''
    药品
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, doc="药品编号")
    name = db.Column(db.String, unique=True, nullable=False, doc="名称")