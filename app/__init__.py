from models import app
from flask import Flask, render_template
from flask import request
from flask_paginate import Pagination
import os
import json
import time
import subprocess
import sys

from flask_sqlalchemy import SQLAlchemy

from models import Game, Platform, Reviews, Studio, app, db

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


@app.route('/unit_tests')
def unit_tests():
    """
        Renders the home page
    """
    # Use full path on server
    print(os.path.realpath(__file__)[:-11])
    return subprocess.check_output([sys.executable, os.path.realpath(__file__)[:-11] + 'tests.py'], stderr=subprocess.STDOUT)


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
    #Appended None to the dictionaries as dummies
    platform = db.session.query(Platform.id, Platform.name).filter(Platform.name != '').order_by('Platform.name')
    genre = {33: "Arcade", 32: "Indie", 31: "Adventure", 30: "Pinball", 26: "Quiz/Trivia", 25: "Hack and slash/Beat 'em up", 24: "Tactical", 16:
              "Turn-based strategy (TBS)", 15: "Strategy", 14: "Sport", 13: "Simulator", 12: "Role-playing (RPG)", 11: "Real Time Strategy (RTS)", 10: "Racing", 9: "Puzzle", 8: "Platform", 7: "Music", 5: "Shooter", 4: "Fighting", 2: "Point-and-click", 99:"None"}
    genre = genre.values()
    status = {0: "Released", 2: "Alpha", 3: "Beta",
                   4: "Early Access", 5: "offline", 6: "Cancelled", 99:"None"}
    status = status.values()
    esrb = {1: "RP", 2: "EC", 3: "E", 4: "E10+", 5: "T", 6: "M", 7: "AO", 8:"None"}
    esrb = esrb.values()
    category = {0: "Main Game", 1: "DLC/Add on", 2:
                     "Expansion", 3: "Bundle", 4: "Standalone expansion", 5:"None"}
    category = category.values()

    #Use so the first time the page is loaded, the things will be unchecked
    genreTemp = []
    statusTemp = []
    esrbTemp = []
    categoryTemp = []
    sort = request.args.get('sort', 'name asc')
    sortPlatform = request.args.getlist('platform')
    sortGenre = request.args.getlist('genre')
    sortStatus = request.args.getlist('status')
    sortEsrb = request.args.getlist('esrb')
    sortCategory = request.args.getlist('category')
    #sortPlatform = [for p in platform]
    genreTemp = sortGenre
    statusTemp = sortStatus
    esrbTemp = sortEsrb
    categoryTemp = sortCategory
    platformTemp = sortPlatform
    if not sortPlatform:
        sortPlatform = db.session.query(Platform.id)
    if not sortGenre:
        # allGenres = db.session.query(Game.genre).distinct()
        # print(allGenres)
        # sortGenre = [g for g in allGenres.all()]
        # print(sortGenre)
        sortGenre =genre
    if not sortStatus:
        sortStatus = status
    if not sortEsrb:
        sortEsrb = esrb
    if not sortCategory:
        sortCategory = category

    if len(platformTemp)>0:
        # if "-" in sort:
        #     games = db.session.query(Game).filter(Game.platform_id.in_(sortPlatform)).order_by(('Game.' + sort[1:]+" desc"))
        # else:
        games = db.session.query(Game.id, Game.name, Game.esrb, Game.rating, Game.genre, Game.release_date, Game.status, Game.image).filter(Game.platform_id.in_(sortPlatform)).filter(Game.genre.in_(sortGenre)).filter(Game.status.in_(sortStatus)).filter(Game.category.in_(sortCategory)).filter(Game.esrb.in_(sortEsrb)).order_by(('Game.' + sort))
    else:
        games = db.session.query(Game.id, Game.name, Game.esrb, Game.rating, Game.genre, Game.release_date, Game.status, Game.image).filter(Game.api_id != 0 and Game.name != '').filter(Game.genre.in_(sortGenre)).filter(Game.status.in_(sortStatus)).filter(Game.category.in_(sortCategory)).filter(Game.esrb.in_(sortEsrb)).order_by(('Game.' + sort))
        #.filter(Game.genre.in_(sortGenre)).filter(Game.status.in_(sortStatus)).filter(Game.category.in_(sortCategory)).filter(Game.esrb.in_(sortEsrb))
#.filter(Game.genre.in_(sortGenre)).filter(Game.status.in_(sortStatus)).filter(Game.category.in_(sortCategory)).filter(Game.esrb.in_(sortEsrb))
#filter(Game.studio_id.in_(sortStudio)).filter(Game.platform_id.in_(sortPlatform)).
    #games = db.session.query(Game).filter(Game.api_id !=0 and Game.name !='').filter(Game.platform_id.in_(sortPlatform)).order_by(('Game.'+sort))
    pagination = Pagination(
        page=page, css_framework='foundation', total=games.count(), per_page=9, record_name='items')

    return render_template('games.html', items=games[(page - 1) * 9:min(page * 9, games.count())], pagination=pagination, genreTemp = genreTemp, esrbTemp = esrbTemp, categoryTemp=categoryTemp, 
        statusTemp=statusTemp,esrb = esrb, selected_esrb = sortEsrb, platforms = platform, genre=genre, category=category, status=status, selected_genre = sortGenre, 
        selected_status = sortStatus, selected_category = sortCategory, selected_platforms=sortPlatform)



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
    sort = request.args.get('sort', 'title asc')
    reviews = db.session.query(Reviews).filter(
        Reviews.url != '')
    platform = db.session.query(Platform.id, Platform.name).filter(Platform.name != '').order_by('Platform.name')
    gameFilter = request.args.getlist('game')
    platformFilter = request.args.getlist('platform')
    games = set()
    for review in reviews:
        games.add(review.game.name)
    games = sorted(games)
    if len(platformFilter)>0:
        reviews = reviews.filter(Reviews.platform_id.in_(platformFilter)).order_by('Reviews.'+sort)
    else:
        reviews = reviews.order_by('Reviews.'+sort)
    filteredReviews = list()
    if len(gameFilter)>0:
        for review in reviews:
            if review.game.name in gameFilter:
                filteredReviews.append(review)
        pagination = Pagination(
            page=page, css_framework='foundation', per_page=9, total=len(filteredReviews), record_name='items')
        return render_template('reviews.html', items=filteredReviews[(page - 1) * 9:min(page * 9, len(filteredReviews))], games=games, pagination=pagination, platforms=platform, selected_platforms=platformFilter, selected_games=gameFilter)
    else:
        pagination = Pagination(
            page=page, css_framework='foundation',per_page=9, total=reviews.count(), record_name='items')
        return render_template('reviews.html', items=reviews[(page - 1) * 9:min(page * 9, reviews.count())], games=games, pagination=pagination, platforms=platform, selected_platforms=platformFilter, selected_games=gameFilter)


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
    sort = request.args.get('sort', 'name asc')
    filterGeneration = request.args.getlist('generation')
    if len(filterGeneration)>0:
        platforms = db.session.query(Platform).filter(
            Platform.api_id != 0 and Platform.name != '' and Platform.generation.in_(filterGeneration)).order_by('Platform.'+sort)
    else:
        platforms = db.session.query(Platform).filter(
            Platform.api_id != 0 and Platform.name != '').order_by('Platform.'+sort)
    pagination = Pagination(
        page=page, css_framework='foundation', per_page=9,total=platforms.count(), record_name='items')
    return render_template('platforms.html', items=platforms[(page - 1) * 9:min(page * 9, platforms.count())], pagination=pagination, selected_generations=filterGeneration)


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
    sort = request.args.get('sort', 'name asc')
    platformFilter = request.args.getlist('platform')
    platform = db.session.query(Platform.id, Platform.name).filter(Platform.name != '').order_by('Platform.name')
    if len(platformFilter)>0:
        studios = db.session.query(Studio).filter(
        Studio.name != '' and Studio.platform_id.in_(platformFilter)).order_by('Studio.'+sort)
    else:
        studios = db.session.query(Studio).filter(
        Studio.name != '').order_by('Studio.'+sort)
    pagination = Pagination(
        page=page, css_framework='foundation', per_page=9, total=studios.count(), record_name='items')
    return render_template('studios.html', items=studios[(page - 1) * 9:min(page * 9, studios.count())], pagination=pagination, platforms=platform, selected_platforms=platformFilter)


@app.route('/studio/<name>', methods=['GET'])
def studio_instance(name):
    """
        Renders the studio_instance page populating items
        with studio objects
    """
    studio_instance = db.session.query(Studio).get(name)
    return render_template('studio.html', title='studio_instance', items=studio_instance)


if __name__ == '__main__':
    app.run()
