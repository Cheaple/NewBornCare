import csv
from datetime import datetime
from random import choice, randint

from app import models
from app.utils import toTimestamp, encipher
from app.extensions import db

def init_options():
    '''
    init options
    '''

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

def init_prod_data():
    '''
    init production data
    '''

    admin = models.Admin(
        username='admin',
        password=encipher('admin'),
        name='管理员',
        department=0,
        status=1
    )
    db.session.add(admin)

    with open("data/nurse.csv", encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)
        for row in csv_reader:
            content = dict(zip(header, row))
            print(content)
            db.session.add(models.Nurse(**content))

    with open("data/patient.csv", encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)
        for row in csv_reader:
            content = dict(zip(header, row))
            print(content)
            db.session.add(models.Patient(**content))

    db.session.commit()


def init_data():
    '''
    init data
    '''

    def generate_name(gender = None):
        family_names = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏"\
            "陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳"
        female_names = "念倩幂辰慕蔚理霜依唐喻微紫盼语音杏晓葵媛采乐青月松彩碧蓉滢含"\
            "馥素沐白南容知艳梨琦盈筠音茹静尔沛娅玉宸畅韵丹尚钰桐美梦璐荷"\
            "悦菡曦聪希黛虞歆可爽雅初昕缦洁迪凌靖芝忆熙芊奕帆露灵霄颖笛迎"
        male_names = "伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁"\
            "诚先敬震振壮会思群豪心邦承乐绍功松善厚庆磊民友裕河哲江超"\
            "浩亮政谦亨奇固之轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭鹏泽"

        if gender is None:
            gender = randint(0, 1) % 2 + 1
        if gender == 1:
            name = family_names[randint(0, len(family_names) - 1)] + male_names[randint(0, len(male_names) - 1)]
            if randint(0, 4) % 3 != 0:
                name += male_names[randint(0, len(male_names) - 1)]
        else:
            name = family_names[randint(0, len(family_names) - 1)] + female_names[randint(0, len(female_names) - 1)]
            if randint(0, 4) % 3 != 0:
                name += female_names[randint(0, len(female_names) - 1)]
        return name

    def generate_time(now = None, days = 365):
        if now is None:
            now = toTimestamp(datetime.now())
        return now - randint(1, days) * 24 * 3600

    admin = models.Admin(
        username='admin',
        password=encipher('admin'),
        name='管理员',
        department=0,
        status=1
    )
    db.session.add(admin)

    numNurse = 50
    numPatient = 200

    # Nurse
    keys = ["username", "password", "name", "gender", "tel", "department", "status"]
    for i in range(1, numNurse + 1):
        values = [
            "nurse{:0>3d}".format(i),
            encipher("nurse{:0>3d}".format(i)),
            generate_name(2),
            2,
            randint(13100000000, 19999999999),
            randint(1, 5),
            1
        ]
        content = dict(zip(keys, values))
        # print(content)
        db.session.add(models.Nurse(**content))

    # Patient
    keys = [
        "name", "gender", "birthdate", 
        "guardian", "guardianId", "relation", "tel", 
        "status", "inDate", "outDate", "department", "room", "bed", 
        "allergy",
        "username", "password", 
    ]
    for i in range(1, numPatient + 1):
        gender = i % 2 + 1
        inDate = generate_time(days = 10)
        values = [
            generate_name(gender), gender, generate_time(inDate, days = 3650),
            generate_name(), str(randint(110000194910010001, 110000200312319999)), randint(1, 4), randint(13100000000, 19999999999),
            1, inDate, None, randint(1, 5), randint(1, 20), choice([1, 2, 3, None]),
            "无过敏",
            "patient{:0>3d}".format(i), encipher("patient{:0>3d}".format(i)),    
        ]
        content = dict(zip(keys, values))
        # print(content)
        db.session.add(models.Patient(**content))

    # Transfusion
    for j in range(5):
        for i in range(1, numPatient + 1):
            transfusion = models.Transfusion(
                nurseId=randint(1, numNurse),
                patientId=i,
                startTime=generate_time(),
                name="输液治疗{}".format(j),
                status=0,
                drugCnt=2,
                vein=randint(1, 5),
                tool=randint(1, 5),
                info="心跳较快"
            )
            drug1 = models.TransfusionDrug(
                transfusionId = j * numPatient + i,
                seq=1,
                startTime=transfusion.startTime,
                rate=randint(1, 8),
                drug=1,
                dose=400,
                status=0,  # 已完成
            )
            drug2 = models.TransfusionDrug(
                transfusionId = j * numPatient + i,
                seq=2,
                startTime=transfusion.startTime + 3600,
                rate=randint(1, 8),
                drug=randint(2, 5),
                dose=100,
                status=0,  # 已完成
            )
            db.session.add(transfusion)
            db.session.add(drug1)
            db.session.add(drug2)

    # Check
    for j in range(30):
        for i in range(1, numPatient + 1):
            check = models.Check(
                nurseId=randint(1, numNurse),
                patientId=i,
                transfusionId=None,
                time=generate_time(),
                info="一切正常"
            )
            db.session.add(check)
    
    db.session.commit()

    
    

