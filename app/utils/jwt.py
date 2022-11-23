import datetime

import jwt
from flask import current_app, g, request


def generate(payload, expiry=None):
    if expiry is None:
        expire_hours = int(current_app.config.get('JWT_EXPIRY'))
        expiry = datetime.datetime.now()
        + datetime.timedelta(hours=expire_hours)

    _payload = {'exp': expiry}
    _payload.update(payload)
    salt = current_app.config.get('JWT_SALT', '')
    token = jwt.encode(_payload, salt, algorithm='HS256')

    return token.decode()


def verify(token):
    salt = current_app.config.get('JWT_SALT', '')
    try:
        payload = jwt.decode(token, salt, algorithm=['HS256'])
    except jwt.PyJWTError:
        payload = None
    return payload