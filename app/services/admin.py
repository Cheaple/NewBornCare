from sqlalchemy import and_

from app.extensions import db
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
                return None, "Administrator not found", False
            return admin, "ok get admin", True
        except Exception as e:
            print(e)
            return None, "errors", False

    def add_admin(self, content):
        try:
            admin = Admin.query.filter(
                Admin.username == content['username']
            ).first()
            if admin is not None:
                return 0, "username already exists", False

            admin = Admin(
                username=str(content['username']),
                password=encipher(str(content['password'])),
                name=content['name'],
                department=content['department'],
                status=content['status'],
            )
            db.session.add(admin)
            db.session.commit()
            return admin.id, "ok add admin", True
        except Exception as e:
            print(e)
            return 0, "username already exists", False

    def update_admin(self, id, content):
        try:
            admin = Admin.query.get(id)
            if admin is None:
                return 0, "admin not found", False

            if 'username' in content:
                admin.username = str(content['username'])
            if 'password' in content:
                admin.password = encipher(str(content['password']))
            if 'name' in content:
                admin.name = content['name']
            if 'department' in content:
                admin.department = content['department']
            if 'status' in content:
                admin.status = content['status']

            db.session.commit()
            return admin.id, "ok update admin", True
        except Exception as e:
            print(e)
            return 0, "error", False
