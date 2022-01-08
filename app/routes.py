from app import app
from flask import render_template, flash, redirect, request, session, url_for
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin


# Login-manager
login_manager = LoginManager(app)

# Подключение к СУБД через драйвер psycopg2
conn = psycopg2.connect(dbname="Kursach_Ferma", user="postgres", password="alp37327", host="localhost")


@login_manager.user_loader
def load_user(user_id):
    print("zbs")
    return UserLogin().from_db()


# Декораторы маршрутов
@app.route('/')
def index():
    # Работа с БД
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT ")

    return render_template("index.html")


@app.route('/login/',  methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated():
        return redirect(url_for('index'))

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        login_in_logform = request.form['login']
        password = request.form['password']

        cursor.execute("SELECT * FROM worker WHERE login_of_worker = %s", (login_in_logform,))
        account = cursor.fetchone()
        password_rs = account['password_of_worker']

        if account and check_password_hash(password_rs, password):
            userlogin = UserLogin().create(account)
            rm = True if request.form.get('checkbox') else False
            login_user(userlogin, remember=rm)

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

    if request.method == 'POST':
        login_in_regform = request.form['login']
        password = request.form['password']
        fio = request.form['fio']
        role = request.form['role']

        _hashed_password = generate_password_hash(password)

        cursor.execute("SELECT * FROM worker WHERE login_of_worker = %s", (login_in_regform,))
        account = cursor.fetchone()

        cursor.execute("SELECT * FROM roles WHERE name_of_role = %s", (role,))
        role = cursor.fetchone()

        if account:
            flash('Account already exists!')
        else:
            if role:
                cursor.execute("INSERT INTO worker(login_of_worker, password_of_worker, fio_of_worker, name_of_role) VALUES (%s,%s,%s,%s)", (login_in_regform, _hashed_password, fio, role))
                conn.commit()
                flash('Registration is successful')
            else:
                flash('Sosi hui')

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

