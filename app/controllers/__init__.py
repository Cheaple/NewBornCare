from app.controllers import hello
from app.controllers.admin import admin
from app.controllers.nurse import nurse
from app.controllers.patient import patient
from app.controllers.transfusion import transfusion
from app.controllers.check import check

blueprints = [
    hello.bp,
    admin.bp,
    nurse.bp,
    patient.bp,
    transfusion.bp,
    check.bp
]
