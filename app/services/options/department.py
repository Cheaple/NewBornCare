from sqlalchemy import and_

from app.extensions import db
from app.models import Department


class DepartmentService():
    def get_department_list(self):
        try:
            content_result = db.session.query(
                Department.id,
                Department.name,
            ).all()
            department_list = [dict(zip(result.keys(), result))
                               for result in content_result]
            return department_list, "ok", True
        except Exception as e:
            print(e)
            return None, "error", False

    def add_department(self, name):
        try:
            department = Department(name=name)
            db.session.add(department)
            db.session.commit()
            return department.id, "ok", True
        except Exception as e:
            print(e)
            return 0, "department already exists", False

    def update_department(self, id, name=None):
        try:
            department = Department.query.get(id)
            if name:
                department.name = name
            db.session.commit()
            return department.id, "ok", True
        except Exception as e:
            print(e)
            return 0, "error", False
