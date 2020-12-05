from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
	return '<h1>INDEX</h1>'

@app.route('/hotels/')
def hotels():
	return '<h1>HOTELES</h1>'

@app.route('/restaurants/')
def restaurants():
	return '<h1>RESTAURANTES</h1>'

if __name__ == '__main__':
	app.run()