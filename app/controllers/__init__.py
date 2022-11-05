from app.controllers import hello
from app.controllers.admin import admin
from app.controllers.nurse import nurse


blueprints = [
    hello.bp,
    admin.bp,
    nurse.bp
]
