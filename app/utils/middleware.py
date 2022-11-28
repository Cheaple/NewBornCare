from flask import request, g, current_app

from .jwt import verify

import functools

def jwt_authentication():
    '''
    Verify jwt token at the beginning of each request.
    '''
    g.userType = None
    g.userId = None
    g.userDepartment = None

    token = request.headers.get('Authorization')
    if token:
        payload = verify(token)
        if payload:
            g.userType = payload.get('userType')
            g.userId = payload.get('userId')
            g.userDepartment = payload.get('userDepartment')

def login_required(user = ["admin", "nurse", "patient"]):
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