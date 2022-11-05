from app.extensions import db


class Patient(db.Model):
    '''
    Patient
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String, nullable=False)
    birthdate = db.Column(db.DateTime, nullable=False)

    # Patient does not need an account necessarily.
    username = db.Column(db.String)
    password = db.Column(db.String)

    status = db.Column(db.Integer, nullable=False)
