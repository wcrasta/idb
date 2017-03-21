from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import json
import time
from models import *
# Create the Flask application.
app = Flask(__name__)

app.debug = True

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

POSTS_PER_PAGE=10

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about.html', methods=['GET'])
def about():
    return render_template('about.html', title="about")


@app.route('/games.html', methods=['GET'])
@app.route('/games.html/<int:page>', methods=['GET'])
def games(page=1):
    games = db.session.query(Game).paginate(page, POSTS_PER_PAGE,False)
    return render_template('games.html', title='games', items=games)

	#items = populateGrid()
	#return render_template('games.html', items=items, title="games")


@app.route('/reviews.html', methods=['GET'])
@app.route('/reviews.html/<int:page>', methods=['GET'])
def reviews(page=1):
    reviews = db.session.query(Reviews).paginate(page, POSTS_PER_PAGE,False)
    #return render_template('reviews.html', title="reviews")
    return render_template('reviews.html', title='reviews', items=reviews)


@app.route('/platforms.html', methods=['GET'])
@app.route('/platforms.html/<int:page>', methods = ['GET'])
def platforms(page=1):
    platforms = db.session.query(Platform).paginate(page, POSTS_PER_PAGE,False)
    #return render_template('platforms.html', title='platforms')
    return render_template('platforms.html', title='platforms', items=platforms)


@app.route('/studios.html', methods=['GET'])
@app.route('/studios.html/<int:page>', methods = ['GET'])
def studios(page=1):
    #for instance in db.session.query(Studio).order_by(Studio.name):
    studios = db.session.query(Studio).paginate(page, POSTS_PER_PAGE,False)
    #posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False).items
    #return render_template('index.html',
    #                       title='Home',
    #                       form=form,
    #                       posts=posts)
    return render_template('studios.html', title='studios', items=studios)



def populateGrid():
	with open('games.json') as json_data:
		items = json.load(json_data)
		for x in items:
			if('first_release_date' in x):
				x['first_release_date'] = time.strftime("%m-%d-%Y", time.gmtime(x['first_release_date']/1000))
			#print(x['first_release_date'])
		return items

# Run the Flask app.
if __name__ == '__main__':
    app.run()
