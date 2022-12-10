from datetime import datetime

from app import models
from app.utils import toTimestamp, encipher
from app.extensions import db

def init_options():
    '''
    init options
    '''
    import csv

    with open("data/department.csv", encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)
        #header = next(csv_reader)
        for row in csv_reader:
            db.session.add(models.Department(name=row[0]))
    with open("data/vein.csv", encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)
        #header = next(csv_reader)
        for row in csv_reader:
            db.session.add(models.Vein(name=row[0]))
    with open("data/tool.csv", encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)
        #header = next(csv_reader)
        for row in csv_reader:
            db.session.add(models.Tool(name=row[0]))
    with open("data/drug.csv", encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)
        #header = next(csv_reader)
        for row in csv_reader:
            db.session.add(models.Drug(name=row[0]))
            
    db.session.commit()

def init_test_data():
    '''
    init test data
    '''
    admin = models.Admin(
        username='admin',
        password=encipher('admin'),
        name='测试管理员',
        department=0,
        status=1
    )

    nurse = models.Nurse(
        username='nurse',
        password=encipher('nurse'),
        name='测试护士',
        gender=1,
        tel=19912345678,
        department=3,
        status=1)

    patient = models.Patient(
        username='patient',
        password=encipher('patient'),
        name='测试患儿',
        gender=0,
        birthdate=toTimestamp(datetime(2022, 11, 1, 12, 0, 0)),
        # palmprint=,
        guardian="患儿父",
        guardianId="42100220000725141x",
        relation=1,
        tel=19972644417,
        status=1,
        inDate=toTimestamp(datetime.now()),
        department=3,
        room=234,
        bed=3
    )

    transfusion = models.Transfusion(
        nurseId=1,
        patientId=1,
        startTime=toTimestamp(datetime.now()),
        name="葡萄糖",
        status=1,
        drugCnt=2,
        vein=2,
        tool=1,
        info="心跳较快"
    )

    drug = models.TransfusionDrug(
        transfusionId = 1,
        seq = 1,
        startTime=toTimestamp(datetime.now()),
        rate = 8,
        drug=1,
        dose=200,
        status = 1,  # 进行中
    )

    drug2 = models.TransfusionDrug(
        transfusionId = 1,
        seq = 2,
        rate = 10,
        drug=2,
        dose=300,
        status = 2,  # 未开始
    )

    check = models.Check(
        nurseId=1,
        patientId=1,
        transfusionId=1,
        time=toTimestamp(datetime.now()),
        info="心跳正常"
    )

    db.session.add(admin)
    db.session.add(nurse)
    db.session.add(patient)
    db.session.add(transfusion)
    db.session.add(drug)
    db.session.add(drug2)
    db.session.add(check)

    # commit the changes
    db.session.commit()

