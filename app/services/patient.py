from codecs import getencoder
from unicodedata import name
from sqlalchemy import and_

from app.extensions import db
from app.models import Patient


class PatientService():
    def get_patient_list(self, department=0):
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
                    birthdate,
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
        try:
            result = db.session.query(
                Patient.id,
                Patient.name,
                Patient.gender,
                Patient.birthdate,
                Patient.palmprint,
                Patient.guardian,
                Patient.guardianId,
                Patient.relation,
                Patient.tel,
                Patient.status,
                Patient.inDate,
                Patient.outDate,
                Patient.department,
                Patient.room,
                Patient.bed
            ).filter(Patient.id == id).first()
            patient = dict(zip(result.keys(), result))
            if patient is None:
                return "user not found", False
            return patient, True
        except Exception as e:
            print(e)
            return "errors", False
    
    def add_patient(self, content):
        try:
            patient = Patient(
                name=content['name'],
                gender=content['gender'],
                birthdate=content['birthdate'],
                # palmprint=content['palmprint'],
                guardian=content['guardian'],
                guardianId=content['guardianId'],
                relation=content['relation'],
                tel=content['tel'],
                status=content['status'],
                inDate=content['inDate'],
                department=content['department'],
                room=content['room'],
                bed=content['bed']
            )
            db.session.add(patient)
            db.session.commit()
            return patient.id, True
        except Exception as e:
            print(e)
            return 0, False