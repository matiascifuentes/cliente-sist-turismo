from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length
import requests

class User(UserMixin):
    def __init__(self, id, name, email, password, is_hash=False, is_admin=False):
        self.id = id
        self.name = name
        self.email = email
        if (is_hash):
            self.password = password
        else:
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

def get_user(email):
    response = requests.request("GET","http://127.0.0.1:5000/api/v1/users/" + email + "/byemail", headers={})
    if(response.status_code == 200 and 'user' in response.json()):
        user = response.json()['user']
        return User(user['id_usuario'],user['nombre'],email,user['password'],is_hash=True)
    return None