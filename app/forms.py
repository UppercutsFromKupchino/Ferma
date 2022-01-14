from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login_loginform = StringField("Login", validators=[DataRequired()])
    password_loginform = PasswordField("Password", validators=[DataRequired()])
    remember_loginform = BooleanField("Remember me", default=False)
    submit_loginform = SubmitField("Log in")


class RegisterForm(FlaskForm):
    login_regform = StringField("Login", validators=[DataRequired()])
    password_regform = PasswordField("Password", validators=[DataRequired()])
    role_regform = StringField("Role", validators=[DataRequired()])
    fio_regform = StringField("FIO", validators=[DataRequired()])
    submit_regform = SubmitField("Register")


class AddingTaskManager(FlaskForm):
    location_addingtaskmanager_form = StringField("Location of task", validators=[DataRequired()])
    typeoftask_addingtaskmanager_form = StringField("Type of task", validators=[DataRequired()])
    comment_addingtaskmanager_form = StringField("Comment")
    login_addingtaskmanager_form = SelectField("Login of worker", choices=[])
    submit_addingtaskmanager_form = SubmitField("Add task")
