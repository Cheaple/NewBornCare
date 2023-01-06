
from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.checkers import (transfusion_add_params_check,
                          transfusion_drug_update_params_check,
                          transfusion_update_params_check)
from app.controllers.access_control import login_required
from app.services import TransfusionService

bp = Blueprint(
    'transfusion',
    __name__,
    template_folder='../templates'
)

service = TransfusionService()


@bp.route('/api/transfusion', methods=['GET'])
@swag_from('transfusion/get-transfusion-list.yml')
@login_required(["admin", "nurse", "patient"])
def get_transfusion_list():
    '''
    获取患者的输液记录列表
    '''
    patientId = request.args.get('patientId')
    transfusions, count, msg, result = service.get_transfusion_list(patientId)
    if result:
        return jsonify({
            'transfusion': transfusions,
            'count': count
        }), 200
    else:
        return jsonify({'message': msg}), 500


@bp.route('/api/transfusion/<int:transfusionId>', methods=['GET'])
@swag_from('transfusion/get-transfusion.yml')
@login_required(["admin", "nurse", "patient"])
def get_transfusion(transfusionId):
    '''
    获取输液记录的完整信息
    '''
    transfusion, msg, result = service.get_transfusion(transfusionId)
    if result:
        return jsonify(transfusion), 200
    else:
        return jsonify({'message': msg}), 500


@bp.route('/api/transfusion/add', methods=['POST'])
@swag_from('transfusion/add-transfusion.yml')
@login_required(["admin", "nurse"])
def add_transfusion():
    """
    添加输液记录
    """
    try:
        content = request.get_json()
        # print(content)
        if content is None:
            return jsonify({'message': "bad arguments"}), 400

        # 参数检查
        key, passed = transfusion_add_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400

        drugs = content['drug']
        del content['drug']
        id, msg, result = service.add_transfusion(content, drugs)

        if result:
            return jsonify({
                'id': id,
                'message': msg
            }), 200
        else:
            return jsonify({'message': msg}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400


@bp.route('/api/transfusion/update/<int:transfusionId>', methods=['PATCH'])
@swag_from('transfusion/update-transfusion.yml')
@login_required(["admin", "nurse"])
def update_transfusion(transfusionId):
    '''
    修改输液记录
    '''
    try:
        content = request.get_json()
        # print(content)
        if content is None:
            return jsonify({'message': "bad arguments"}), 400

        # 参数检查
        key, passed = transfusion_update_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400

        id, msg, result = service.update_transfusion(transfusionId, content)

        if result:
            return jsonify({
                'id': id,
                'message': msg
            }), 200
        else:
            return jsonify({'message': msg}), 500
    except KeyError as e:
        print(e)
        return jsonify({'message': "bad arguments"}), 400


@bp.route(
    '/api/transfusion/update/<int:transfusionId>/<drugSeq>',
    methods=['PATCH'])
@swag_from('transfusion/update-transfusion-drug.yml')
@login_required(["admin", "nurse"])
def update_transfusion_drug(transfusionId, drugSeq):
    '''
    修改输液记录的药物
    '''
    try:
        content = request.get_json()
        # print(content)
        if content is None:
            return jsonify({'message': "bad arguments"}), 400

        # 参数检查
        key, passed = transfusion_drug_update_params_check(content)
        if not passed:
            return jsonify({'message': "invalid arguments: " + key}), 400

        id, msg, result = service.update_transfusion_drug(
            transfusionId, drugSeq, content)

        if result:
            return jsonify({
                'id': id,
                'message': msg
            }), 200
        else:
            return jsonify({'message': msg}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400


@bp.route(
    '/api/transfusion/update/<int:transfusionId>/next',
    methods=['PATCH'])
@swag_from('transfusion/update-transfusion-next.yml')
@login_required(["admin", "nurse"])
def update_transfusion_next(transfusionId):
    '''
    修改输液记录：换药
    '''
    id, msg, result = service.update_transfusion_next(transfusionId)

    if result:
        return jsonify({
            'id': id,
            'message': msg
        }), 200
    else:
        return jsonify({'message': msg}), 500


@bp.route(
    '/api/transfusion/update/<int:transfusionId>/finish',
    methods=['PATCH'])
@swag_from('transfusion/update-transfusion-finish.yml')
@login_required(["admin", "nurse"])
def update_transfusion_finish(transfusionId):
    '''
    修改输液记录：完成输液
    '''
    id, msg, result = service.update_transfusion_finish(transfusionId)

    if result:
        return jsonify({
            'id': id,
            'message': msg
        }), 200
    else:
        return jsonify({'message': msg}), 500


@bp.route('/api/transfusion/delete/<int:transfusionId>', methods=['PATCH'])
@swag_from('transfusion/delete-transfusion.yml')
@login_required(["admin"])
def delete_transfusion(transfusionId):
    '''
    删除输液记录
    '''
    try:
        id, msg, result = service.delete_transfusion(transfusionId)

        if result:
            return jsonify({
                'id': id,
                'message': msg
            }), 200
        else:
            return jsonify({'message': msg}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400
