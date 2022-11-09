# -*- coding: utf-8 -*-
from datetime import date, datetime
import os
from unicodedata import name

from flask_script import Manager

from app import create_app, db, models
from app.utils import encipher, toTimestamp

app = create_app(os.getenv('TYPE', 'default'))

manager = Manager(app)


@manager.command
def init_db():
    """Init Database"""
    from app import models

    # create the database and the db table
    db.create_all()

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
        department=1,
        status=1)

    patient = models.Patient(
        name='测试患儿',
        gender=0,
        birthdate=toTimestamp(datetime(2022,11,1,12,0,0)),
        #palmprint=,
        guardian = "患儿父",
        guardianId = "42100220000725141x",
        relation = 1,
        tel = 19972644417,
        status=1,
        inDate=toTimestamp(datetime.now()),
        department=1, 
        room=234,
        bed=3
    )

    transfusion = models.Transfusion(
        nurseId=1,
        patientId=1,
        startTime=toTimestamp(datetime.now()),
        status=1,

        vein=2,
        drug=3,
        dose=200,
        tool=1,
        rate=3,
        info="心跳较快"
    )

    check = models.Check(
        nurseId=10,
        patientId=1,
        transfusionId=1,
        time=toTimestamp(datetime.now()),
        dose=100,
        rate=3,
        info="心跳正常"
    )

    db.session.add(admin)   
    db.session.add(nurse)
    db.session.add(patient)
    db.session.add(transfusion)
    db.session.add(check)

    # commit the changes
    db.session.commit()


if __name__ == '__main__':
    manager.run()
