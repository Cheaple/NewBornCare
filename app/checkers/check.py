import re
from datetime import datetime

from app.utils import toTimestamp

def check_add_params_check(content):
    """
    对 check 添加请求进行参数检查
    """
    if "nurseId" not in content or type(content["nurseId"]) != int:
        return "nurseId", False
    if "patientId" not in content or type(content["patientId"]) != int:
        return "patientId", False
    if "transfusionId" not in content:
        content["transfusionId"] = None
    elif type(content["transfusionId"]) != int:
        return "transfusionId", False
    if 'time' not in content:
        content['time'] = toTimestamp(datetime.now())
    elif type(content["time"]) != int:
        return 'time', False

    if "info" not in content:
        content["info"] = None
    
    return "ok", True

def check_update_params_check(content):
    """
    对 check 更新请求进行参数检查
    """
    if "time" in content and type(content["time"]) != int:
        return 'time', False

    return "ok", True
