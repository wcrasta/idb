from models import app
from database import db
from flask import Flask, render_template
from flask import request
from flask_paginate import Pagination
import os
import json
import time
from flask_sqlalchemy import SQLAlchemy

from models import Game, Platform, Reviews, Studio

POSTS_PER_PAGE = 10

@app.route('/report')
def report():
    """
        Renders the report page
    """
    return render_template('report.html')

@app.route('/')
def index():
    """
        Renders the home page
    """
    return render_template('home.html')


@app.route('/about', methods=['GET'])
def about():
    """
        Renders the about page
    """
    return render_template('about.html', title="about")


@app.route('/games', methods=['GET'])
@app.route('/games/<int:page>', methods=['GET'])
def games(page=1):
    """
        Renders the games page 
        passing in Game objects for dynamic generation of pages
    """

    value = request.args.get('sort', 'name')
    games = db.session.query(Game).filter(
        Game.api_id != 0 and Game.name != '').order_by(Game.name)
    pagination = Pagination(
        page=page, css_framework='foundation', total=games.count(), record_name='items')
    return render_template('games.html', items=games[min(page * 9, games.count() - 9):(page + 1) * 9], pagination=pagination)

       
@app.route('/game/<name>', methods=['GET'])
def game_instance(name):
    """
        Renders the game_instance page populating items 
        with Game objects
    """
    game_instance = db.session.query(Game).get(name)
    return render_template('game.html', title='game_instance', items=game_instance)


@app.route('/reviews', methods=['GET'])
@app.route('/reviews/<int:page>', methods=['GET'])
def reviews(page=1):
    """
        Renders the reviews page 
        passing in Reviews objects for dynamic generation of pages
    """
    value = request.args.get('sort', 'title')
    reviews = db.session.query(Reviews).filter(
        Reviews.url != '').order_by(Reviews.title)
    pagination = Pagination(
        page=page, css_framework='foundation', total=reviews.count(), record_name='items')
    return render_template('reviews.html', items=reviews[min(page * 9, reviews.count() - 9):(page + 1) * 9], pagination=pagination)



@app.route('/review/<name>', methods=['GET'])
def review_instance(name):
    """
        Renders the review_instance page populating items 
        with Reviews objects
    """
    review_instance = db.session.query(Reviews).get(name)
    return render_template('review.html', title='review_instance', items=review_instance)


@app.route('/platforms', methods=['GET'])
@app.route('/platforms/<int:page>', methods=['GET'])
def platforms(page=1):
    """
        Renders the platforms  page 
        passing in Platform objects for dynamic generation of pages
    """
    value = request.args.get('sort', 'name')
    platforms = db.session.query(Platform).filter(
        Platform.api_id != 0 and Platform.name != '').order_by(Platform.name)
    pagination = Pagination(
        page=page, css_framework='foundation', total=platforms.count(), record_name='items')
    return render_template('platforms.html', items=platforms[min(page * 9, platforms.count() - 9):(page + 1) * 9], pagination=pagination)


@app.route('/platform/<name>', methods=['GET'])
def platform_instance(name):
    """
        Renders the platform_instance page populating items 
        with platform objects
    """
    platform_instance = db.session.query(Platform).get(name)
   
    return render_template('platform.html', title='platform_instance', items=platform_instance)


@app.route('/studios', methods=['GET'])
@app.route('/studios/<int:page>', methods=['GET'])
def studios(page=1):
    """
        Renders the studio  page 
        passing in Studios objects for dynamic generation of pages
    """
    value = request.args.get('sort', 'name')
    studios = db.session.query(Studio).filter(
        Studio.name != '').order_by(Studio.name)
    pagination = Pagination(
        page=page, css_framework='foundation', total=studios.count(), record_name='items')
    return render_template('studios.html', items=studios[min(page * 9, studios.count() - 9):(page + 1) * 9], pagination=pagination)


@app.route('/studio/<name>', methods=['GET'])
def studio_instance(name):
    """
        Renders the studio_instance page populating items 
        with studio objects
    """
    studio_instance = db.session.query(Studio).get(name)
    return render_template('studio.html', title='studio_instance', items=studio_instance)



if __name__=='__main__':
    app.run()
