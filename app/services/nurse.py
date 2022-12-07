from sqlalchemy import and_

from app.extensions import db
from app.models import Nurse
from app.utils import encipher


class NurseService():
    def get_nurse_with_password(self, username, password):
        # print(username, password)
        try:
            nurse = Nurse.query.filter(
                and_(
                    Nurse.username == username,
                    Nurse.password == encipher(password))).first()
            if nurse is None:
                return None, "nurse not found or wrong password", False
            return nurse, "ok get nurse", True
        except Exception as e:
            print(e)
            return None, "errors", False

    def get_nurse_list(self, department=0):
        try:
            where_clause = "WHERE status <> 0 "
            if department != 0:
                where_clause += ("AND department = " + str(department))

            # TODO: list是否应该返回所有信息？
            content_base = '''
                SELECT
                    id,
                    name,
                    gender,
                    tel,
                    department,
                    status
                FROM
                    Nurse
                {where}
            '''
            count_base = '''
                SELECT
                    COUNT(id) as count
                FROM
                    Nurse
                {where}
            '''
            sql_content = content_base.format(where=where_clause)
            sql_count = count_base.format(where=where_clause)

            content_result = db.session.execute(sql_content)
            count_result = db.session.execute(sql_count)
            nurse_list = [dict(zip(result.keys(), result))
                          for result in content_result]
            count = [dict(zip(result.keys(), result))
                     for result in count_result]

            return nurse_list, count[0]['count'], "ok get nurse list", True

        except Exception as e:
            print(e)
            return [], 0, "error", False

    def get_nurse(self, id):
        try:
            result = db.session.query(
                Nurse.id,
                Nurse.username,
                Nurse.name,
                Nurse.gender,
                Nurse.tel,
                Nurse.department,
                Nurse.status,
            ).filter(Nurse.id == id).first()
            if result is None:
                return None, "nurse not found", False
            return dict(zip(result.keys(), result)), "ok get nurse", True
        except Exception as e:
            print(e)
            return None, "error", False

    def add_nurse(self, content):
        try:
            nurse = Nurse.query.filter(
                Nurse.username == content['username']
            ).first()
            if nurse is not None:
                return 0, "username already exists", False

            nurse = Nurse(
                username=str(content['username']),
                password=encipher(str(content['password'])),
                name=content['name'],
                gender=content['gender'],
                tel=content['tel'],
                department=content['department'],
                status=content['status'],
            )
            db.session.add(nurse)
            db.session.commit()
            return nurse.id, "ok add nurse", True
        except Exception as e:
            print(e)
            return 0, "username already exists", False

    def update_nurse(self, id, content):
        try:
            nurse = Nurse.query.get(id)
            if nurse is None:
                return 0, "nurse not found", False

            if 'username' in content:
                nurse.username = str(content['username'])
            if 'password' in content:
                nurse.password = encipher(str(content['password']))
            if 'name' in content:
                nurse.name = content['name']
            if 'gender' in content:
                nurse.gender = content['gender']
            if 'tel' in content:
                nurse.tel = content['tel']
            if 'department' in content:
                nurse.department = content['department']
            if 'status' in content:
                nurse.status = content['status']

            db.session.commit()
            return nurse.id, "ok update nurse", True
        except Exception as e:
            print(e)
            return 0, "error", False
