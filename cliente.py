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

@app.route('/restaurants/')
def restaurants():
	restaurantes = requests.get(dominioApi + '/api/v1/restaurants')
	restaurantes = restaurantes.json()
	return render_template('restaurants.html',restaurantes=restaurantes['restaurants'])

@app.route('/atractions/')
def atractions():
	atracciones = requests.get(dominioApi + '/api/v1/atractions')
	atracciones = atracciones.json()
	return render_template('atracciones.html',atracciones=atracciones['atractions'])

if __name__ == '__main__':
	app.run(host='127.0.0.1',port='5001',debug=True)