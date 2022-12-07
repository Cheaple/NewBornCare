
from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.services import NurseService
from app.utils import jwt
from app.checkers import nurse_add_params_check, nurse_update_params_check
from app.controllers.access_control import login_required

bp = Blueprint(
    'nurse',
    __name__,
    template_folder='../templates'
)

service = NurseService()


@bp.route('/api/nurse/login', methods=['POST'])
@swag_from('login.yml')
def login():
    """
    Login
    """
    try:
        content = request.get_json()
        if content is None:
            return jsonify({'message': "bad arguments"}), 400
        nurse, msg, result = service.get_nurse_with_password(
            content['username'], content['password'])

        if result:
            token = jwt.generate({
                "userType": "nurse",
                "userId": nurse.id,
                "userDepartment": nurse.department
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
            return jsonify({'message': msg}), 500
    except KeyError:
        return jsonify({'message': 'bad arguments'}), 400


@bp.route('/api/nurse/logout', methods=['PATCH'])
@login_required(["nurse"])
def logout():
    pass


@bp.route('/api/nurse', methods=['GET'])
@swag_from('nurse/get-nurse-list.yml')
@login_required(["admin", "nurse"])
def get_nurse_list():
    '''
    获取护士列表
    '''
    dep = 0 if request.args.get('department') is None else int(
        request.args.get('department'))
    # TODO: 添加department之外的其他的搜索条件

    nurses, count, msg, result = service.get_nurse_list(dep)
    if result:
        return jsonify({
            'nurse': nurses,
            'count': count
        }), 200
    else:
        return jsonify({'message': msg}), 500


@bp.route('/api/nurse/<int:nurseId>', methods=['GET'])
@swag_from('nurse/get-nurse.yml')
@login_required(["admin", "nurse"])
def get_nurse(nurseId):
    '''
    获取护士的完整基本信息
    '''
    nurse, msg, result = service.get_nurse(nurseId)
    if result:
        return jsonify(nurse), 200
    else:
        return jsonify({'message': msg}), 500


@bp.route('/api/nurse/add', methods=['POST'])
@swag_from('nurse/add-nurse.yml')
@login_required(["admin", "nurse"])
def add_nurse():
    """
    添加护士
    """
    try:
        content = request.get_json()
        # print(content)
        if content is None:
            return jsonify({'message': "bad arguments"}), 400

        # 检查参数
        key, passed = nurse_add_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400

        id, msg, result = service.add_nurse(content)

        if result:
            return jsonify({
                'id': id,
                'message': msg
            }), 200
        else:
            return jsonify({'message': msg}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400

@bp.route('/api/nurse/update/<int:nurseId>', methods=['PATCH'])
@swag_from('nurse/update-nurse.yml')
@login_required(["admin", "nurse"])
def update_nurse(nurseId):
    '''
    修改护士
    '''
    try:
        content = request.get_json()
        # print(content)
        if content is None:
            return jsonify({'message': "bad arguments"}), 400

        # 检查参数
        key, passed = nurse_update_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400

        id, msg, result = service.update_nurse(nurseId, content)

        if result:
            return jsonify({
                'id': id,
                'message': msg
            }), 200
        else:
            return jsonify({'message': msg}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400
