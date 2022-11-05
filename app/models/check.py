from app.extensions import db


class Check(db.Model):
    '''
    Check for Patients
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nurse_id = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.Integer, nullable=False)
    transfusion_id = db.Column(db.Integer)
    time = db.Column(db.DateTime, nullable=False)
