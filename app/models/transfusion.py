from app.extensions import db


class Transfusion(db.Model):
    '''
    Transfusion
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nurse_id = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    status = db.Column(db.Integer, nullable=False)
