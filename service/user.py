import base64
import hashlib
import hmac

from dao.user import UserDAO
from config import Config


class UserService:
    def __init__(self, dao: UserDAO, config: Config):
        self.dao = dao
        self.config = config

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def get_all(self):
        return self.dao.get_all()

    def create(self, new_user):
        new_user['password'] = self.get_pass_hash(new_user['password'])
        return self.dao.create(new_user)

    def update(self, req_json):
        self.dao.update(req_json)

    def delete(self, uid):
        self.dao.delete(uid)

    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            self.config.PWD_HASH_SALT,
            self.config.PWD_HASH_ITERATIONS
        )

    def get_pass_hash(self, password):
        pass_hash = self.get_hash(password)
        b64_hash = self.encode_base64(pass_hash)
        return b64_hash

    def encode_base64(self, data):
        return base64.b64encode(data)

    def decode_base64(self, data):
        return base64.b64decode(data)

    def compare_password(self, password_hash, password) -> bool:
        db_bass_decode = self.decode_base64(password_hash)
        try_password_hash = self.get_hash(password)
        return hmac.compare_digest(db_bass_decode, try_password_hash)
