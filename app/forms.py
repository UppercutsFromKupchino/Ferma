from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login_loginform = StringField("Login", validators=[DataRequired()])
    password_loginform = PasswordField("Password", validators=[DataRequired()])
    submit_loginform = SubmitField("Log in")


class RegisterForm(FlaskForm):
    login_regform = StringField("Login", validators=[DataRequired()])
    password_regform = PasswordField("Password", validators=[DataRequired()])
    role_regform = SelectField("Role", choices=['executor', 'manager'])
    fio_regform = StringField("FIO", validators=[DataRequired()])
    submit_regform = SubmitField("Register")


class ChangingForm(FlaskForm):
    submit_changing_hidden = HiddenField()
    submit_changing = SubmitField("Удалить задачу")


class ChangingFormExecutor(FlaskForm):
    select_status = SelectField()
    changing_status = HiddenField()
    changing_submit = SubmitField("Изменить статус")

