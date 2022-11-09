from codecs import getencoder
from unicodedata import name
from sqlalchemy import and_

from app.extensions import db
from app.models import Transfusion


class TransfusionService():
    def get_transfusion_list(self, patientId):
        try:
            where_clause = "WHERE patientId  = " + str(patientId)

            # TODO: list是否应该返回所有信息？
            content_base = '''
                SELECT
                    id,
                    nurseId,
                    patientId,
                    startTime,
                    finishTime,
                    vein,
                    drug,
                    dose,
                    tool,
                    rate,
                    info
                FROM
                    transfusion
                {where}
            '''
            count_base = '''
                select
                    count(id) as count
                from
                    transfusion
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
    
    def get_transfusion(self, id):
        try:
            result = db.session.query(
                Transfusion.id,
                Transfusion.nurseId,
                Transfusion.patientId,
                Transfusion.startTime,
                Transfusion.finishTime,
                Transfusion.vein,
                Transfusion.drug,
                Transfusion.dose,
                Transfusion.tool,
                Transfusion.rate,
                Transfusion.info,
            ).filter(Transfusion.id == id).first()
            transfusion = dict(zip(result.keys(), result))
            if transfusion is None:
                return "transfusion not found", False
            return transfusion, True
        except Exception as e:
            print(e)
            return "errors", False
    
    def add_transfusion(self, content):
        try:
            transfusion = Transfusion(
                nurseId=content['nurseId'],
                patientId=content['patientId'],
                startTime=content['startTime'],
                
                vein=content['vein'],
                drug=content['drug'],
                dose=content['dose'],
                tool=content['tool'],
                rate=content['rate'],
                info=content['info'],
            )
            db.session.add(transfusion)
            db.session.commit()
            return transfusion.id, True
        except Exception as e:
            print(e)
            return 0, False