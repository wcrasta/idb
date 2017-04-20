from models import app
from flask import Flask, render_template, jsonify
from flask import request, send_file
from flask_paginate import Pagination
from sqlalchemy import func, or_
import os
import json
import time
import subprocess
from subprocess import call
import sys
import binascii


from flask_sqlalchemy import SQLAlchemy

from models import Game, Platform, Reviews, Studio, app, db, api, Resource

POSTS_PER_PAGE = 10


# Api portions
class Api_Games(Resource):

    def get(self):
        gamelist = []
        listholder = Game.query.filter(Game.name != "").order_by(Game.id).all()
        for i in listholder:
            temp_dict = {}
            temp_dict['id'] = i.id
            temp_dict['name'] = i.name
            gamelist += [temp_dict]
        return jsonify(gamelist)


class Api_Game(Resource):

    def get(self, id):
        game = Game.query.get(id)
        temp_list = []
        reviews = Reviews.query.filter(Reviews.game_id == id).all()
        for x in reviews:
            temp_list += [x.id]
        return jsonify(
            {"id": game.id, "name": game.name, "summary": game.summary, "genre": game.genre, "rating": game.rating, "storyline": game.storyline, "category": game.category, "ESRB": game.esrb, "status": game.status, "platform_id": game.platform_id,
             "studio_id": game.studio_id, "image": game.image, "release_date": game.release_date, "website": game.website, "reviews": temp_list})


api.add_resource(Api_Games, '/api/games')
api.add_resource(Api_Game, '/api/games/<int:id>')


class Api_Platforms(Resource):

    def get(self):
        platformlist = []
        listholder = Platform.query.filter(
            Platform.name != "").order_by(Platform.id).all()
        for i in listholder:
            temp_dict = {}
            temp_dict['id'] = i.id
            temp_dict['name'] = i.name
            platformlist += [temp_dict]
        return jsonify(platformlist)


class Api_Platform(Resource):

    def get(self, id):
        platform = Platform.query.get(id)
        temp_list = []
        studios = Studio.query.filter(Studio.platform_id == id).all()
        for x in studios:
            temp_list += [x.id]
        if platform.name == "":
            return "Not a valid entry"
        return jsonify(
            {"id": platform.id, "name": platform.name, "summary": platform.summary, "created_at": platform.created_at,
             "generation": platform.generation, "image": platform.image, "website": platform.website, "studios": temp_list})


api.add_resource(Api_Platforms, '/api/platforms')
api.add_resource(Api_Platform, '/api/platforms/<int:id>')


class Api_Studios(Resource):

    def get(self):
        studiolist = []
        listholder = Studio.query.filter(
            Studio.name != "").order_by(Studio.id).all()
        for i in listholder:
            temp_dict = {}
            temp_dict['id'] = i.id
            temp_dict['name'] = i.name
            studiolist += [temp_dict]
        return jsonify(studiolist)


class Api_Studio(Resource):

    def get(self, id):
        studio = Studio.query.get(id)
        temp_list = []
        games = Game.query.filter(Game.studio_id == id).all()
        for x in games:
            temp_list += [x.id]
        if studio.name == "":
            return "Not a valid entry"
        return jsonify(
            {"id": studio.id, "name": studio.name, "platform_id": studio.platform_id,
             "description": studio.description, "created_at": studio.created_at, "website": studio.website, "games": temp_list})


api.add_resource(Api_Studios, '/api/studios')
api.add_resource(Api_Studio, '/api/studios/<int:id>')


class Api_Reviews(Resource):

    def get(self):
        reviewlist = []
        listholder = Reviews.query.filter(
            Reviews.title != "None").order_by(Reviews.id).all()
        for i in listholder:
            temp_dict = {}
            temp_dict['id'] = i.id
            temp_dict['name'] = i.title
            if(i.game_id != None):
                temp_dict['game_name'] = Game.query.get(i.game_id).name
            reviewlist += [temp_dict]
        return jsonify(reviewlist)


class Api_Review(Resource):

    def get(self, id):
        review = Reviews.query.get(id)
        if review.title == "None":
            return "Not a valid entry"
        return jsonify(
            {"id": review.id, "title": review.title, "platform_id": review.platform_id,
             "game_id": review.game_id, "created_at": review.created_at,
             "views": review.views, "video": review.video, "introduction": review.introduction,
             "content": review.content, "conclusion": review.conclusion,
             "positive": review.positive, "negative": review.negative, "url": review.url})


api.add_resource(Api_Reviews, '/api/reviews')
api.add_resource(Api_Review, '/api/reviews/<int:id>')


def orSearch(items):

    gameResults = set()
    platformResults = set()
    studioResults = set()
    reviewsResults = set()
    for i in items.split(" "):
        caseSensitive = "%" + i + "%"
        print(caseSensitive)
        mod = Game.query.whoosh_search(items, or_=True).filter(
            or_(Game.name.ilike(caseSensitive), Game.summary.ilike(caseSensitive),
                Game.genre.ilike(
                    caseSensitive), Game.storyline.ilike(caseSensitive),
                Game.esrb.ilike(caseSensitive), Game.status.ilike(caseSensitive))
        ).all()
        for m in mod:
            gameResults.add(m)

        mod1 = Platform.query.whoosh_search(items, or_=True).filter(
            or_(Platform.name.ilike(caseSensitive), Platform.summary.ilike(caseSensitive),
                Platform.image.ilike(caseSensitive), Platform.website.ilike(caseSensitive))
        )
        for m in mod1:
            platformResults.add(m)

        mod2 = Studio.query.whoosh_search(items, or_=True).filter(
            or_(Studio.name.ilike(caseSensitive), Studio.logo.ilike(caseSensitive),
                Studio.description.ilike(caseSensitive), Studio.website.ilike(caseSensitive))
        )
        for m in mod2:
            studioResults.add(m)

        mod3 = Reviews.query.whoosh_search(items, or_=True).filter(
            or_(Reviews.title.ilike(caseSensitive), Reviews.video.ilike(caseSensitive),
                Reviews.introduction.ilike(
                    caseSensitive), Reviews.content.ilike(caseSensitive),
                Reviews.conclusion.ilike(
                    caseSensitive), Reviews.positive.ilike(caseSensitive),
                Reviews.negative.ilike(caseSensitive), Reviews.url.ilike(caseSensitive))
        ).all()
        for m in mod3:
            reviewsResults.add(m)


    return [list(gameResults)[0:400], list(platformResults)[0:400], list(studioResults)[0:400], list(reviewsResults)[0:400]]


def andSearch(items):
    itemlist = items.split(" ")
    gameResults = Game.query.whoosh_search(items)
    platformResults = Platform.query.whoosh_search(items)
    studioResults = Studio.query.whoosh_search(items)
    reviewsResults = Reviews.query.whoosh_search(items)
    for i in items.split(" "):
        caseSensitive = "%" + i + "%"
        gameResults = gameResults.filter(
        or_(Game.name.ilike(caseSensitive), Game.summary.ilike(caseSensitive),
            Game.genre.ilike(caseSensitive), Game.storyline.ilike(caseSensitive),
            Game.esrb.ilike(caseSensitive), Game.status.ilike(caseSensitive))
        )

        platformResults = platformResults.filter(
            or_(Platform.name.ilike(caseSensitive), Platform.summary.ilike(caseSensitive),
                Platform.image.ilike(caseSensitive), Platform.website.ilike(caseSensitive))
        )

        studioResults = studioResults.filter(
            or_(Studio.name.ilike(caseSensitive), Studio.logo.ilike(caseSensitive),
                Studio.description.ilike(caseSensitive), Studio.website.ilike(caseSensitive))
        )

        reviewsResults = reviewsResults.filter(
            or_(Reviews.title.ilike(caseSensitive), Reviews.video.ilike(caseSensitive),
                Reviews.introduction.ilike(
                    caseSensitive), Reviews.content.ilike(caseSensitive),
                Reviews.conclusion.ilike(
                    caseSensitive), Reviews.positive.ilike(caseSensitive),
                Reviews.negative.ilike(caseSensitive), Reviews.url.ilike(caseSensitive))
        )

    return [gameResults[:400], platformResults[:400], studioResults[:400], reviewsResults[0:400]]


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# @app.route('/presentation')
# def presentation():
#     """
#         Renders the presentation page
#     """
#     with open ("presentation.pdf", "rb") as f:
#         return send_file(f, attachment_filename='file.pdf', as_attachment=True)


@app.route('/visualization')
def visualization():
    """
        Renders the visualization page
    """
    return render_template('visualization.html')


@app.route('/search', methods=["GET"])
def search(typeSearch=None):
    searchA = request.args.get('searchAnd')

    searchO = request.args.get('searchOr')

    searched = ""
    results = []

    if searchA == None or len(searchA) == 0:
        results = orSearch(searchO)
        searched = searchO
    else:
        results = andSearch(searchA)
        searched = searchA

    return render_template('search.html', platforms=results[1], studios=results[2], reviews=results[3], games=results[0], wordsSearched=searched)


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
    subprocess.call(
        "coverage run    --branch --include=tests.py tests.py > tests.out 2>&1", shell=True)
    subprocess.call("coverage report -m >> tests.out", shell=True)
    with open("tests.out", "r") as f:
        output = f.read()
    result = ""
    for char in output:
        result += char
        if(char == '\n'):
            result += "<br>"

    return result


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
    # Appended None to the dictionaries as dummies
    platform = db.session.query(Platform.id, Platform.name).filter(
        Platform.name != '').order_by('Platform.name')
    genre = {33: "Arcade", 32: "Indie", 31: "Adventure", 30: "Pinball", 26: "Quiz/Trivia", 25: "Hack and slash/Beat 'em up", 24: "Tactical", 16:
             "Turn-based strategy (TBS)", 15: "Strategy", 14: "Sport", 13: "Simulator", 12: "Role-playing (RPG)", 11: "Real Time Strategy (RTS)", 10: "Racing", 9: "Puzzle", 8: "Platform", 7: "Music", 5: "Shooter", 4: "Fighting", 2: "Point-and-click", 99: "None"}
    genre = genre.values()
    status = {0: "Released", 2: "Alpha", 3: "Beta",
              4: "Early Access", 5: "offline", 6: "Cancelled", 99: "None"}
    status = status.values()
    esrb = {1: "RP", 2: "EC", 3: "E", 4:
            "E10+", 5: "T", 6: "M", 7: "AO", 8: "None"}
    esrb = esrb.values()
    category = {0: "Main Game", 1: "DLC/Add on", 2:
                "Expansion", 3: "Bundle", 4: "Standalone expansion", 5: "None"}
    category = category.values()

    # Use so the first time the page is loaded, the things will be unchecked
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
    genreTemp = sortGenre
    statusTemp = sortStatus
    esrbTemp = sortEsrb
    categoryTemp = sortCategory
    platformTemp = sortPlatform
    if not sortPlatform:
        sortPlatform = db.session.query(Platform.id)
    if not sortGenre:
        sortGenre = genre
    if not sortStatus:
        sortStatus = status
    if not sortEsrb:
        sortEsrb = esrb
    if not sortCategory:
        sortCategory = category

    if len(platformTemp) > 0:
        games = db.session.query(Game).filter(Game.platform_id.in_(sortPlatform)).filter(Game.genre.in_(sortGenre)).filter(
            Game.status.in_(sortStatus)).filter(Game.category.in_(sortCategory)).filter(Game.esrb.in_(sortEsrb)).order_by(('Game.' + sort))
    else:
        games = db.session.query(Game).filter(Game.api_id != 0 and Game.name != '').filter(Game.genre.in_(sortGenre)).filter(
            Game.status.in_(sortStatus)).filter(Game.category.in_(sortCategory)).filter(Game.esrb.in_(sortEsrb)).order_by(('Game.' + sort))
    pagination = Pagination(
        page=page, css_framework='foundation', total=games.count(), per_page=9, record_name='items')

    return render_template(
        'games.html', items=games.limit(9).offset((page - 1) * 9), pagination=pagination, genreTemp=genreTemp, esrbTemp=esrbTemp, categoryTemp=categoryTemp,
        statusTemp=statusTemp, esrb=esrb, selected_esrb=sortEsrb, platforms=platform, genre=genre, category=category, status=status, selected_genre=sortGenre,
        selected_status=sortStatus, selected_category=sortCategory, selected_platforms=sortPlatform)


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
    platform = db.session.query(Platform.id, Platform.name).filter(
        Platform.name != '').order_by('Platform.name')
    gameFilter = request.args.getlist('game')
    platformFilter = request.args.getlist('platform')
    games = set()
    for review in reviews:
        games.add(u'' + review.game.name)
    games = sorted(games)
    if len(platformFilter) > 0:
        reviews = reviews.filter(
            Reviews.platform_id.in_(platformFilter)).order_by('Reviews.' + sort)
    else:
        reviews = reviews.order_by('Reviews.' + sort)
    filteredReviews = list()
    if len(gameFilter) > 0:
        for review in reviews:
            if review.game.name in gameFilter:
                filteredReviews.append(review)
        pagination = Pagination(
            page=page, css_framework='foundation', per_page=9, total=len(filteredReviews), record_name='items')
        return render_template('reviews.html', items=filteredReviews[(page - 1) * 9:min(len(filteredReviews), page * 9)], games=games, pagination=pagination, platforms=platform, selected_platforms=platformFilter, selected_games=gameFilter)
    else:
        pagination = Pagination(
            page=page, css_framework='foundation', per_page=9, total=reviews.count(), record_name='items')
        return render_template('reviews.html', items=reviews.limit(9).offset((page - 1) * 9), games=games, pagination=pagination, platforms=platform, selected_platforms=platformFilter, selected_games=gameFilter)


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
    if len(filterGeneration) > 0:
        platforms = db.session.query(Platform).filter(
            Platform.api_id != 0 and Platform.name != '' and Platform.generation.in_(filterGeneration)).order_by('Platform.' + sort)
    else:
        platforms = db.session.query(Platform).filter(
            Platform.api_id != 0 and Platform.name != '').order_by('Platform.' + sort)
    pagination = Pagination(
        page=page, css_framework='foundation', per_page=9, total=platforms.count(), record_name='items')
    return render_template('platforms.html', items=platforms.limit(9).offset((page - 1) * 9), pagination=pagination, selected_generations=filterGeneration)


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
    platform = db.session.query(Platform.id, Platform.name).filter(
        Platform.name != '').order_by('Platform.name')
    if len(platformFilter) > 0:
        studios = db.session.query(Studio).filter(
            Studio.name != '' and Studio.platform_id.in_(platformFilter)).order_by('Studio.' + sort)
    else:
        studios = db.session.query(Studio).filter(
            Studio.name != '').order_by('Studio.' + sort)
    pagination = Pagination(
        page=page, css_framework='foundation', per_page=9, total=studios.count(), record_name='items')
    return render_template('studios.html', items=studios.limit(9).offset((page - 1) * 9), pagination=pagination, platforms=platform, selected_platforms=platformFilter)


@app.route('/studio/<name>', methods=['GET'])
def studio_instance(name):
    """
        Renders the studio_instance page populating items
        with studio objects
    """
    studio_instance = db.session.query(Studio).get(name)
    return render_template('studio.html', title='studio_instance', items=studio_instance)


@app.route('/flare', methods=['GET'])
def flare_instance():
    return render_template('flare.json')

if __name__ == '__main__':
    app.run(threaded=True)
