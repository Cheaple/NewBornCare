from datetime import datetime

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.services import DepartmentService
from app.controllers.access_control import login_required

bp = Blueprint(
    'department',
    __name__,
    template_folder='../templates'
)

departmentService = DepartmentService()


@bp.route('/api/list/department', methods=['GET'])
@swag_from('options/get-department-list.yml')
@login_required(["admin", "nurse", "patient"])
def get_department_list():
    '''
    获取科室列表
    '''
    departments, msg, result = departmentService.get_department_list()
    if result:
        return jsonify(departments), 200
    else:
        return jsonify({'message': msg}), 500

@bp.route('/api/list/department/add', methods=['POST'])
@swag_from('options/add-department.yml')
@login_required(["admin"])
def add_department():
    '''
    添加科室
    '''
    content = request.form.to_dict()
    id, msg, result = departmentService.add_department(content["name"])
    if result:
        return jsonify({
            'id': id,
            'message': msg
        }), 200
    else:
        return jsonify({'message': msg}), 500

@bp.route('/api/list/department/update/<int:departmentId>', methods=['PATCH'])
@swag_from('options/update-department.yml')
@login_required(["admin"])
def update_department(departmentId):
    '''
    更新科室
    '''
    content = request.form.to_dict()
    id, msg, result = departmentService.update_department(departmentId, content["name"])
    if result:
        return jsonify({
            'id': id,
            'message': msg
        }), 200
    else:
        return jsonify({'message': msg}), 500