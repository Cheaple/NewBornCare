from datetime import datetime

from app.extensions import db
from app.models import Transfusion, TransfusionDrug
from app.utils import toTimestamp


class TransfusionService():
    def get_transfusion_list(self, patientId):
        try:
            where_clause = "WHERE ifExist IS TRUE AND patientId = " + \
                str(patientId)

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
                    drugCnt,
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

            return transfusion_list, count[0]['count'], "ok get transfusion list", True

        except Exception as e:
            print(e)
            return [], 0, "error", False

    def get_transfusion(self, id):
        try:
            result = db.session.query(
                Transfusion.id,
                Transfusion.nurseId,
                Transfusion.patientId,
                Transfusion.name,
                Transfusion.startTime,
                Transfusion.finishTime,
                Transfusion.status,
                Transfusion.drugCnt,
                Transfusion.vein,
                Transfusion.tool,
                Transfusion.info,
                Transfusion.ifExist
            ).filter(Transfusion.id == id).first()
            if result is None or result.ifExist is False:
                return None, "transfusion not found", False

            drugs = db.session.query(
                TransfusionDrug.id,
                TransfusionDrug.seq,
                TransfusionDrug.drug,
                TransfusionDrug.dose,
                TransfusionDrug.rate,
                TransfusionDrug.startTime,
                TransfusionDrug.status,
            ).filter(TransfusionDrug.transfusionId == id).all()

            transfusion = dict(zip(result.keys(), result))
            del transfusion["ifExist"]
            transfusion["drug"] = [dict(zip(row.keys(), row)) for row in drugs]
            return transfusion, "ok get transfusion", True
        except Exception as e:
            print(e)
            return None, "errors", False

    def add_transfusion(self, content, drugs):
        try:
            transfusion = Transfusion(**content)
            db.session.add(transfusion)
            db.session.flush()
            for drug in drugs:
                drug['transfusionId'] = transfusion.id
                db.session.add(TransfusionDrug(**drug))

            db.session.commit()
            return transfusion.id, "ok add transfusion", True
        except Exception as e:
            print(e)
            return 0, "error", False

    def update_transfusion(self, id, content):
        try:
            transfusion = Transfusion.query.get(id)
            if transfusion is None:
                return 0, "transfusion not found", False

            if 'name' in content:
                transfusion.name = content['name']
            if 'startTime' in content:
                transfusion.startTime = content['startTime']
            if 'finishTime' in content:
                transfusion.finishTime = content['finishTime']
            if 'vein' in content:
                transfusion.vein = content['vein']
            if 'tool' in content:
                transfusion.tool = content['tool']
            if 'info' in content:
                transfusion.info = content['info']

            if 'status' in content:
                # 0：已完成  1：进行中  2：未开始  -1：中止
                transfusion.status = content['status']

            db.session.commit()
            return transfusion.id, "ok update transfusion", True
        except Exception as e:
            print(e)
            return 0, "error", False

    def update_transfusion_drug(self, tId, drugSeq, content):
        try:
            drug = TransfusionDrug.query.filter(
                TransfusionDrug.transfusionId == tId,
                TransfusionDrug.seq == drugSeq
            ).first()
            if drug is None:
                return 0, "drug not found", False

            if 'seq' in content:
                drug.seq = content['seq']
            if 'drug' in content:
                drug.drug = content['drug']
            if 'dose' in content:
                drug.dose = content['dose']
            if 'rate' in content:
                drug.rate = content['rate']
            if 'startTime' in content:
                drug.startTime = content['startTime']

            if 'status' in content:
                drug.status = content['status']

            db.session.commit()

            return drug.id, "ok update drug", True
        except Exception as e:
            print(e)
            return 0, "error", False

    def update_transfusion_next(self, tId):
        '''
        更新输液记录：换药
        '''
        try:
            transfusion = Transfusion.query.get(tId)
            drugSeq = transfusion.status

            if transfusion.status >= transfusion.drugCnt:  # 已到最后药品
                return self.update_transfusion_finish(tId)
            elif transfusion.status <= 0:
                return 0, "already finished", False

            transfusion.status += 1
            cur_drug = TransfusionDrug.query.filter_by(
                transfusionId=tId, seq=drugSeq).one()
            cur_drug.status = 0  # 将当前药物标记完成
            next_drug = TransfusionDrug.query.filter_by(
                transfusionId=tId, seq=drugSeq + 1).one()
            next_drug.status = 1  # 将下一个药物标记开始
            next_drug.startTime = toTimestamp(datetime.now())
            msg = "ok change drug"

            db.session.commit()
            return transfusion.id, msg, True
        except Exception as e:
            print(e)
            return 0, "error", False

    def update_transfusion_finish(self, tId):
        '''
        更新输液记录：完成
        '''
        try:
            transfusion = Transfusion.query.get(tId)
            drugSeq = transfusion.status

            if transfusion.status > 0 and transfusion.status < transfusion.drugCnt:  # 未到最后药品
                return transfusion.id, "not finished yet", False
            elif transfusion.status <= 0:
                return 0, "already finished", False

            transfusion.status = 0
            transfusion.finishTime = toTimestamp(datetime.now())
            cur_drug = TransfusionDrug.query.filter_by(
                transfusionId=tId, seq=drugSeq).one()
            cur_drug.status = 0  # 将当前药物标记完成
            msg = "ok finish transfusion"

            db.session.commit()
            return transfusion.id, msg, True
        except Exception as e:
            print(e)
            return 0, "error", False

    def delete_transfusion(self, id):
        try:
            transfusion = Transfusion.query.get(id)
            if transfusion is None:
                return 0, "Administrator not found", False

            transfusion.ifExist = False

            db.session.commit()
            return transfusion.id, "ok delete transfusion", True
        except Exception as e:
            print(e)
            return 0, "error", False
