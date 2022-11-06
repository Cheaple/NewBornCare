from sqlalchemy import and_

from app.extensions import db
from app.models import Admin


class PatientService():
    def get_patient_list(self, department=0):
        try:
            where_clause = "WHERE status <> 0 "
            if department != 0:
                where_clause += ("AND department = " + str(department))

            # todo: list是否应该返回所有信息？
            content_base = '''
                SELECT
                    id,
                    name,
                    gender,
                    birthdate,
                    palmprint,
                    tel,
                    indate,
                    outdate,
                    department,
                    room,
                    bed,
                    allergy
                FROM
                    patient
                {where}
            '''
            count_base = '''
                select
                    count(id) as count
                from
                    patient
                {where}
            '''
            sql_content = content_base.format(where=where_clause)
            sql_count = count_base.format(where=where_clause)

            content_result = db.session.execute(sql_content)
            count_result = db.session.execute(sql_count)
            post_list = [dict(zip(result.keys(), result)) for result in content_result]
            count = [dict(zip(result.keys(), result)) for result in count_result]

            return post_list, count[0]['count'], True

        except Exception as e:
            print(e)
            return [], 0, False
    
    def get_patient(self, id):
        pass
