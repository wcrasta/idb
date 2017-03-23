from database import db
from flask import Flask, render_template
from flask import request
from flask_paginate import Pagination
import os
import json
import time
from flask_sqlalchemy import SQLAlchemy

# Create the Flask application.
from models import Game, Platform, Reviews, Studio
app = Flask(__name__)

app.debug = True

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
#db = SQLAlchemy(app)

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
    games = db.session.query(Game).filter(Game.api_id!=0 and Game.name!='').order_by(Game.name)
    pagination = Pagination(page=page, css_framework='foundation',total=games.count(), record_name='items')
    return render_template('games.html', items=games[min(page * 9,games.count()-9):(page+1) * 9], pagination=pagination)

	#items = populateGrid()
	#return render_template('games.html', items=items, title="games")

@app.route('/game/<name>', methods = ['GET'])
def game_instance(name):
    game_instance = db.session.query(Game).get(name)
    return render_template('game.html', title='game_instance', items = game_instance)

@app.route('/reviews', methods=['GET'])
@app.route('/reviews/<int:page>', methods=['GET'])
def reviews(page=1):
    value = request.args.get('sort', 'title')
    reviews = db.session.query(Reviews).filter(Reviews.url!='').order_by(Reviews.title)
    pagination = Pagination(page=page, css_framework='foundation',total=reviews.count(), record_name='items')
    return render_template('reviews.html', items=reviews[min(page * 9,reviews.count()-9):(page+1) * 9], pagination=pagination)

    # reviews = db.session.query(Reviews).paginate(page, POSTS_PER_PAGE,False)
    # return render_template('reviews.html', title='reviews', items=reviews)

@app.route('/review/<name>', methods = ['GET'])
def review_instance(name):
    review_instance = db.session.query(Reviews).get(name)
    return render_template('review.html', title='review_instance', items = review_instance)


@app.route('/platforms', methods=['GET'])
@app.route('/platforms/<int:page>', methods = ['GET'])
def platforms(page=1):
    # platforms = db.session.query(Platform).paginate(page, POSTS_PER_PAGE,False)
    # #return render_template('platforms.html', title='platforms')
    # return render_template('platforms.html', title='platforms', items=platforms)
    value = request.args.get('sort', 'name')
    platforms = db.session.query(Platform).filter(Platform.api_id!=0 and Platform.name!='').order_by(Platform.name)
    pagination = Pagination(page=page, css_framework='foundation',total=platforms.count(), record_name='items')
    return render_template('platforms.html', items=platforms[min(page * 9,platforms.count()-9):(page+1) * 9], pagination=pagination)



@app.route('/platform/<name>', methods = ['GET'])
def platform_instance(name):
    platform_instance = db.session.query(Platform).get(name)
    #platform_instance = db.session.query(Platform).filter(Platform.name.contains(name))
    return render_template('platform.html', title='platform_instance', items = platform_instance)
    #return render_template('platform.html')

@app.route('/studios', methods=['GET'])
@app.route('/studios/<int:page>', methods = ['GET'])
def studios(page=1):
    value = request.args.get('sort', 'name')
    studios = db.session.query(Studio).filter(Studio.name!='').order_by(Studio.name)
    pagination = Pagination(page=page, css_framework='foundation',total=studios.count(), record_name='items')
    return render_template('studios.html', items=studios[min(page * 9,studios.count()-9):(page+1) * 9], pagination=pagination)

@app.route('/studio/<name>', methods = ['GET'])
def studio_instance(name):
    studio_instance = db.session.query(Studio).get(name)
    return render_template('studio.html', title='studio_instance', items = studio_instance)



# Run the Flask app.
if __name__ == '__main__':
    app.run()
