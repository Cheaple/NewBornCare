# -*- coding: utf-8 -*-
import os
from unicodedata import name

from flask_script import Manager

from app import create_app, db
from app.utils import encipher

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
        department=0)
    nurse = models.Nurse(
        username='nurse',
        password=encipher('nurse'),
        name='测试护士',
        department=5,
        status=1)
    #patient = models.Patient(username='patient', password='patient', name='测试患者')
    db.session.add(admin)
    db.session.add(nurse)

    # commit the changes
    db.session.commit()


if __name__ == '__main__':
    manager.run()
