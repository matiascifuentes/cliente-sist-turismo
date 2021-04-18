from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import requests
from models import LoginForm, User, get_user
from werkzeug.urls import url_parse
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
login_manager = LoginManager(app)
login_manager.login_view = "login"
dominioApi = 'http://127.0.0.1:5000'

@app.route('/')
@login_required
def index():
	return render_template('index.html')

@app.route('/hotels/')
@login_required
def hotels():
	hoteles = requests.get(dominioApi + '/api/v1/hotels')
	hoteles = hoteles.json()
	#VERIFICAR RESPUESTA
	return render_template('hotels.html',hoteles=hoteles['hotels'])

@app.route('/hotels/<cod_hotel>')
@login_required
def hotel(cod_hotel):
	hotel = requests.get(dominioApi + '/api/v1/hotels/' + cod_hotel)
	hotel = hotel.json()
	#VERIFICAR RESPUESTA
	return render_template('hotel.html',hotel=hotel['hotel'])

@app.route('/restaurants/')
@login_required
def restaurants():
	restaurantes = requests.get(dominioApi + '/api/v1/restaurants')
	restaurantes = restaurantes.json()
	return render_template('restaurants.html',restaurantes=restaurantes['restaurants'])

@app.route('/restaurants/<cod_restaurant>')
@login_required
def restaurant(cod_restaurant):
	restaurant = requests.get(dominioApi + '/api/v1/restaurants/' + cod_restaurant)
	restaurant = restaurant.json()
	return render_template('restaurant.html',restaurant=restaurant['restaurant'])

@app.route('/atractions/')
@login_required
def atractions():
	atracciones = requests.get(dominioApi + '/api/v1/atractions')
	atracciones = atracciones.json()
	return render_template('atractions.html',atracciones=atracciones['atractions'])

@app.route('/atractions/<cod_atraccion>')
@login_required
def atraction(cod_atraccion):
	atraccion = requests.get(dominioApi + '/api/v1/atractions/' + cod_atraccion)
	atraccion = atraccion.json()
	return render_template('atraction.html',atraccion=atraccion['atraction'])

@app.route('/carro/addlist',methods=["get","post"])
@login_required
def add_list():
	url = dominioApi + '/api/v1/lists'
	try:
		carro = json.loads(request.cookies.get(str(current_user.id)))
	except:
		carro = []
	if len(carro) > 0:
		servicios = []
		for servicio in carro:
			servicios.append({"id_servicio": servicio['id']})
		lista = {
			"id_usuario": 1,
			"servicios": servicios
		}	
		response = requests.request("POST", url, headers={}, json=lista)
		return carro_delete_all()
	return carro()

@app.route('/carro/add/<id>',methods=["get","post"])
@login_required
def carro_add(id):
	try:
		datos = json.loads(request.cookies.get(str(current_user.id)))
	except:
		datos = []
	
	exists = False
	for dato in datos:
	    if dato['id'] == id:
	        exists = True
	        break

	if not exists:
		datos.append({"id":id})
	
	resp = make_response(redirect(url_for('carro')))
	resp.set_cookie(str(current_user.id),json.dumps(datos))
	return resp


@app.route('/carro', methods=['GET'])
@login_required
def carro():
	try:
		datos = json.loads(request.cookies.get(str(current_user.id)))
	except:
		datos = []
	servicios = []
	for servicio in datos:
		servicios.append(servicio)
	return render_template("carro.html",servicios=servicios)

@app.route('/carro/delete/<id>')
@login_required
def carro_delete(id):
	try:
		datos = json.loads(request.cookies.get(str(current_user.id)))
	except:
		datos = []
	new_datos=[]
	for dato in datos:
		if dato['id']!=id:
			new_datos.append(dato)
	resp = make_response(redirect(url_for('carro')))
	resp.set_cookie(str(current_user.id),json.dumps(new_datos))
	return resp

@app.route('/carro/delete')
@login_required
def carro_delete_all():
	new_datos = []
	resp = make_response(redirect(url_for('carro')))
	resp.set_cookie(str(current_user.id),json.dumps(new_datos))
	return resp

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
    response = requests.request("GET","http://127.0.0.1:5000/api/v1/users/" + user_id + "/byid", headers={})
    if(response.status_code == 200 and 'user' in response.json()):
        user = response.json()['user']
        return User(user_id,user['nombre'],user['correo'],user['password'],is_hash=True)
    return None

if __name__ == '__main__':
	app.run(host='127.0.0.1',port='5001',debug=True)