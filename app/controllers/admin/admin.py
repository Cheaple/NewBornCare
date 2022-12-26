
from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.services import AdminService
from app.utils import jwt

from app.checkers import admin_add_params_check, admin_update_params_check
from app.controllers.access_control import login_required

bp = Blueprint(
    'admin',
    __name__,
    template_folder='../templates'
)

service = AdminService()


@bp.route('/api/admin/login', methods=['POST'])
@swag_from('login.yml')
def login():
    """
    Login
    """
    try:
        content = request.get_json()
        if content is None:
            return jsonify({'message': "bad arguments"}), 400
        admin, msg, result = service.get_user_with_password(
            content['username'], content['password'])

        if result:
            token = jwt.generate({
                "userType": "admin",
                "userId": admin.id,
                "userDepartment": admin.department
            })
            return jsonify({
                "jwt": token,
                "id": admin.id,
                "username": admin.username,
                "name": admin.name,
                "department": admin.department,
            }), 200
        else:
            return jsonify({'message': msg}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400


@bp.route('/api/admin/logout', methods=['PATCH'])
@login_required(["admin"])
def logout():
    pass


@bp.route('/api/admin/add', methods=['POST'])
@swag_from('admin/add-admin.yml')
@login_required(["admin"])
def add_admin():
    """
    添加管理员
    """
    try:
        content = request.get_json()
        # print(content)
        if content is None:
            return jsonify({'message': "bad arguments"}), 400

        # 检查参数
        key, passed = admin_add_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400


        id, msg, result = service.add_admin(content)

        if result:
            return jsonify({
                'id': id,
                'message': msg
            }), 200
        else:
            return jsonify({'message': msg}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400

@bp.route('/api/admin/update/<int:adminId>', methods=['PATCH'])
@swag_from('admin/update-admin.yml')
@login_required(["admin"])
def update_admin(adminId):
    '''
    修改管理员
    '''
    try:
        content = request.get_json()
        # print(content)
        if content is None:
            return jsonify({'message': "bad arguments"}), 400

        # 检查参数
        key, passed = admin_update_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400

        id, msg, result = service.update_admin(adminId, content)

        if result:
            return jsonify({
                'id': id,
                'message': msg
            }), 200
        else:
            return jsonify({'message': msg}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400

@bp.route('/api/admin/delete/<int:adminId>', methods=['PATCH'])
@swag_from('admin/delete-admin.yml')
@login_required(["admin"])
def delete_admin(adminId):
    '''
    修改管理员
    '''
    try:
        content = request.get_json()
        # print(content)
        if content is None:
            return jsonify({'message': "bad arguments"}), 400

        # 检查参数
        key, passed = admin_update_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400

        id, msg, result = service.update_admin(adminId, content)

        if result:
            return jsonify({
                'id': id,
                'message': msg
            }), 200
        else:
            return jsonify({'message': msg}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400
