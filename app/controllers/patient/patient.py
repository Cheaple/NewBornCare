from datetime import datetime

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.services import PatientService
from app.utils import toTimestamp

bp = Blueprint(
    'patient',
    __name__,
    template_folder='../templates'
)

service = PatientService()


@bp.route('/api/patient', methods=['GET'])
@swag_from('get-patient-list.yml')
def get_patient_list():
    '''
    获取患者列表
    '''
    dep = 0 if request.args.get('department') is None else int(
        request.args.get('department'))
    # TODO: 添加department之外的其他的搜索条件

    patients, count, msg, result = service.get_patient_list(dep)
    if result:
        return jsonify({
            'patient': patients,
            'count': count
        }), 200
    else:
        return jsonify({'message': msg}), 500


@bp.route('/api/patient/<int:patientId>', methods=['GET'])
@swag_from('get-patient.yml')
def get_patient(patientId):
    '''
    获取患者的完整基本信息
    '''
    patient, msg, result = service.get_patient(patientId)
    if result:
        return jsonify(patient), 200
    else:
        return jsonify({'message': msg}), 500


@bp.route('/api/patient/add', methods=['POST'])
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

        id, msg, result = service.add_patient(content)

        if result:
            return jsonify({
                'id': id,
                'message': msg
            }), 200
        else:
            return jsonify({'message': msg}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400

@bp.route('/api/patient/update/<int:patientId>', methods=['PATCH'])
@swag_from('update-patient.yml')
def update_patient(patientId):
    '''
    修改护士
    '''
    try:
        content = request.get_json()
        # print(content)
        if content is None:
            return jsonify({'message': "bad arguments"}), 400

        # TODO: 参数检测
        # key, passed = patient_params_check(content)
        # if not passed:
            # return jsonify({'message': "invalid arguments: " + key}), 400

        id, msg, result = service.update_patient(patientId, content)

        if result:
            return jsonify({
                'id': id,
                'message': msg
            }), 200
        else:
            return jsonify({'message': msg}), 500
    except KeyError:
        return jsonify({'message': "bad arguments"}), 400