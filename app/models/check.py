from enum import unique
from pydoc import doc
from app.extensions import db


class Check(db.Model):
    '''
    Check for Patients
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nurse_id = db.Column(db.Integer, nullable=False, doc="巡视护士")
    patient_id = db.Column(db.Integer, nullable=False, doc="病人")
    transfusion_id = db.Column(db.Integer, doc="输液记录")
    time = db.Column(db.DateTime, nullable=False, doc="巡视时间")

    dose = db.Column(db.Integer, nullable=False, doc="药量")
    rate = db.Column(db.Integer, nullable=False, doc="滴速（滴/秒）") 
    info = db.Column(db.String, nullable=True, doc="其他情况")
