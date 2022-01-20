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
        user = self.__cursor.fetchone()
        if not user:
            return False
        return user

    def add_user(self, fio, role, login, password):
        self.__cursor.execute("INSERT INTO worker VALUES (%s,%s,%s,%s)", (login, password, fio, role))
        self.__db.commit()

    def get_purpose(self):
        self.__cursor.execute("SELECT * FROM purpose WHERE login_of_worker = %s", (session['role']))
        purposes = self.__cursor.fetchall()
        if not purposes:
            return False
        return purposes

    def add_purpose(self, date_of_purpose, login_of_worker):
        self.__cursor.execute("INSERT INTO purpose(date_of_purpose, login_of_worker) VALUES (%s,%s,%s)",
                              (date_of_purpose, login_of_worker))
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

    def get_task_by_text(self, text):
        self.__cursor.execute("""SELECT id_of_task FROM task WHERE text_of_task = %s""", (text,))
        id_of_task = self.__cursor.fetchone()
        if id_of_task is None:
            return False
        return id_of_task

    def add_task_form(self, text, location, typeoftask):
        # Добавляю в таблицу task
        self.__cursor.execute("INSERT INTO task(text_of_task,id_of_location,id_of_type) VALUES(%s,%s,%s)",
                              (text, location, typeoftask))
        self.__db.commit()

    def add_purpose_comment_form(self, comment, datetime, id_of_task, login):
        # Добавляю в таблицу purpose
        self.__cursor.execute("INSERT INTO purpose VALUES (%s,%s,%s,'1')", (datetime, id_of_task, login))
        self.__db.commit()

        # Добавляю в таблицу comment
        self.__cursor.execute("""INSERT INTO comment_to_task(text_of_comment,datetime_of_comment,id_of_task,
        login_of_worker) VALUES (%s,%s,%s,%s)""", (comment, datetime, id_of_task, login))
        self.__db.commit()

    def get_tasks_manager(self):
        self.__cursor = self.__db.cursor()
        self.__cursor.execute("""SELECT DISTINCT text_of_task,text_of_comment,name_of_status,purpose.login_of_worker,
        date_of_purpose FROM purpose JOIN status ON purpose.id_of_status=status.id_of_status 
        JOIN task ON purpose.id_of_task=task.id_of_task
        JOIN comment_to_task ON purpose.id_of_task=comment_to_task.id_of_task""")
        tasks_manager = self.__cursor.fetchall()
        return tasks_manager

    def get_tasks_executor(self, login):
        self.__cursor = self.__db.cursor()
        self.__cursor.execute("""SELECT DISTINCT text_of_task,text_of_comment,name_of_status,date_of_purpose
        FROM purpose JOIN comment_to_task ON purpose.id_of_task=comment_to_task.id_of_task
        JOIN task ON task.id_of_task=purpose.id_of_task
        JOIN status ON purpose.id_of_status=status.id_of_status WHERE purpose.login_of_worker = %s""", (login,))
        tasks_executor = self.__cursor.fetchall()
        return tasks_executor
