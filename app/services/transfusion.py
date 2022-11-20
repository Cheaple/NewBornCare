from app.extensions import db
from app.models import Transfusion, TransfusionDrug


class TransfusionService():
    def get_transfusion_list(self, patientId):
        try:
            where_clause = "WHERE patientId = " + str(patientId)

            # TODO: list是否应该返回所有信息？
            content_base = '''
                SELECT
                    id,
                    nurseId,
                    patientId,
                    name,
                    startTime,
                    finishTime,
                    status,
                    vein,
                    tool,
                    info
                FROM
                    Transfusion
                {where}
            '''
            count_base = '''
                SELECT
                    COUNT(id) as count
                FROM
                    Transfusion
                {where}
            '''
            sql_content = content_base.format(where=where_clause)
            sql_count = count_base.format(where=where_clause)

            content_result = db.session.execute(sql_content)
            count_result = db.session.execute(sql_count)
            transfusion_list = [dict(zip(row.keys(), row))
                                for row in content_result]
            count = [dict(zip(result.keys(), result))
                     for result in count_result]

            return transfusion_list, count[0]['count'], True

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
                Transfusion.status,
                Transfusion.vein,
                Transfusion.tool,
                Transfusion.info,
            ).filter(Transfusion.id == id).first()
            if result is None:
                return "transfusion not found", False

            drugs = db.session.query(
                TransfusionDrug.id,
                TransfusionDrug.drug,
                TransfusionDrug.dose,
                TransfusionDrug.rate,
                TransfusionDrug.startTime,
                TransfusionDrug.status,
            ).filter(TransfusionDrug.transfusionId == id).all()

            transfusion = dict(zip(result.keys(), result))
            transfusion["drug"] = [dict(zip(row.keys(), row)) for row in drugs]
            return transfusion, True
        except Exception as e:
            print(e)
            return "errors", False

    def add_transfusion(self, content, drugs):
        try:
            transfusion = Transfusion(**content)
            db.session.add(transfusion)
            db.session.flush()
            for drug in drugs:
                drug['transfusionId'] = transfusion.id
                db.session.add(TransfusionDrug(**drug))

            db.session.commit()
            return transfusion.id, True
        except Exception as e:
            print(e)
            return 0, False
