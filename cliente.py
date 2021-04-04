from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user
import requests
from models import users, LoginForm, get_user
from werkzeug.urls import url_parse

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
login_manager = LoginManager(app)
login_manager.login_view = "login"
dominioApi = 'http://127.0.0.1:5000'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/hotels/')
def hotels():
	hoteles = requests.get(dominioApi + '/api/v1/hotels')
	hoteles = hoteles.json()
	#VERIFICAR RESPUESTA
	return render_template('hotels.html',hoteles=hoteles['hotels'])

@app.route('/hotels/<cod_hotel>')
def hotel(cod_hotel):
	hotel = requests.get(dominioApi + '/api/v1/hotels/' + cod_hotel)
	hotel = hotel.json()
	#VERIFICAR RESPUESTA
	return render_template('hotel.html',hotel=hotel['hotel'])

@app.route('/restaurants/')
def restaurants():
	restaurantes = requests.get(dominioApi + '/api/v1/restaurants')
	restaurantes = restaurantes.json()
	return render_template('restaurants.html',restaurantes=restaurantes['restaurants'])

@app.route('/restaurants/<cod_restaurant>')
def restaurant(cod_restaurant):
	restaurant = requests.get(dominioApi + '/api/v1/restaurants/' + cod_restaurant)
	restaurant = restaurant.json()
	return render_template('restaurant.html',restaurant=restaurant['restaurant'])

@app.route('/atractions/')
def atractions():
	atracciones = requests.get(dominioApi + '/api/v1/atractions')
	atracciones = atracciones.json()
	return render_template('atractions.html',atracciones=atracciones['atractions'])

@app.route('/atractions/<cod_atraccion>')
def atraction(cod_atraccion):
	atraccion = requests.get(dominioApi + '/api/v1/atractions/' + cod_atraccion)
	atraccion = atraccion.json()
	return render_template('atraction.html',atraccion=atraccion['atraction'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None

if __name__ == '__main__':
	app.run(host='127.0.0.1',port='5001',debug=True)