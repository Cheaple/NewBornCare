import re
from datetime import datetime

from app.utils import toTimestamp

from app.services import DrugService

drugService = DrugService()

def transfusion_add_params_check(content):
    """
    对 transfusion 添加请求进行参数检查
    """
    if "nurseId" not in content or type(content["nurseId"]) != int:
        return "nurseId", False
    if "patientId" not in content or type(content["patientId"]) != int:
        return "patientId", False

    if 'name' not in content:
        # example: "葡萄糖，青霉素"
        content['name'] = ', '.join(
            [drugService.get_drug_name(d['drug']) 
            for d in content['drug']]
        )
    if 'startTime' not in content:
        content['startTime'] = toTimestamp(datetime.now())
    elif type(content["startTime"]) != int:
        return 'startTime', False

    if "vein" not in content or type(content["vein"]) != int:
        return "vein", False
    if "tool" not in content or type(content["tool"]) != int:
        return "tool", False
    if "info" not in content:
        content["info"] = None

    if "drug" not in content or (type(content["drug"])) != list:
        return "drug", False
    else:
        for d in content["drug"]:
            if "seq" not in d or type(d["seq"]) != int:
                return "drug seq", False
            if "drug" not in d or type(d["drug"]) != int:
                return "drug drug", False
            if "dose" not in d or type(d["dose"]) != int:
                return "drug dose", False
            if "rate" not in d or type(d["rate"]) != int:
                return "drug rate", False
            if "startTime" not in d:
                d["startTime"] = None
            elif type(d["startTime"]) != int:
                return 'startTime', False
            if "status" not in d:
                # 0：已完成  1：进行中  2：未开始  -1：中止
                d["status"] = 2
            
    content['drugCnt'] = len(content['drug'])
    
    # 开始第一个药品
    if "status" not in content:
        content['status'] = 1  
        content['drug'][0]['status'] = 1
        content['drug'][0]['startTime'] = toTimestamp(datetime.now())
    
    return "ok", True

def transfusion_update_params_check(content):
    """
    对 transfusion 更新请求进行参数检查
    """
    if 'startTime' in content and type(content["startTime"]) != int:
        return 'startTime', False
    if 'finishTime' in content and type(content["finishTime"]) != int:
        return 'finishTime', False
    if "vein" in content and type(content["vein"]) != int:
        return "vein", False
    if "tool" in content and type(content["tool"]) != int:
        return "tool", False
    if "status" in content and (
        type(content["status"]) != int or content["status"] < -1):
        return "status", False

    return "ok", True

def transfusion_drug_update_params_check(d):
    """
    对 transfusion 的某个 drug 的更新请求进行参数检查
    """
    if "seq" in d and type(d["seq"]) != int:
        return "drug seq", False
    if "drug" in d and type(d["drug"]) != int:
        return "drug drug", False
    if "dose" in d and type(d["dose"]) != int:
        return "drug dose", False
    if "rate" in d and type(d["rate"]) != int:
        return "drug rate", False
    if "startTime" in d and type(d["startTime"]) != int:
        return 'startTime', False
    if "status" in d and d["status"] not in [-1, 0, 1, 2]:
        # 0：已完成  1：进行中  2：未开始  -1：中止
        return 'status', False

    return "ok", True
