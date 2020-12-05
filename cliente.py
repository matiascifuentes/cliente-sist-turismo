from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/hotels/')
def hotels():
	return render_template('hotels.html')

@app.route('/restaurants/')
def restaurants():
	return render_template('restaurants.html')

if __name__ == '__main__':
	app.run()