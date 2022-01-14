from app import app
from flask import render_template, redirect, request, url_for, g, flash, session
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app.UserLogin import UserLogin
from app.DataBase import DataBase
from app.forms import LoginForm, RegisterForm, AddingTaskManager
import this

# Login-manager
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    print("login_manager zbs")
    return UserLogin().from_db(user_id, dbase)


# Подключение к СУБД через драйвер psycopg2
def connect_db():
    conn = psycopg2.connect(dbname="Kursach_Ferma", user="postgres", password="alp37327", host="localhost")
    print("Connection w/ DB zbs")
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.before_request
def before_request():
    db = get_db()
    global dbase
    dbase = DataBase(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


# Декораторы маршрутов
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Создание экземпляра класса LoginForm
    login_form = LoginForm()

    # Переадресация, если пользователь залогинен
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if login_form.validate_on_submit():
        user = dbase.get_user(login_form.login_loginform.data)
        if user:
            print(user)
        else:
            print("user not found")

        if user and check_password_hash(user['password_of_worker'], login_form.password_loginform.data):
            print("Check is nice")

        if user and check_password_hash(user['password_of_worker'], login_form.password_loginform.data):
            print("check zbs")

            user_login = UserLogin().create(user)
            rm = True if login_form.remember_loginform.data else False
            login_user(user_login, remember=rm)
            session['role'] = user['name_of_role']
            if login_user:
                print("login zbs")

            return redirect(url_for('index'))

    return render_template('login.html', login_form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegisterForm()
    # Проверка на валидацию формы
    if reg_form.validate_on_submit():
        print("validate zbs")
        user = dbase.get_user(reg_form.login_regform.data)
        print(user)
        if user:
            flash("Account already exists")
            redirect(url_for('register'))
        else:
            dbase.add_user(reg_form.fio_regform.data, reg_form.role_regform.data, reg_form.login_regform.data, reg_form.password_regform.data)
            print("adding user in table zbs")

    return render_template('register.html', reg_form=reg_form)


@app.route('/tasks')
def tasks():
    task_form = AddingTaskManager()
    task_form.login_addingtaskmeneger_form.choices = [dbase.get_all_users()]
    return render_template("tasks.html")


@app.route('/test')
def test():
    return render_template("test.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    print("logout zbs")

    return redirect(url_for('index'))
