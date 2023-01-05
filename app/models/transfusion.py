from app.extensions import db

from sqlalchemy import text


class Transfusion(db.Model):
    '''
    Transfusion
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, doc="输液记录编号")
    nurseId = db.Column(db.Integer, db.ForeignKey('nurse.id'), nullable=False, doc="护士编号")  # immutable
    patientId = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False, doc="患者编号")  # immutable
    name = db.Column(db.Integer, nullable=False, doc="名称")  # 若无名称，则直接以药物名代替
    startTime = db.Column(db.Integer, nullable=False, doc="开始时间") 
    finishTime = db.Column(db.Integer, nullable=True, doc="结束时间")

    # form = Column(db.Integer, nullable=False, doc="类型")
    drugCnt = db.Column(db.Integer, nullable=False, doc="药物数量")
    vein = db.Column(db.Integer, db.ForeignKey('vein.id'), nullable=False, doc="静脉编号")
    tool = db.Column(db.Integer, db.ForeignKey('tool.id'), nullable=False, doc="工具编号")
    info = db.Column(db.String, nullable=True, doc="其他情况")

    # 0: 已完成  -1: 中止  n: 正进行到阶段 n (n > 1)
    status = db.Column(db.Integer, nullable=False,doc='输液状态')

    ifExist = db.Column(db.Boolean, nullable=False, server_default=text('True'), doc='记录是否存在')

class TransfusionDrug(db.Model):
    '''
    A Drug in a Transfusion
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, doc="输液记录药品编号")
    transfusionId = db.Column(db.Integer, db.ForeignKey('transfusion.id'), nullable=False, doc="输液记录编号")  # immutable
    seq = db.Column(db.Integer, nullable=False, doc="序号")
    drug = db.Column(db.Integer, db.ForeignKey('drug.id'), nullable=False, doc="药物编号")
    dose = db.Column(db.Integer, nullable=False, doc="药量")
    rate = db.Column(db.Integer, nullable=False, doc="滴速")
    startTime = db.Column(db.Integer, nullable=True, doc="开始时间")
    # finishTime = db.Column(db.Integer, nullable=True, doc="结束时间")

    # 0：已完成  1：进行中  2：未开始  -1：中止
    status = db.Column(db.Integer, nullable=False, server_default="2", doc='药品的输液状态')
