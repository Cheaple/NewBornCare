from sqlalchemy import and_

from app.extensions import db
from app.models import Drug


class DrugService():
    def get_drug_list(self):
        try:
            content_result = db.session.query(
                Drug.id,
                Drug.name,
            ).all()
            drug_list = [dict(zip(result.keys(), result))
                for result in content_result]
            return drug_list, "ok", True
        except Exception as e:
            print(e)
            return None, "error", False

    def add_drug(self, name):
        try:
            drug = Drug(name = name)
            db.session.add(drug)
            db.session.commit()
            return drug.id, "ok", True
        except Exception as e:
            print(e)
            return 0, "drug already exists", False

    def update_drug(self, id, name = None):
        try:
            drug = Drug.query.get(id)
            if name:
                drug.name = name
            db.session.commit()
            return drug.id, "ok", True
        except Exception as e:
            print(e)
            return 0, "error", False
