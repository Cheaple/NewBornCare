# -*- coding: utf-8 -*-
import coverage
import os
from datetime import datetime

import unittest

from flask_script import Manager, Server
# from flask_migrate import Migrate, MigrateCommand

from app import create_app, db
from app.utils import config
from app.init_db import init_test_data, init_options

COV=coverage.coverage(branch=True,include='app/*')
COV.start()

app = create_app(os.getenv('TYPE', 'default'))

host = config.get_yaml('app.HOST')
port = config.get_yaml('app.PORT')

manager = Manager(app)
manager.add_command('runserver', Server(host=host, port=port))

# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)

@manager.command
def test(filter=None):
    """Run the unit tests"""
    loader = unittest.TestLoader()
    loader.testNamePatterns = [filter+"*"] if filter is not None else None
    tests = loader.discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

    COV.stop()
    COV.save()
    print('Coverage:')
    COV.report()
    basedir = os.path.abspath(os.path.dirname("backend"))
    covdir = os.path.join(basedir, 'test_report')
    COV.html_report(directory=covdir)
    
    print('HTML version: file://%s/index.html' % covdir)

@manager.command
def init_db():
    """Init Database"""
    # recreate the database and the db table
    db.drop_all()
    db.create_all()
    init_options()
    init_test_data()

    
if __name__ == '__main__':
    manager.run()
