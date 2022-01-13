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

    def add_user(self, fio, role, login, password):
        self.__cursor.execute("INSERT INTO worker VALUES (%s,%s,%s,%s)", (fio, role, login, password))
        self.__db.commit()
