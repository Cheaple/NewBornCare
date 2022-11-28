from datetime import datetime

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.services import VeinService
from app.utils.middleware import login_required

bp = Blueprint(
    'vein',
    __name__,
    template_folder='../templates'
)

veinService = VeinService()


@bp.route('/api/list/vein', methods=['GET'])
@swag_from('get-vein-list.yml')
@login_required(["admin", "nurse", "patient"])
def get_vein_list():
    '''
    获取科室列表
    '''
    veins, msg, result = veinService.get_vein_list()
    if result:
        return jsonify(veins), 200
    else:
        return jsonify({'message': msg}), 500

@bp.route('/api/list/vein/add', methods=['POST'])
@swag_from('add-vein.yml')
@login_required(["admin"])
def add_vein():
    '''
    添加科室
    '''
    content = request.form.to_dict()
    id, msg, result = veinService.add_vein(content["name"])
    if result:
        return jsonify({
            'id': id,
            'message': msg
        }), 200
    else:
        return jsonify({'message': msg}), 500

@bp.route('/api/list/vein/update/<int:veinId>', methods=['PATCH'])
@swag_from('update-vein.yml')
@login_required(["admin"])
def update_vein(veinId):
    '''
    更新科室
    '''
    content = request.form.to_dict()
    id, msg, result = veinService.update_vein(veinId, content["name"])
    if result:
        return jsonify({
            'id': id,
            'message': msg
        }), 200
    else:
        return jsonify({'message': msg}), 500