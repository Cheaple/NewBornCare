# -*- coding: utf-8 -*-
import os
import unittest

import coverage
from flask_script import Manager, Server

from app import create_app, db
from app.init_db import init_data, init_options, init_test_data
from app.utils import config

# import pandas as pd


# from flask_migrate import Migrate, MigrateCommand


COV = coverage.coverage(branch=True, include='app/*')
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
    loader.testNamePatterns = [filter + "*"] if filter is not None else None
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
def init_test_db():
    """Init Database for Testing"""
    # recreate the database and the db table
    db.drop_all()
    db.create_all()
    init_options()
    init_test_data()


@manager.command
def init_db():
    """Init Database"""
    # recreate the database and the db table
    db.drop_all()
    db.create_all()
    init_options()
    init_data()

# @manager.command
# def export_metadata():
#     writer = pd.ExcelWriter('data\\metadata.xlsx')
#     for t in meta.sorted_tables:
#         columns = []
#         for c in t.columns:
#             # print([c.name, c.doc, c.type, c.nullable, c.primary_key, [k.target_fullname for k in c.foreign_keys]])
#             columns.append([c.name, c.doc, c.type, c.nullable, c.primary_key])
#         df = pd.DataFrame(columns)
#         df.columns = ["列名", "描述", "类型", "空值", "主键"]
#         df["空值"] = df["空值"].map({False: "No", True: "Yes"})
#         df["主键"] = df["主键"].map({False: "No", True: "Yes"})
#         df.to_excel(writer, sheet_name=t.name)
#     writer.save()


if __name__ == '__main__':
    manager.run()
