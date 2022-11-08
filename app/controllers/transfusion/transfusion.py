from flask import Blueprint, jsonify, request
from flasgger import swag_from
from app.services import TransfusionService
from app.utils import toTimestamp
from datetime import datetime

bp = Blueprint(
    'transfusion',
    __name__,
    template_folder='../templates'
)

service = TransfusionService()

@bp.route('/transfusion', methods=['GET'])
@swag_from('get-transfusion-list.yml')
def get_transfusion_list():
    '''
    获取患者的输液列表
    '''
    patientId = request.args.get('patientId')
    transfusions, count, result = service.get_transfusion_list(patientId)
    if result:
        return jsonify({
            'transfusion': transfusions,
            'count': count
        }), 200
    else:
        return jsonify({'message': "error"}), 500

@bp.route('/transfusion/<int:transfusionId>', methods=['GET'])
@swag_from('get-transfusion.yml')
def get_transfusion(transfusionId):
    '''
    获取输液的完整基本信息
    '''
    transfusion, result = service.get_transfusion(transfusionId)
    if result:
        return jsonify(transfusion), 200
    else:
        return jsonify({'message': transfusion}), 500

@bp.route('/transfusion/add', methods=['POST'])
@swag_from('add-transfusion.yml')
def add_transfusion():
    """
    添加患者
    """
    try:
        content = request.get_json()
        print(content)
        if content is None:
            return jsonify({'message': "bad arguments"}), 400

        # TODO: 参数检测
        # key, passed = transfusion_params_check(content)
        # if not passed:
            # return jsonify({'message': "invalid arguments: " + key}), 400
        if 'startTime' not in content:
            content['startTime'] = toTimestamp(datetime.now())
        if 'info' not in content:
            content['info'] = None

        id, result = service.add_transfusion(content)

        if result:
            return jsonify({
                'id': id,
                'message': "ok"
            }), 200
        else:
            return jsonify({'message': "error"}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400