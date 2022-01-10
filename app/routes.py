from app import app
from flask import render_template, redirect, request, url_for, g
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app.UserLogin import UserLogin
from app.DataBase import DataBase

# Login-manager
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    print("zbs")
    return UserLogin().from_db(user_id, dbase)


# Подключение к СУБД через драйвер psycopg2
def connect_db():
    conn = psycopg2.connect(dbname="Kursach_Ferma", user="postgres", password="alp37327", host="localhost")
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


global dbase
@app.before_request
def before_request():
    db = get_db()
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
    # Переадресация, если пользователь залогинен
    if current_user.is_authenticated():
        return redirect(url_for('index'))

    if request.method == 'POST' and 'login' in request.form and 'password' in request.form:
        user = dbase.get_user(request.form['login'])

        if user and check_password_hash(user['password_of_worker'], request.form['password']):
            user_login = UserLogin().create(user)
            rm = True if request.form.get('rememberme') else False
            login_user(user_login, remember=rm)

            return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/tasks')
def tasks():
    return redirect(url_for('index'))


@app.route('/test')
def test():
    return render_template("test.html")


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
