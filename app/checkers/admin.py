import re


def admin_add_params_check(content):
    """
    对 admin 添加请求进行参数检查
    """
    if "username" not in content or re.search(
        r"^(?=.{5,12}$)[a-zA-Z][a-zA-Z_]{0,18}\d{1,19}$",
        content["username"]) is None:
        # ⻓度5-12的字⺟串加数字，且必须包含这两种类型，所有字⺟串必须在数字前⾯，字⺟包括⼤写字⺟和⼩写字⺟
        return "username", False

    if "password" not in content or re.search(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)"
            r"[A-Za-z\d\`\~\!\@\#\$\%\^\&\*\(\)\_\-\+\=\[\]\{\}\\\|\;\:\'\"\,\.\/\<\>\?]{8,15}$",
        content["password"]) is None:
        # ⻓度8-15的字符串，由⼤写、⼩写字⺟、数字和标点符号组成且必须包含前三种类型
        return "password", False

    if "name" not in content or re.search(
        r"^[\u4e00-\u9fa5]{2,10}$",
        content["name"]) is None:
        # 长度为2-10的汉字串
        return "name", False

    if "department" not in content:
        content['department'] = 0

    if 'status' not in content:
        content['status'] = 1

    return "ok", True

def admin_update_params_check(content):
    """
    对 admin 更新请求进行参数检查
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
        r"^[\u4e00-\u9fa5]{2,10}$",
        content["name"]) is None:
        # 长度为2-10的汉字串
        return "name", False

    return "ok", True
