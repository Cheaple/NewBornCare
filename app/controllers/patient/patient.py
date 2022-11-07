from flask import Blueprint, jsonify, request
from flasgger import swag_from
from app.services import PatientService
from app.utils import toTimestamp
from datetime import datetime

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
    # TODO: 添加department之外的其他的搜索条件

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

@bp.route('/patient/add', methods=['POST'])
@swag_from('add-patient.yml')
def add_patient():
    """
    添加患者
    """
    try:
        content = request.get_json()
        print(content)
        if content is None:
            return jsonify({'message': "bad arguments"}), 400

        # TODO: 参数检测
        # key, passed = patient_params_check(content)
        # if not passed:
            # return jsonify({'message': "invalid arguments: " + key}), 400
        if 'status' not in content:
            content['status'] = 1
        if 'inDate' not in content:
            content['inDate'] = toTimestamp(datetime.now())
        if 'room' not in content:
            content['room'] = None
        if 'bed' not in content:
            content['bed'] = None
        if 'allergy' not in content:
            content['allergy'] = None

        id, result = service.add_patient(content)

        if result:
            return jsonify({
                'id': id,
                'message': "ok"
            }), 200
        else:
            return jsonify({'message': "error"}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400