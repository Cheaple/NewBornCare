from codecs import getencoder
from unicodedata import name
from sqlalchemy import and_

from app.extensions import db
from app.models import Check

class CheckService():
    def get_check_list(self, patientId = None, transfusionId = None):
        try:
            where_clause = ""
            if patientId:
                where_clause = "WHERE patientId = " + str(patientId)
            elif transfusionId:
                where_clause = "WHERE transfusionId = " + str(transfusionId)

            # TODO: list是否应该返回所有信息？
            # Note: 'check' is a keyword in SQL
            content_base = '''
                SELECT
                    id,
                    nurseId,
                    patientId,
                    transfusionId,
                    time,
                    dose,
                    rate,
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
            check_list = [dict(zip(result.keys(), result)) for result in content_result]
            count = [dict(zip(result.keys(), result)) for result in count_result]

            return check_list, count[0]['count'], True

        except Exception as e:
            print(e)
            return [], 0, False
    
    def get_check(self, id):
        try:
            result = db.session.query(
                Check.id,
                Check.nurseId,
                Check.patientId,
                Check.transfusionId,
                Check.time,
                Check.dose,
                Check.rate,
                Check.info,
            ).filter(Check.id == id).first()
            if result is None:
                return "check not found", False
            return dict(zip(result.keys(), result)), True
        except Exception as e:
            print(e)
            return "errors", False
    
    def add_check(self, content):
        try:
            check = Check(
                nurseId=content['nurseId'],
                patientId=content['patientId'],
                transfusionId=content['transfusionId'],
                
                time=content['time'],
                dose=content['dose'],
                rate=content['rate'],
                info=content['info'],
            )
            db.session.add(check)
            db.session.commit()
            return check.id, True
        except Exception as e:
            print(e)
            return 0, False