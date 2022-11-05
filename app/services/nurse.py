from sqlalchemy import and_

from app.extensions import db
from app.models import Admin, Nurse


class NurseService():
    def get_user_with_password(self, username, password):
        try:
            nurse = Nurse.query.filter(
                and_(
                    Nurse.username == username,
                    Nurse.password == password)).first()
            if nurse is None:
                return "user not found", False
            return nurse, True
        except Exception as e:
            print(e)
            return "errors", False
