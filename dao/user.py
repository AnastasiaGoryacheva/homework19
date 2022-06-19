from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).all()

    def get_all(self):
        self.session.query(User).all()

    def create(self, users):
        user = User(**users)
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, req_json):
        user = self.get_one(req_json.get("id"))
        user.username = req_json.get("username")
        user.password = req_json.get("password")
        user.role = req_json.get("role")

        self.session.add(user)
        self.session.commit()

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()
