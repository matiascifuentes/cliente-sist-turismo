from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class User(UserMixin):
    def __init__(self, id, name, email, password, is_admin=False):
        self.id = id
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def __repr__(self):
        return '<User {}>'.format(self.email)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')

users = [User(1,'matias','matias@gmail.com','12345')]
def get_user(email):
    for user in users:
        if user.email == email:
            return user
    return None