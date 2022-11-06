
from flask import Blueprint, jsonify, request
from flasgger import swag_from
from app.models import Nurse
from app.services import NurseService
from app.utils import encipher, jwt

bp = Blueprint(
    'nurse',
    __name__,
    template_folder='../templates'
)

service = NurseService()


@bp.route('/nurse/login', methods=['POST'])
@swag_from('login.yml')
def login():
    """
    Login
    """
    try:
        content = request.get_json()
        if content is None:
            return jsonify({'message': "bad arguments"}), 400
        nurse, result = service.get_user_with_password(
            content['username'], encipher(content['password']))

        if result:
            token = jwt.generate({
                "user": "admin",
                "id": nurse.id
            })
            return jsonify({
                "jwt": token,
                "id": nurse.id,
                "username": nurse.username,
                "name": nurse.name,
                "gender": nurse.gender,
                "tel": nurse.tel,
                "department": nurse.department
            }), 200
        else:
            return jsonify({'message': nurse}), 500
    except KeyError:
        return jsonify({'message': 'bad arguments'}), 400


@bp.route('/nurse/logout', methods=['PATCH'])
def logout():
    pass


@bp.route('/nurse/patient', methods=['PATCH'])
def patient_list():
    pass
