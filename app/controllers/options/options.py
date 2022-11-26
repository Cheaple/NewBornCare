from datetime import datetime

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.services import DepartmentService
from app.utils import toTimestamp
from app.utils.middleware import login_required

bp = Blueprint(
    'options',
    __name__,
    template_folder='../templates'
)

departmentService = DepartmentService()

@bp.route('/api/list', methods=['GET'])
@swag_from('get-department-list.yml')
@login_required(["admin", "nurse"])
def get_department_list():
    '''
    获取科室、静脉、工具、药物表
    '''
    departments, msg, result = departmentService.get_department_list()
    if result:
        return jsonify({
            'department': departments,
        }), 200
    else:
        return jsonify({'message': msg}), 500

@bp.route('/api/list/department', methods=['GET'])
@swag_from('get-department-list.yml')
@login_required(["admin", "nurse", "patient"])
def get_department_list():
    '''
    获取科室列表
    '''
    departments, msg, result = departmentService.get_department_list()
    if result:
        return jsonify({
            'department': departments,
        }), 200
    else:
        return jsonify({'message': msg}), 500

@bp.route('/api/list/department/add', methods=['POST'])
@swag_from('add-department.yml')
@login_required(["admin"])
def add_department():
    '''
    添加科室列表
    '''
    name = request.args.get('name')
    id, msg, result = departmentService.add_department(name)
    if result:
        return jsonify({
            'id': id,
            'message': msg
        }), 200
    else:
        return jsonify({'message': msg}), 500