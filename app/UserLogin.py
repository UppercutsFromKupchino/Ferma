from flask_login import UserMixin


class UserLogin(UserMixin):

    def from_db(self, user_id, dbase):
        self.__user = dbase.get_user(user_id)

    def from_db(self, user_id, db):
        self.__user = db.get_user(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['login_of_worker'])
