import psycopg2
import psycopg2.extras


class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def get_user(self, login):
        self.__cursor.execute(f"SELECT * FROM worker WHERE login_of_worker = '{login}' ")
        result = self.__cursor.fetchone()
        if not result:
            print("Пользователь не найден")
            return False

        return result
