from flask import Blueprint, jsonify, request
from flasgger import swag_from
from app.services import PatientService 

bp = Blueprint(
    'patient',
    __name__,
    template_folder='../templates'
)

service = PatientService()

@bp.route('/patient', methods=['GET'])
@swag_from('get-patient-list.yml')
def get_patient_list():
    '''
    获取患者列表
    '''
    dep = 0 if request.args.get('department') is None else int(request.args.get('department'))
    # todo: 添加department之外的其他的搜索条件

    patients, count, result = service.get_patient_list(dep)
    if result:
        return jsonify({
            'patient': patients,
            'count': count
        }), 200
    else:
        return jsonify({'message': "error"}), 500

@bp.route('/patient/<int:patientId>', methods=['GET'])
@swag_from('get-patient.yml')
def get_patient(patientId):
    '''
    获取患者的完整基本信息
    '''
    patient, result = service.get_patient(patientId)
    if result:
        return jsonify(patient), 200
    else:
        return jsonify({'message': patient}), 500
