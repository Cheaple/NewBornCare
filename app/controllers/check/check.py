
from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.checkers import check_add_params_check, check_update_params_check
from app.controllers.access_control import login_required
from app.services import CheckService

bp = Blueprint(
    'check',
    __name__,
    template_folder='../templates'
)

service = CheckService()


@bp.route('/api/check', methods=['GET'])
@swag_from('check/get-check-list.yml')
@login_required(["admin", "nurse", "patient"])
def get_check_list():
    '''
    获取某个患者或某次输液记录的巡视记录列表
    '''
    patientId = request.args.get('patientId')
    transfusionId = request.args.get('transfusionId')
    checks, count, msg, result = service.get_check_list(
        patientId=patientId, transfusionId=transfusionId)
    if result:
        return jsonify({
            'check': checks,
            'count': count
        }), 200
    else:
        return jsonify({'message': msg}), 500


@bp.route('/api/check/<int:checkId>', methods=['GET'])
@swag_from('check/get-check.yml')
@login_required(["admin", "nurse", "patient"])
def get_check(checkId):
    '''
    获取巡视记录的完整信息
    '''
    check, msg, result = service.get_check(checkId)
    if result:
        return jsonify(check), 200
    else:
        return jsonify({'message': msg}), 500


@bp.route('/api/check/add', methods=['POST'])
@swag_from('check/add-check.yml')
@login_required(["admin", "nurse"])
def add_check():
    """
    添加输液记录
    """
    try:
        content = request.get_json()
        # print(content)
        if content is None:
            return jsonify({'message': "bad arguments"}), 400

        # 参数检测
        key, passed = check_add_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400

        id, msg, result = service.add_check(content)

        if result:
            return jsonify({
                'id': id,
                'message': msg
            }), 200
        else:
            return jsonify({'message': msg}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400


@bp.route('/api/check/update/<int:checkId>', methods=['PATCH'])
@swag_from('check/update-check.yml')
@login_required(["admin", "nurse"])
def update_check(checkId):
    '''
    修改巡视记录
    '''
    try:
        content = request.get_json()
        # print(content)
        if content is None:
            return jsonify({'message': "bad arguments"}), 400

        key, passed = check_update_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400

        id, msg, result = service.update_check(checkId, content)

        if result:
            return jsonify({
                'id': id,
                'message': msg
            }), 200
        else:
            return jsonify({'message': msg}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400


@bp.route('/api/check/delete/<int:checkId>', methods=['PATCH'])
@swag_from('check/delete-check.yml')
@login_required(["admin"])
def delete_check(checkId):
    '''
    删除巡视记录
    '''
    try:
        id, msg, result = service.delete_check(checkId)

        if result:
            return jsonify({
                'id': id,
                'message': msg
            }), 200
        else:
            return jsonify({'message': msg}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400
