from app.extensions import db


class Transfusion(db.Model):
    '''
    Transfusion
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nurseId = db.Column(db.Integer, nullable=False, doc="输液护士")
    patientId = db.Column(db.Integer, nullable=False, doc="输液病人")
    name = db.Column(db.Integer, nullable=False, doc="名称")  # 若无名称，则直接以药物名代替
    startTime = db.Column(db.Integer, nullable=False, doc="开始时间")
    finishTime = db.Column(db.Integer, nullable=True, doc="结束时间")
    

    # 0: 已完成  1: 进行中  -1: 中止
    status = db.Column(db.Integer, nullable=False,doc='输液状态')

    # form = Column(db.Integer, nullable=False, doc="类型")
    vein = db.Column(db.Integer, nullable=False, doc="静脉")
    tool = db.Column(db.Integer, nullable=False, doc="输液工具")
    info = db.Column(db.String, nullable=True, doc="其他情况")

class TransfusionDrug(db.Model):
    '''
    A Drug in a Transfusion
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transfusionId = db.Column(db.Integer, nullable=False, doc="输液记录")
    drug = db.Column(db.Integer, nullable=False, doc="药物")
    dose = db.Column(db.Integer, nullable=False, doc="药量")
    rate = db.Column(db.Integer, nullable=False, doc="滴速")
    startTime = db.Column(db.Integer, nullable=True, doc="开始时间")

    # 0：已完成  1：进行中  2：未开始  -1：中止
    status = db.Column(db.Integer, nullable=False, server_default="2", doc='状态')