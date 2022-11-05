from sqlalchemy import and_

from app.extensions import db
from app.models import Admin


class AdminService():
    def get_user_with_password(self, username, password):
        try:
            admin = Admin.query.filter(
                and_(
                    Admin.username == username,
                    Admin.password == password)).first()
            if admin is None:
                return "Administrator not found", False
            return admin, True
        except Exception as e:
            print(e)
            return "errors", False
