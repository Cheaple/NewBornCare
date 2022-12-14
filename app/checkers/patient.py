import re
from datetime import datetime
from app.utils import toTimestamp

def patient_add_params_check(content):
    """
    对 patient 添加请求进行参数检查
    """

    """基本信息"""
    if "username" in content and re.search(
        r"^(?=.{5,12}$)[a-zA-Z][a-zA-Z_]{0,18}\d{1,19}$",
        content["username"]) is None:
        # ⻓度5-12的字⺟串加数字，且必须包含这两种类型，所有字⺟串必须在数字前⾯，字⺟包括⼤写字⺟和⼩写字⺟
        return "username", False

    if "password" in content and re.search(
        r"^(?=.*[a-zA-Z])(?=.*\d)"
            r"[A-Za-z\d\`\~\!\@\#\$\%\^\&\*\(\)\_\-\+\=\[\]\{\}\\\|\;\:\'\"\,\.\/\<\>\?]{8,15}$",
        content["password"]) is None:
        # ⻓度8-15的字符串，由⼤写、⼩写字⺟、数字和标点符号组成且必须包含前三种类型
        return "password", False

    if "name" not in content or re.search(
        r"^[A-Za-z\d\u4e00-\u9fa5]{2,10}$",
        content["name"]) is None:
        # 长度为2-10的汉字串
        return "name", False

    if "gender" not in content:
        content['gender'] = 2  # 默认为女性
    elif content['gender'] not in [0, 1, 2]:
        return "gender", False

    if 'birthdate' not in content:
        content['birthdate'] = toTimestamp(datetime.now())
    elif str.isdigit(str(content["birthdate"])) is False:
        # 数字
        return "birthdate", False


    """监护人"""
    if "guardian" not in content or re.search(
        r"^[A-Za-z\d\u4e00-\u9fa5]{2,10}$",
        content["guardian"]
    ) is None:
        return "guardian", False

    if "guardianId" not in content:
        return "guardianId", False

    if "relation" not in content or str.isdigit(str(content["relation"])) is False:
        # 数字
        return "relation", False

    if "tel" not in content or re.search(
        r"^\d{11}$", str(content["tel"])) is None:
        # 11位手机号
        return "tel", False
    else:
        content["tel"] = int(content["tel"])


    """住院信息"""
    content['status'] = 1

    if "department" not in content:
        content['department'] = 0
    elif str.isdigit(str(content["department"])) is False:
        # 数字
        return "department", False
    
    if 'inDate' not in content:
        content['inDate'] = toTimestamp(datetime.now())
    elif str.isdigit(str(content["inDate"])) is False:
        # 数字
        return "inDate", False
    
    if 'room' not in content:
        content['room'] = None
    elif str.isdigit(str(content["room"])) is False:
        # 数字
        return "room", False
    
    if 'bed' not in content:
        content['bed'] = None
    elif str.isdigit(str(content["bed"])) is False:
        # 数字
        return "bed", False
    
    if 'allergy' not in content:
        content['allergy'] = None

    return "ok", True



def patient_update_params_check(content):
    """
    对 patient 更新请求进行参数检查
    """

    """基本信息"""
    if "username" in content and re.search(
        r"^(?=.{5,12}$)[a-zA-Z][a-zA-Z_]{0,18}\d{1,19}$",
            content["username"]) is None:
        # ⻓度5-12的字⺟串加数字，且必须包含这两种类型，所有字⺟串必须在数字前⾯，字⺟包括⼤写字⺟和⼩写字⺟
        return "username", False

    if "password" in content and re.search(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)"
            r"[A-Za-z\d\`\~\!\@\#\$\%\^\&\*\(\)\_\-\+\=\[\]\{\}\\\|\;\:\'\"\,\.\/\<\>\?]{8,15}$",
        content["password"]) is None:
        # ⻓度8-15的字符串，由⼤写、⼩写字⺟、数字和标点符号组成且必须包含前三种类型
        return "password", False

    if "name" in content and re.search(
        r"^[A-Za-z\d\u4e00-\u9fa5]{2,10}$",
        content["name"]) is None:
        # 长度为2-10的汉字串
        return "name", False
    
    if "gender" in content and content['gender'] not in [0, 1, 2]:
        return "gender", False

    if 'birthdate' in content and str.isdigit(str(content["birthdate"])) is False:
        # 数字
        return "birthdate", False


    """监护人"""
    if "guardian" in content and re.search(
        r"^[A-Za-z\d\u4e00-\u9fa5]{2,10}$",
        content["guardian"]
    ) is None:
        return "guardian", False

    if "relation" in content and str.isdigit(str(content["relation"])) is False:
        # 数字
        return "relation", False

    if "tel" in content and re.search(
        r"^\d{11}$", str(content["tel"])) is None:
        # 11位手机号
        return "tel", False


    """住院信息"""
    if "status" in content and str.isdigit(str(content["status"])) is False:
        # 数字
        return "status", False

    if "department" in content and str.isdigit(str(content["department"])) is False:
        # 数字
        return "department", False

    if 'inDate' in content and str.isdigit(str(content["inDate"])) is False:
        # 数字
        return "inDate", False

    if 'outDate' in content and str.isdigit(str(content["outDate"])) is False:
        # 数字
        return "outDate", False
    
    if 'room' in content and str.isdigit(str(content["room"])) is False:
        # 数字
        return "room", False
    
    if 'bed' in content and str.isdigit(str(content["bed"])) is False:
        # 数字
        return "bed", False
    

    return "ok", True
