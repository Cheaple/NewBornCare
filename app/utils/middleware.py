from flask import g, request

from .jwt import verify


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
