from flask import Flask, render_template
import requests

app = Flask(__name__)
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

@app.route('/atractions/<cod_atraction>')
def atraction(cod_atraccion):
	atraccion = requests.get(dominioApi + '/api/v1/atractions/' + cod_atraccion)
	atraccion = atraccion.json()
	return render_template('atraction.html',atraccion=atraccion['atraction'])

if __name__ == '__main__':
	app.run(host='127.0.0.1',port='5001',debug=True)