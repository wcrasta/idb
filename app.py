from database import db
from flask import Flask, render_template
from flask import request
import os
import json
import time
#from models import *
# Create the Flask application.
from models import Game, Platform, Reviews, Studio
app = Flask(__name__)

app.debug = False

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# db = SQLAlchemy(app)

#from models import Game, Platform, Reviews, Studio

POSTS_PER_PAGE=10

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title="about")


@app.route('/games', methods=['GET'])
@app.route('/games/<int:page>', methods=['GET'])
def games(page=1):
    value = request.args.get('sort', 'name')
    games = db.session.query(Game).order_by(eval('Game.'+value)).paginate(page, POSTS_PER_PAGE,True)

    return render_template('games.html', title='games', items=games)

	#items = populateGrid()
	#return render_template('games.html', items=items, title="games")


@app.route('/reviews', methods=['GET'])
@app.route('/reviews/<int:page>', methods=['GET'])
def reviews(page=1):
    reviews = db.session.query(Reviews).paginate(page, POSTS_PER_PAGE,False)
    #return render_template('reviews.html', title="reviews")
    return render_template('reviews.html', title='reviews', items=reviews)

@app.route('/review/<name>', methods = ['GET'])
def review_instance(name):
    review_instance = db.session.query(Reviews).get(name)
    return render_template('review.html', title='review_instance', items = review_instance)


@app.route('/platforms', methods=['GET'])
@app.route('/platforms/<int:page>', methods = ['GET'])
def platforms(page=1):
    platforms = db.session.query(Platform).paginate(page, POSTS_PER_PAGE,False)
    #return render_template('platforms.html', title='platforms')
    return render_template('platforms.html', title='platforms', items=platforms)

@app.route('/platform/<name>', methods = ['GET'])
def platform_instance(name):
    platform_instance = db.session.query(Platform).get(name)
    #platform_instance = db.session.query(Platform).filter(Platform.name.contains(name))
    return render_template('platform.html', title='platform_instance', items = platform_instance)
    #return render_template('platform.html')

@app.route('/studios', methods=['GET'])
@app.route('/studios/<int:page>', methods = ['GET'])
def studios(page=1):
    #for instance in db.session.query(Studio).order_by(Studio.name):
    studios = db.session.query(Studio).paginate(page, POSTS_PER_PAGE,False)
    #posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False).items
    #return render_template('index.html',
    #                       title='Home',
    #                       form=form,
    #                       posts=posts)
    return render_template('studios.html', title='studios', items=studios)

@app.route('/studio/<name>', methods = ['GET'])
def studio_instance(name):
    studio_instance = db.session.query(Studio).get(name)
    return render_template('studio.html', title='studio_instance', items = studio_instance)


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
