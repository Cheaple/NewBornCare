from sqlalchemy import and_

from app.models import Admin
from app.utils import encipher


class AdminService():
    def get_user_with_password(self, username, password):
        try:
            admin = Admin.query.filter(
                and_(
                    Admin.username == username,
                    Admin.password == encipher(password))).first()
            if admin is None:
                return "Administrator not found", False
            return admin, True
        except Exception as e:
            print(e)
            return "errors", False
