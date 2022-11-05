import base64

import scrypt
from flask import current_app


def encipher(text):
    salt = current_app.config.get('SALT', '')
    key = scrypt.hash(text, salt, 32768, 8, 1, 32)
    return base64.b64encode(key).decode("ascii")
