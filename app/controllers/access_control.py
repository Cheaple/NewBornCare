import functools

from flask import current_app, g


def login_required(user=["admin", "nurse", "patient"]):
    """
    用户必须登录装饰器
    """
    def login(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if current_app.config.get('TYPE') == "dev":
                return func(*args, **kwargs)
            if not g.userId:
                return {'message': 'Unauthorized'}, 401
            if g.userType not in user:
                return {'message': 'Forbidden'}, 403
            else:
                return func(*args, **kwargs)
        wrapper.__name__ = "warper" + func.__name__
        return wrapper
    return login
