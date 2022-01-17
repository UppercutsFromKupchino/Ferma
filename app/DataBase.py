import psycopg2
import psycopg2.extras
import psycopg2.errors
from flask import session


class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def get_user(self, login):
        self.__cursor.execute(f"SELECT * FROM worker WHERE login_of_worker = '{login}' ")
        result = self.__cursor.fetchone()
        if not result:
            return False

        return result

    def add_user(self, fio, role, login, password):
        self.__cursor.execute("INSERT INTO worker VALUES (%s,%s,%s,%s)", (fio, role, login, password))
        self.__db.commit()

    def get_purpose(self):
        self.__cursor.execute("SELECT * FROM purpose WHERE login_of_worker = %s", (session['role']))
        purposes = self.__cursor.fetchall()
        if not purposes:
            return False

        return purposes

    def add_purpose(self, date_of_purpose, login_of_worker):
        self.__cursor.execute("INSERT INTO purpose(date_of_purpose, login_of_worker) VALUES (%s,%s,%s)", (date_of_purpose, login_of_worker))
        self.__db.commit()

    def get_all_users(self):
        self.__cursor = self.__db.cursor()
        self.__cursor.execute("SELECT login_of_worker FROM worker WHERE name_of_role = 'executor'")
        workers_executors = self.__cursor.fetchall()

        return workers_executors

    def get_all_locations(self):
        self.__cursor = self.__db.cursor()
        self.__cursor.execute("SELECT name_of_location FROM location_of_task")
        locations = self.__cursor.fetchall()

        return locations

    def get_all_types(self):
        self.__cursor = self.__db.cursor()
        self.__cursor.execute("SELECT type_of_task_ FROM type_of_task")
        types_of_task = self.__cursor.fetchall()

        return types_of_task

    def adding_task_form(self, login, text, location, typeoftask, datetime, comment):
        try:
            # Добавляю в таблицу task
            self.__cursor.execute(
                "INSERT INTO task(text_of_task,id_of_location,id_of_type,id_of_status) VALUES(%s,%s,%s,'1')",
                (text, location, typeoftask))
            self.__db.commit()

            # Ищу максимальное значение id в таблице task
            self.__cursor.execute("SELECT MAX(id_of_task) FROM task")
            max_id_of_task = self.__cursor.fetchone()
            if not max_id_of_task:
                max_id_of_task = 1

            # Добавляю в таблицу purpose
            self.__cursor.execute("INSERT INTO purpose VALUES (%s,%s,%s)", (datetime, max_id_of_task, login))
            self.__db.commit()

            # Добавляю в таблицу comment
            self.__cursor.execute("INSERT INTO comment_to_task(text_of_comment,datetime_of_comment,id_of_task,login_of_worker) VALUES (%s,%s,%s,%s)",
                                  (comment, datetime, max_id_of_task, login))
            self.__db.commit()
        except:
            self.__db.rollback()

    def show_tasks(self):
        self.__cursor.execute("SELECT ")
