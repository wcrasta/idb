#!/usr/bin/env python3

# pylint: disable = no-member
# pylint: disable = missing-docstring
# pylint: disable = invalid-name
# pylint: disable = too-few-public-methods
# pylint: disable = too-many-arguments
# pylint: disable = too-many-instance-attributes
# pylint: disable = too-many-locals
# pylint: disable = line-too-long
# pylint: disable = unused-import
# pylint: disable = too-many-branches
import os
import datetime
import getpass
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import flask_whooshalchemy as whooshalchemy

app = Flask(__name__)
app.debug = True
api = Api(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['our_secret']

if getpass.getuser() == 'www-data': #pragma: no cover
    app.config['WHOOSH_BASE'] = '/var/www/FlaskApps/GGnoSWEApp/whoosh_index'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
#    os.path.join(basedir, 'app.db')
# WHOOSH_BASE = os.path.join(basedir,'app.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Game(db.Model):

    """
        Game model represents the various games and contains information
        regarding their names, esrb ratings, ratings, status, website, images
        and more. It has relationships with other models like studio, reviews
        and companies.
    """
    __tablename__ = 'game'
    __searchable__ = [
        'name', 'summary', 'genre', 'storyline', 'esrb', 'status']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    api_id = db.Column(db.Integer)
    summary = db.Column(db.Text)
    genre = db.Column(db.String(256))
    rating = db.Column(db.Float)
    storyline = db.Column(db.Text)
    category = db.Column(db.String(256))
    esrb = db.Column(db.String(256))
    status = db.Column(db.String(256))
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))
    studio_id = db.Column(db.Integer, db.ForeignKey('studio.id'))
    reviews = db.relationship('Reviews', backref='game', lazy="dynamic")
    video = db.Column(db.String(256))
    image = db.Column(db.String(256))
    release_date = db.Column(db.DateTime)
    website = db.Column(db.String(256))

    # inits a game object
    def __init__(self, name=None, api_id=None, summary=None, genre=None,
                 rating=None, storyline=None, category=None, esrb=None, status=None,
                 video=None, image=None, release_date=None, website=None):

        if name != None: #pragma: no cover
            assert name != ''
            self.name = name

        if api_id != None: #pragma: no cover
            assert api_id > 0
            self.api_id = api_id

        if summary != None: #pragma: no cover
            assert summary != ""
            self.summary = summary

        if genre != None: #pragma: no cover
            assert genre != ""
            self.genre = genre

        if rating != None: #pragma: no cover
            assert rating > -1
            self.rating = rating

        if storyline != None: #pragma: no cover
            assert storyline != ""
            self.storyline = storyline

        if category != None: #pragma: no cover
            assert category != ''
            self.category = category

        if esrb != None: #pragma: no cover
            assert esrb != ''
            self.esrb = esrb

        if status != None: #pragma: no cover
            assert status != ''
            self.statis = status

        if video != None: #pragma: no cover
            assert video != ""
            self.video = video

        if image != None: #pragma: no cover
            assert image != ""
            self.image = image

        if release_date != None: #pragma: no cover
            assert isinstance(release_date, datetime)
            self.release_date = release_date

        if website != None: #pragma: no cover
            assert website != ""
            self.website = website


class Platform(db.Model):

    """ Platform is a model that represents the various video game consoles
    that exist  and it contains information regarding the games the console
    supports, the reviews of the console, the generation, image, website and
    etc. Platform models also have relationships with the other models such as
    game, review and studio.
    """
    __tablename__ = 'platform'
    __searchable__ = ['name', 'summary', 'image', 'website']
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

    # makes a platform object
    def __init__(self, api_id=None, created_at=None, name=None, summary=None,
                 games=None, review=None, generation=None, image=None, website=None, studio=None):

        if api_id != None: #pragma: no cover
            assert api_id > -1
            self.api_id = api_id

        if created_at != None: #pragma: no cover
            assert isinstance(created_at, datetime)

        if name != None: #pragma: no cover
            assert name != "None"
            self.name = name

        if summary != None: #pragma: no cover
            assert summary != ""
            self.summary = summary

        if games != None: #pragma: no cover
            assert isinstance(games, Game)
            self.games = games

        if review != None: #pragma: no cover
            assert isinstance(review, Reviews)
            self.review = review

        if generation != None: #pragma: no cover
            assert generation > -1 and generation < 100
            self.generation = generation

        if image != None: #pragma: no cover
            assert image != ""
            self.image = image

        if website != None: #pragma: no cover
            assert website != ""
            self.website = website

        if studio != None: #pragma: no cover
            assert isinstance(studio, Studio)
            self.studio = studio


class Studio(db.Model):

    """
        Studio is a model that represents the companies that publish and develop
        video games. Studios have informatino regarding the name, the logo, the games
        they built/published, the website and etc.
        Studio models have relationships with game, platform and reviews.
    """
    __tablename__ = 'studio'
    __searchable__ = ['name', 'logo', 'description', 'website']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))
    logo = db.Column(db.String(256))
    description = db.Column(db.Text, nullable=True)
    game = db.relationship('Game', backref='studio', lazy="dynamic")
    created_at = db.Column(db.DateTime)
    website = db.Column(db.String(256))

    # makes a studio model
    def __init__(self, name=None, platform_id=None, logo=None, description=None, game=None, created_at=None, website=None):

        if name != None: #pragma: no cover
            assert name != "None"
            self.name = name

        if platform_id != None: #pragma: no cover
            assert platform_id >= 0
            self.platform_id = platform_id

        if logo != None: #pragma: no cover
            assert logo != ""
            self.logo = logo

        if description != None: #pragma: no cover
            assert description != ""
            self.description = description

        if game != None: #pragma: no cover
            assert isinstance(game, Game)
            self.game = game

        if created_at != None: #pragma: no cover
            assert isinstance(created_at, datetime)
            self.created_at = created_at

        if website != None: #pragma: no cover
            assert website != ""
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
    __tablename__ = 'reviews'
    __searchable__ = ['title', 'video', 'introduction',
                      'content', 'conclusion', 'positive', 'negative', 'url']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    created_at = db.Column(db.DateTime)
    views = db.Column(db.Integer)
    video = db.Column(db.String(256))
    introduction = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text)
    conclusion = db.Column(db.Text)
    positive = db.Column(db.Text)
    negative = db.Column(db.Text)
    url = db.Column(db.String(256))

    # makes a reviews model
    def __init__(
            self, title=None, platform_id=None, game_id=None, created_at=None, views=None, video=None,
            introduction=None, content=None, conclusion=None, positive=None, negative=None, url=None):
        if title != None: #pragma: no cover
            assert title != ""
            self.title = title

        if platform_id != None: #pragma: no cover
            assert platform_id >= 0
            self.platform_id = platform_id

        if game_id != None: #pragma: no cover
            assert game_id >= 0
            self.game_id = game_id

        if created_at != None: #pragma: no cover
            assert isinstance(created_at, datetime)
            self.created_at = created_at

        if views != None: #pragma: no cover
            assert views >= 0
            self.views = views

        if video != None: #pragma: no cover
            assert video != ""
            self.video = video

        if introduction != None: #pragma: no cover
            assert introduction != ""
            self.introduction = introduction

        if content != None: #pragma: no cover
            assert content != ""
            self.content = content

        if conclusion != None: #pragma: no cover
            assert conclusion != ""
            self.conclusion = conclusion

        if positive != None: #pragma: no cover
            assert positive != ""
            self.positive = positive

        if negative != None: #pragma: no cover
            assert negative != ""
            self.negative = negative

        if url != None: #pragma: no cover
            assert url != "None"
            self. url = url
whooshalchemy.whoosh_index(app, Game)
whooshalchemy.whoosh_index(app, Studio)
whooshalchemy.whoosh_index(app, Reviews)
whooshalchemy.whoosh_index(app, Platform)
