import re


def nurse_add_params_check(content):
    """
    对 nurse 添加请求进行参数检查
    """
    if "username" not in content or re.search(
        r"^(?=.{5,12}$)[a-zA-Z][a-zA-Z_]{0,18}\d{1,19}$",
        content["username"]) is None:
        # ⻓度5-12的字⺟串加数字，且必须包含这两种类型，所有字⺟串必须在数字前⾯，字⺟包括⼤写字⺟和⼩写字⺟
        return "username", False

    if "password" not in content or re.search(
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

    if "tel" not in content or re.search(
        r"^\d{11}$", str(content["tel"])) is None:
        # 11位手机号
        return "tel", False
    else:
        content["tel"] = int(content["tel"])

    if "department" not in content:
        content['department'] = 0
    elif str.isdigit(str(content["department"])) is False:
        # 数字
        return "department", False
    
    content['status'] = 1

    return "ok", True

def nurse_update_params_check(content):
    """
    对 nurse 更新请求进行参数检查
    """
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

    if "tel" in content and re.search(
        r"^\d{11}$", str(content["tel"])) is None:
        # 11位手机号
        return "tel", False

    if "department" in content and str.isdigit(str(content["department"])) is False:
        # 数字
        return "department", False

    if "status" in content and str.isdigit(str(content["status"])) is False:
        # 数字
        return "status", False

    return "ok", True
