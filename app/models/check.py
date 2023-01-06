from sqlalchemy import text

from app.extensions import db


class Check(db.Model):
    '''
    Check for Patients
    '''
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        doc="巡视记录编号")  # immutable
    nurseId = db.Column(
        db.Integer,
        db.ForeignKey('nurse.id'),
        nullable=False,
        doc="巡视护士的护士编号")  # immutatble
    patientId = db.Column(
        db.Integer,
        db.ForeignKey('patient.id'),
        nullable=False,
        doc="患者编号")  # immutable
    transfusionId = db.Column(
        db.Integer,
        db.ForeignKey('transfusion.id'),
        nullable=True,
        doc="输液记录编号")  # immutable

    time = db.Column(db.Integer, nullable=False, doc="巡视时间")
    info = db.Column(db.String, nullable=True, doc="其他情况")

    ifExist = db.Column(
        db.Boolean,
        nullable=False,
        server_default=text('True'),
        doc='记录是否存在')
