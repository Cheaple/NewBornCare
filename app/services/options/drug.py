
from app.extensions import db
from app.models import Drug


class DrugService():
    def get_drug_list(self):
        try:
            content_result = db.session.query(
                Drug.id,
                Drug.name,
            ).filter(Drug.ifExist == True).all()
            drug_list = [dict(zip(result.keys(), result))
                         for result in content_result]
            return drug_list, "ok", True
        except Exception as e:
            print(e)
            return None, "error", False

    def get_drug_name(self, id):
        try:
            drug = Drug.query.filter(Drug.id == id).first()
            if drug is None:
                return None
            return drug.name
        except Exception as e:
            print(e)
            return None

    def add_drug(self, name):
        try:
            drug = Drug(name=name)
            db.session.add(drug)
            db.session.commit()
            return drug.id, "ok", True
        except Exception as e:
            print(e)
            return 0, "drug already exists", False

    def update_drug(self, id, name=None):
        try:
            drug = Drug.query.get(id)
            if name:
                drug.name = name
            db.session.commit()
            return drug.id, "ok", True
        except Exception as e:
            print(e)
            return 0, "error", False

    def delete_drug(self, id):
        try:
            drug = Drug.query.get(id)
            if drug is None:
                return 0, "Drug not found", False

            drug.ifExist = False

            db.session.commit()
            return drug.id, "ok delete drug", True
        except Exception as e:
            print(e)
            return 0, "error", False
