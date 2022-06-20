import jwt
import calendar
import datetime

from flask_restx import abort

from config import Config
from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService, config: Config):
        self.user_service = user_service
        self.config = config

    def generate_tokens(self, username, password, is_refresh=False):
        user = self.user_service.get_by_username(username)
        user = user[0]
        if user is None:
            raise abort(404)
        if not is_refresh:
            if not self.user_service.compare_password(user.password, password):
                abort(400)

        info = {
            'username': user.username,
            'role': user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        info['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(info, Config.SECRET_HERE, algorithm=Config.ALGORITHM)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        info['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(info, Config.SECRET_HERE, algorithm=Config.ALGORITHM)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(refresh_token, Config.SECRET_HERE, Config.ALGORITHM)
        username = data.get('username')

        return self.generate_tokens(username, None, is_refresh=True)
