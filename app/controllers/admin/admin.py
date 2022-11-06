
from flask import Blueprint, jsonify, request
from flasgger import swag_from
from app.models import Admin
from app.services import AdminService
from app.utils import encipher, jwt

bp = Blueprint(
    'admin',
    __name__,
    template_folder='../templates'
)

service = AdminService()


@bp.route('/admin/login', methods=['POST'])
@swag_from('login.yml')
def login():
    """
    Login
    """
    try:
        content = request.get_json()
        if content is None:
            return jsonify({'message': "bad arguments"}), 400
        admin, result = service.get_user_with_password(
            content['username'], encipher(content['password']))

        if result:
            token = jwt.generate({
                "user": "admin",
                "id": admin.id
            })
            return jsonify({
                "jwt": token,                
                "id": admin.id,
                "username": admin.username,
                "name": admin.name,
                "department": admin.department,
            }), 200
        else:
            return jsonify({'message': admin}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400


@bp.route('/admin/logout', methods=['PATCH'])
def logout():
    pass


@bp.route('/admin/staff', methods=['PATCH'])
def staff_list():
    pass


@bp.route('/admin/patient', methods=['PATCH'])
def patient_list():
    pass
