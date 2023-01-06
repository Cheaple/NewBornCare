
from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.controllers.access_control import login_required
from app.services import VeinService

bp = Blueprint(
    'vein',
    __name__,
    template_folder='../templates'
)

veinService = VeinService()


@bp.route('/api/list/vein', methods=['GET'])
@swag_from('options/get-vein-list.yml')
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
@swag_from('options/add-vein.yml')
@login_required(["admin"])
def add_vein():
    '''
    添加科室
    '''
    content = request.get_json()
    id, msg, result = veinService.add_vein(content["name"])
    if result:
        return jsonify({
            'id': id,
            'message': msg
        }), 200
    else:
        return jsonify({'message': msg}), 500


@bp.route('/api/list/vein/update/<int:veinId>', methods=['PATCH'])
@swag_from('options/update-vein.yml')
@login_required(["admin"])
def update_vein(veinId):
    '''
    更新科室
    '''
    content = request.get_json()
    id, msg, result = veinService.update_vein(veinId, content["name"])
    if result:
        return jsonify({
            'id': id,
            'message': msg
        }), 200
    else:
        return jsonify({'message': msg}), 500


@bp.route('/api/list/vein/delete/<int:veinId>', methods=['PATCH'])
@swag_from('options/delete-vein.yml')
@login_required(["admin"])
def delete_vein(veinId):
    '''
    删除科室
    '''
    try:
        id, msg, result = veinService.delete_vein(veinId)

        if result:
            return jsonify({
                'id': id,
                'message': msg
            }), 200
        else:
            return jsonify({'message': msg}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400
