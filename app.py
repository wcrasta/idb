from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import json
import time

# Create the Flask application.
app = Flask(__name__)

app.debug = True

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about.html', methods=['GET'])
def about():
    return render_template('about.html', title="about")


@app.route('/games.html', methods=['GET'])
def games():
	items = populateGrid()
	return render_template('games.html', items=items, title="games")


@app.route('/reviews.html', methods=['GET'])
def reviews():
    return render_template('reviews.html', title="reviews")


@app.route('/platforms.html', methods=['GET'])
def platforms():
    return render_template('platforms.html', title='platforms')


@app.route('/studios.html', methods=['GET'])	
def studios():
    return render_template('studios.html', title='studios')

def populateGrid():
	with open('games.json') as json_data:
		items = json.load(json_data)
		for x in items:
			if(x['first_release_date']):
				x['first_release_date'] = time.strftime("%m-%d-%Y", time.gmtime(x['first_release_date']/1000))
			print(x['first_release_date'])
		return items

# Run the Flask app.
if __name__ == '__main__':
    app.run()