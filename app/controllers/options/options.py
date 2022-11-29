from datetime import datetime

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.services import DepartmentService, VeinService, ToolService, DrugService

from app.controllers.access_control import login_required

bp = Blueprint(
    'options',
    __name__,
    template_folder='../templates'
)

departmentService = DepartmentService()
veinService = VeinService()
toolService = ToolService()
drugService = DrugService()

@bp.route('/api/list', methods=['GET'])
@swag_from('options/get-list.yml')
@login_required(["admin", "nurse"])
def get_list():
    '''
    获取科室、静脉、工具、药物表
    '''
    departments, msg, result = departmentService.get_department_list()
    

    return jsonify({
        'department': departments,
    }), 200