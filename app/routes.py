from app import app
from flask import render_template, redirect, request, url_for, g, session
from flask import render_template, redirect, request, url_for, g, flash, session
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app.UserLogin import UserLogin
from app.DataBase import DataBase
from app.forms import LoginForm, RegisterForm
import datetime


# инициализация менеджера логинов
login_manager = LoginManager(app)


# Login-manager
@login_manager.user_loader
def load_user(user_id):
    return UserLogin().from_db(user_id, dbase)


# Подключение к СУБД через драйвер psycopg2
def connect_db():
    conn = psycopg2.connect(dbname="Kursach_Ferma", user="postgres", password="alp37327", host="localhost")
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

# Создание объекта для работы с бд
@app.before_request
def before_request():
    db = get_db()
    global dbase
    dbase = DataBase(db)

# Закрытие работы с базой данных
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


# Декораторы маршрутов
@app.route('/')
def index():
    if current_user.is_authenticated:
        login_user = session['login']
        print(session['login'])
        return render_template("index.html", login_user=login_user)
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Создание экземпляра класса LoginForm
    login_form = LoginForm()
    # Переадресация, если пользователь залогинен
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Проверка валидации формы, введённой на сайте
    if login_form.validate_on_submit():
        # Проверяю, существует ли в базе данных пользователь с логином, введённым в форме
        user = dbase.get_user(login_form.login_loginform.data)
        # Проверка пароля; пароль хранится в виде хэша в целях безопасности
        if user and check_password_hash(user['password_of_worker'], login_form.password_loginform.data):
            print("check zbs")
            # Авторизация пользователя
            user_login = UserLogin().create(user)
            login_user(user_login)
            session['role'] = user[1]
            session['login'] = user[2]
            print(session['login'])

            return redirect(url_for('index'))

    return render_template('login.html', login_form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegisterForm()

    # Проверка на валидацию формы
    if reg_form.validate_on_submit():

        # Хэширование пароля
        _hashed_password = generate_password_hash(reg_form.password_regform.data)

        user = dbase.get_user(reg_form.login_regform.data)
        if user:
            flash("Account already exists")
            redirect(url_for('register'))
        else:
            dbase.add_user(reg_form.fio_regform.data, reg_form.role_regform.data, reg_form.login_regform.data, _hashed_password)

            return redirect(url_for('index'))

    return render_template('register.html', reg_form=reg_form)


@app.route('/tasks', methods=['GET','POST'])
@login_required
def tasks():
    if session['role'] == 'executor':
        changing_form = ChangingStatusForm()
        tasks_executor = dbase.get_tasks_executor(session['login'])
        tasks_executor_i_len = len(tasks_executor)
        print(tasks_executor_i_len)
        return render_template("tasks.html", tasks_executor_i_len=tasks_executor_i_len, tasks_executor=tasks_executor,
                               changing_form=changing_form)
    elif session['role'] == 'manager':
        tasks_manager = dbase.get_tasks_manager()
        tasks_manager_i_len = len(tasks_manager)
        print(tasks_manager_i_len)
        print(tasks_manager)

        return render_template("tasks.html", tasks_manager_i_len=tasks_manager_i_len, tasks_manager=tasks_manager)


@app.route('/task_adding', methods=['GET', 'POST'])
@login_required
def task_purpose_adding():
    # Получаю всех работников с ролью "рабочий"
    executors_select = dbase.get_all_users()
    executors_select_len = len(executors_select)
    executors_select_dict = {}
    for i in range(executors_select_len):
        executors_select_dict[i+1] = executors_select[i][0]

    # Получаю все локации из базы данных
    locations_select = dbase.get_all_locations()
    locations_select_len = len(locations_select)
    locations_select_dict = {}
    for i in range(locations_select_len):
        locations_select_dict[i+1] = locations_select[i][0]

    # Получаю все типы задач из базы данных
    typeoftask_select = dbase.get_all_types()
    typeoftask_select_len = len(typeoftask_select)
    typeoftask_select_dict = {}
    for i in range(typeoftask_select_len):
        typeoftask_select_dict[i + 1] = typeoftask_select[i][0]

    # Добавляю задачу
    if request.method == 'POST':
        # Получаю логин
        select_login = request.form['select-login']
        select_login_value = executors_select_dict[int(select_login)]
        # Получаю локацию
        select_location = request.form['select-location']
        select_location_value = locations_select_dict[int(select_location)]
        # Получаю тип задачи
        select_typeoftask = request.form['select-typeoftask']
        select_typeoftask_value = typeoftask_select_dict[int(select_typeoftask)]
        # Получаю время
        current_datetime_addingtask = datetime.datetime.now()
        # Получаю комментарий
        input_comment = request.form['comment-form']

        # Конкатенация локации и типа
        adding_location_plus_typeoftask = select_typeoftask_value + " in " + select_location_value

        # Взаимодействие с БД
        id_of_task = dbase.get_task_by_text(adding_location_plus_typeoftask)
        if id_of_task is False:
            dbase.add_task_form(adding_location_plus_typeoftask, select_location, select_typeoftask)
        id_of_task = dbase.get_task_by_text(adding_location_plus_typeoftask)
        dbase.add_purpose_comment_form(input_comment, current_datetime_addingtask, id_of_task, select_login_value)

    return render_template("task_adding.html", executors_select_dict=executors_select_dict,
                           locations_select_dict=locations_select_dict, typeoftask_select_dict=typeoftask_select_dict)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")

    return redirect(url_for('index'))
