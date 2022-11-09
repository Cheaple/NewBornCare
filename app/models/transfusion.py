from enum import unique
from pydoc import doc
from app.extensions import db


class Transfusion(db.Model):
    '''
    Transfusion
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nurseId = db.Column(db.Integer, nullable=False, doc="输液护士")
    patientId = db.Column(db.Integer, nullable=False, doc="输液病人")
    startTime = db.Column(db.Integer, nullable=False, doc="开始时间")
    finishTime = db.Column(db.Integer, nullable=True, doc="结束时间")
    status = db.Column(db.Integer, nullable=False, doc='输液状态')  # 0: 已完成  1: 进行中  2: 中止 

    #form = Column(db.Integer, nullable=False, doc="类型")
    vein = db.Column(db.Integer, nullable=False, doc="静脉")
    drug = db.Column(db.Integer, nullable=False, doc="药物")
    dose = db.Column(db.Integer, nullable=False, doc="药量")
    tool = db.Column(db.Integer, nullable=False, doc="输液工具")
    rate = db.Column(db.Integer, nullable=False, doc="滴速（滴/秒）") 
    info = db.Column(db.String, nullable=True, doc="其他情况")

'''
        id
        nurseId
        patientId
        startTime
        finishTime

        vein
        drug
        dose
        tool
        rate
        info
'''