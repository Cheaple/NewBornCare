
from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.services import NurseService
from app.utils import jwt

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
        nurse, result = service.get_nurse_with_password(
            content['username'], content['password'])

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


@bp.route('/api/nurse/logout', methods=['PATCH'])
def logout():
    pass


@bp.route('/api/nurse', methods=['GET'])
@swag_from('get-nurse-list.yml')
def get_nurse_list():
    '''
    获取护士列表
    '''
    dep = 0 if request.args.get('department') is None else int(
        request.args.get('department'))
    # TODO: 添加department之外的其他的搜索条件

    nurses, count, result = service.get_nurse_list(dep)
    if result:
        return jsonify({
            'nurse': nurses,
            'count': count
        }), 200
    else:
        return jsonify({'message': "error"}), 500


@bp.route('/api/nurse/<int:nurseId>', methods=['GET'])
@swag_from('get-nurse.yml')
def get_nurse(nurseId):
    '''
    获取护士的完整基本信息
    '''
    nurse, result = service.get_nurse(nurseId)
    if result:
        return jsonify(nurse), 200
    else:
        return jsonify({'message': nurse}), 500


@bp.route('/api/nurse/add', methods=['POST'])
@swag_from('add-nurse.yml')
def add_nurse():
    """
    添加护士
    """
    try:
        content = request.get_json()
        print(content)
        if content is None:
            return jsonify({'message': "bad arguments"}), 400

        # TODO: 参数检测
        # key, passed = nurse_params_check(content)
        # if not passed:
            # return jsonify({'message': "invalid arguments: " + key}), 400
        if 'status' not in content:
            content['status'] = 1

        id, result = service.add_nurse(content)

        if result:
            return jsonify({
                'id': id,
                'message': "ok"
            }), 200
        else:
            return jsonify({'message': "username already exists"}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400
