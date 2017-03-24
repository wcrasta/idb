#!/usr/bin/env python3

# pylint: disable = no-member
# pylint: disable = missing-docstring
# pylint: disable = invalid-name
# pylint: disable = too-few-public-methods


#from database import db
# from app import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os 
app = Flask(__name__)

app.debug = True

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
db = SQLAlchemy(app)

class Game(db.Model):

    """
        Game model represents the various games and contains information
        regarding their names, esrb ratings, ratings, status, website, images
        and more. It has relationships with other models like studio, reviews
        and companies.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    api_id = db.Column(db.Integer)
    summary = db.Column(db.Text)

    genre = db.Column(db.String(80))

    rating = db.Column(db.Float)

    storyline = db.Column(db.Text)

    category = db.Column(db.Integer)

    esrb = db.Column(db.Integer)

    status = db.Column(db.Integer)

    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))

    studio_id = db.Column(db.Integer, db.ForeignKey('studio.id'))

    reviews = db.relationship('Reviews', backref='game', lazy="dynamic")

    video = db.Column(db.String(128))

    image = db.Column(db.String(128))
    release_date = db.Column(db.DateTime)
    website = db.Column(db.String(80))

    #inits a game object
    def __init__(self, name, api_id, summary, genre, \
        rating, storyline, category, esrb, status, platform_id, \
        studio_id, reviews, video, image, release_date, website):
        assert name!=None
        assert api_id>0
        assert summary != None
        assert genre != None 
        assert rating > -1
        assert storyline != None
        assert category > -1
        assert category< 50
        assert esrb>-1
        assert status > -1 and status < 50
        assert video != None
        assert image != None
        assert release_date != None
        assert website != None
        self.name = name
        self.api_id = api_id
        self.summary = summary
        self.genre = genre 
        self.rating = rating
        self.storyline = storyline
        self.category = category
        self.esrb = esrb
        self.status = status
        self.platform_id = platform_id
        self.studio_id = studio_id
        self.reviews = reviews
        self.video = video
        self.image = image
        self.release_date = release_date
        self.website = website 


class Platform(db.Model):

    """ Platform is a model that represents the various video game consoles
    that exist  and it contains information regarding the games the console
    supports, the reviews of the console, the generation, image, website and
    etc. Platform models also have relationships with the other models such as
    game, review and studio.
    """

    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer)

    created_at = db.Column(db.DateTime)
    name = db.Column(db.String(80))
    summary = db.Column(db.Text)
    games = db.relationship('Game', backref='platform', lazy="dynamic")
    review = db.relationship('Reviews', backref='platform', lazy="dynamic")
    generation = db.Column(db.Integer)
    image = db.Column(db.String(128))
    website = db.Column(db.String(80))
    studio = db.relationship('Studio', backref='platform', lazy="dynamic")

    #makes a platform object
    def __init__(self, api_id, created_at, name, summary, games , review, generation, image, website, studio):
        assert api_id > 0
        assert created_at!=None
        assert name != ''
        assert summary != None 
        assert games != None
        assert review != None 
        assert generation > -1 and generation < 100
        assert image != None
        assert website != None 
        assert studio != None

        self.api_id = api_id
        self.created_at = created_at
        self.name = name
        self.summary = summary
        self.games =games 
        self.review = review 
        self.generation = generation
        self.image = image
        self.website = website
        self.studio = studio

class Studio(db.Model):

    """
        Studio is a model that represents the companies that publish and develop
        video games. Studios have informatino regarding the name, the logo, the games
        they built/published, the website and etc.
        Studio models have relationships with game, platform and reviews.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))

    logo = db.Column(db.String(128))
    description = db.Column(db.Text, nullable=True)
    game = db.relationship('Game', backref='studio', lazy="dynamic")
    created_at = db.Column(db.DateTime)
    website = db.Column(db.String(128))

    #makes a studio model
    def __init__(self, name, platform_id, logo, description, game, created_at, website ):
        assert name != ''
        assert platform_id >=0
        assert logo != None
        assert description != None
        assert game != None
        assert created_at != None
        assert website != None
        self.name = name
        self.platform_id = platform_id
        self.logo = logo
        self.description = description
        self.game = game 
        self.created_at = created_at
        self.website = website

class Reviews(db.Model):

    """
        Reviews is a model that represents the consumer reviews of various
        games that involve discussing the console the game is on and the company
        that built it. Reviews contain information regarding the title,
        the number of views of the review, website, and written contents
        such as introduction, content and conclusion.
        Reviews have relationships with game,platform and studios.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))

    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    created_at = db.Column(db.DateTime)
    views = db.Column(db.Integer)

    video = db.Column(db.String(128))
    introduction = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text)
    conclusion = db.Column(db.Text)
    positive = db.Column(db.Text)
    negative = db.Column(db.Text)
    url = db.Column(db.String(80))

    #makes a reviews model 
    def __init__(self, title,platform_id, game_id, created_at, views, video,\
     introduction, content, conclusion, positive, negative, url):
        assert title!=''
        assert platform_id != None
        assert game_id != None
        assert created_at != None
        assert views >=0
        assert video != None
        assert introduction != None
        assert content!= None
        assert conclusion!= None
        assert positive != None
        assert negative!=None
        assert url!=None
        self.title = title
        self.platform_id=platform_id
        self.game_id = game_id
        self.created_at = created_at
        self.views = views
        self.video = video
        self.introduction = introduction
        self.content = content
        self.conclusion = conclusion
        self.positive = positive
        self.negative = negative
        self.url = url