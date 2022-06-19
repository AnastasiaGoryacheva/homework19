import jwt
from flask import request
from flask_restx import abort

from config import Config


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer')[-1]

        try:
            jwt.decode(token, Config.SECRET_HERE, Config.ALGORITHM)
        except Exception as e:
            print('JWT decode Exception', e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(jwt=None, *args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer')[-1]
        role = None

        try:
            user = jwt.decode(token, Config.SECRET_HERE, Config.ALGORITHM)
            role = user.get('role', 'user')
        except Exception as e:
            print('JWT decode Exception', e)

        if role != 'admin':
            abort(403)

        return func(*args, **kwargs)

    return wrapper
