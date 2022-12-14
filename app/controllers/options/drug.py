from datetime import datetime

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.services import DrugService
from app.controllers.access_control import login_required

bp = Blueprint(
    'drug',
    __name__,
    template_folder='../templates'
)

drugService = DrugService()


@bp.route('/api/list/drug', methods=['GET'])
@swag_from('options/get-drug-list.yml')
@login_required(["admin", "nurse", "patient"])
def get_drug_list():
    '''
    获取科室列表
    '''
    drugs, msg, result = drugService.get_drug_list()
    if result:
        return jsonify(drugs), 200
    else:
        return jsonify({'message': msg}), 500

@bp.route('/api/list/drug/add', methods=['POST'])
@swag_from('options/add-drug.yml')
@login_required(["admin"])
def add_drug():
    '''
    添加科室
    '''
    content = request.get_json()
    id, msg, result = drugService.add_drug(content["name"])
    if result:
        return jsonify({
            'id': id,
            'message': msg
        }), 200
    else:
        return jsonify({'message': msg}), 500

@bp.route('/api/list/drug/update/<int:drugId>', methods=['PATCH'])
@swag_from('options/update-drug.yml')
@login_required(["admin"])
def update_drug(drugId):
    '''
    更新科室
    '''
    content = request.get_json()
    id, msg, result = drugService.update_drug(drugId, content["name"])
    if result:
        return jsonify({
            'id': id,
            'message': msg
        }), 200
    else:
        return jsonify({'message': msg}), 500