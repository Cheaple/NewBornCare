from datetime import datetime

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.services import CheckService
from app.utils import toTimestamp

bp = Blueprint(
    'check',
    __name__,
    template_folder='../templates'
)

service = CheckService()


@bp.route('/api/check', methods=['GET'])
@swag_from('get-check-list.yml')
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
@swag_from('get-check.yml')
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
@swag_from('add-check.yml')
def add_check():
    """
    添加输液记录
    """
    try:
        content = request.get_json()
        print(content)
        if content is None:
            return jsonify({'message': "bad arguments"}), 400

        # TODO: 参数检测
        # key, passed = check_params_check(content)
        # if not passed:
            # return jsonify({'message': "invalid arguments: " + key}), 400
        if 'time' not in content:
            content['time'] = toTimestamp(datetime.now())
        if 'info' not in content:
            content['info'] = None

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
@swag_from('update-check.yml')
def update_check(checkId):
    '''
    修改护士
    '''
    try:
        content = request.get_json()
        # print(content)
        if content is None:
            return jsonify({'message': "bad arguments"}), 400

        # TODO: 参数检测
        # key, passed = check_params_check(content)
        # if not passed:
            # return jsonify({'message': "invalid arguments: " + key}), 400

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