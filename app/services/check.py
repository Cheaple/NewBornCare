from app.extensions import db
from app.models import Check


class CheckService():
    def get_check_list(self, patientId=None, transfusionId=None):
        try:
            where_clause = ""
            if patientId:
                where_clause = "WHERE ifExist IS TRUE AND patientId = " + \
                    str(patientId)
            elif transfusionId:
                where_clause = "WHERE ifExist IS TRUE AND transfusionId = " + \
                    str(transfusionId)

            # TODO: list是否应该返回所有信息？
            # Note: 'check' is a keyword in SQL
            content_base = '''
                SELECT
                    id,
                    nurseId,
                    patientId,
                    transfusionId,
                    time,
                    info
                FROM
                    `Check`
                {where}
            '''
            count_base = '''
                SELECT
                    COUNT(id) as count
                FROM
                    `Check`
                {where}
            '''
            sql_content = content_base.format(where=where_clause)
            sql_count = count_base.format(where=where_clause)

            content_result = db.session.execute(sql_content)
            count_result = db.session.execute(sql_count)
            check_list = [dict(zip(result.keys(), result))
                          for result in content_result]
            count = [dict(zip(result.keys(), result))
                     for result in count_result]

            return check_list, count[0]['count'], "ok get check list", True

        except Exception as e:
            print(e)
            return [], 0, "error", False

    def get_check(self, id):
        try:
            result = db.session.query(
                Check.id,
                Check.nurseId,
                Check.patientId,
                Check.transfusionId,
                Check.time,
                Check.info,
                Check.ifExist
            ).filter(Check.id == id).first()
            if result is None or result.ifExist is False:
                return None, "check not found", False
            check = dict(zip(result.keys(), result))
            del check["ifExist"]
            return check, "ok get check", True
        except Exception as e:
            print(e)
            return None, "error", False

    def add_check(self, content):
        try:
            check = Check(
                nurseId=content['nurseId'],
                patientId=content['patientId'],
                transfusionId=content['transfusionId'],

                time=content['time'],
                info=content['info'],
            )
            db.session.add(check)
            db.session.commit()
            return check.id, "ok add check", True
        except Exception as e:
            print(e)
            return 0, "error", False

    def update_check(self, id, content):
        try:
            check = Check.query.get(id)
            if check is None:
                return 0, "check not found", False

            if 'info' in content:
                check.info = content['info']
            if 'time' in content:
                check.time = content['time']

            db.session.commit()
            return check.id, "ok update check", True
        except Exception as e:
            print(e)
            return 0, "error", False

    def delete_check(self, id):
        try:
            check = Check.query.get(id)
            if check is None:
                return 0, "Administrator not found", False

            check.ifExist = False

            db.session.commit()
            return check.id, "ok delete check", True
        except Exception as e:
            print(e)
            return 0, "error", False
