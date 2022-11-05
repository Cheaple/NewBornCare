from app.extensions import db


class Nurse(db.Model):
    '''
    Nurse
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    department = db.Column(db.Integer)

    status = db.Column(db.Integer, nullable=False)
