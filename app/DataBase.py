import psycopg2
import psycopg2.extras
from flask import session


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

    def get_purpose(self):
        self.__cursor.execute("SELECT * FROM purpose WHERE login_of_worker = %s", (session['role']))
        purposes = self.__cursor.fetchall()
        if not purposes:
            print("Указаний нет")
            return False

        return purposes

    def add_purpose(self, date_of_purpose, login_of_worker):
        self.__cursor.execute("INSERT INTO purpose(date_of_purpose, login_of_worker) VALUES (%s,%s,%s)", (date_of_purpose, login_of_worker))
        self.__db.commit()

    def get_all_users(self, db):
        self.__cursor = db.cursor()
        self.__cursor.execute("SELECT login_of_worker FROM worker WHERE role_of_worker = 'executor'")
