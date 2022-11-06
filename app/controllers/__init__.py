from app.controllers import hello
from app.controllers.admin import admin
from app.controllers.nurse import nurse
from app.controllers.patient import patient


blueprints = [
    hello.bp,
    admin.bp,
    nurse.bp,
    patient.bp
]
