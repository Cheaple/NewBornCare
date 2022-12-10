from app.extensions import db


class Check(db.Model):
    '''
    Check for Patients
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # immutable
    nurseId = db.Column(db.Integer, nullable=False, doc="巡视护士")  # immutatble
    patientId = db.Column(db.Integer, nullable=False, doc="病人")  # immutable
    transfusionId = db.Column(db.Integer, nullable=True, doc="输液记录")  # immutable

    time = db.Column(db.Integer, nullable=False, doc="巡视时间")
    info = db.Column(db.String, nullable=True, doc="其他情况")
