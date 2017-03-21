from models import *
from app import db
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import json
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData

#conn = sqlite3.connect('app.db')
genres={33:"Arcade", 32:"Indie", 31:"Adventure", 30:"Pinball", 26:"Quiz/Trivia", 25:"Hack and slash/Beat 'em up", 24:"Tactical", 16:"Turn-based strategy (TBS)", 15:"Strategy", 14:"Sport", 13:"Simulator", 12:"Role-playing (RPG)",11:"Real Time Strategy (RTS)", 10:"Racing", 9:"Puzzle", 8:"Platform", 7:"Music", 5:"Shooter", 4:"Fighting", 2:"Point-and-click"}


#To do : For each one that has the relationship() call, make a new
# variable that actually displays everything
#Discuss studio to platform
#Check github issues for platform?
#add platform and etc in game (maybe can do this while rendering)

def reviews():
    with open('reviews.json',encoding='UTF-8') as data_file:
        data = json.load(data_file)
        for entry in data:
            name = "None"
            if 'title' in entry:
                name = entry['title']


            if 'created_at' in entry:
                ts = datetime.datetime.fromtimestamp(entry['created_at']/1000)


            view = 0
            if 'views' in entry:
                view = entry['views']

            #need to think about platform and game

            introduction = "None"
            if 'introduction' in entry:
                introduction = entry['introduction']

            content = "None"
            if 'content' in entry:
                content = entry['content']

            conclusion = "None"
            if 'conclusion' in entry:
                conclusion = entry['conclusion']

            positive = "None"
            if 'positive_points' in entry:
                positive = entry['positive_points']

            negative = "None"
            if 'negative_points' in entry:
                negative = entry['negative_points']

            url = "None"
            if 'url' in entry:
                url = entry['url']

            review = Reviews()

            review.title = name
            review.created_at = ts
            review.views = view
            review.introduction = introduction
            review.content = content
            review.conconclusion = conclusion
            review.positive = positive
            review.negative = negative
            review.url = url
            #review game
            #review platform

            db.session.add(review)
            db.session.commit()

            if 'game' in entry:
                game1 = db.session.query(Game).filter_by(api_id=entry['game']).first()
                game1.reviews.append(review)
                db.session.commit()
            #hacky way to get around the relationship, check
            if 'platform' in entry:
                platform1 = db.session.query(Platform).filter_by(api_id=entry['platform']).first()
                platform1.review.append(review)
                db.session.commit()


def studio():
    with open('companies.json',encoding='UTF-8') as data_file:
        data = json.load(data_file)
        for entry in data:
            #print(entry)
            name = entry['name']


            #reviews
            image = "None"
            if 'logo' in entry:
                image = "https:"+entry['logo']['url']

            games = list()
            if 'developed' in entry:
                for game in entry['developed']:
                    games.append(game)
            if 'published' in entry:
                for game in entry['published']:
                    games.append(game)


            summary = "None"
            if 'description' in entry:
                summary = entry['description']
            #print(name,summary,genre,image,ts,website)
            final_game_list = list()

            for game in games:
                if db.session.query(Game).filter_by(api_id=game).scalar() is not None:
                    temp_game = db.session.query(Game).filter_by(api_id=game).first()
                    final_game_list.append(temp_game)
            studio = Studio()
            studio.name = name
            studio.logo = image
            studio.description=summary



            for x in final_game_list:
                studio.game.append(x)


            db.session.add(studio)
            db.session.commit()


def platform():
    with open('platforms.json',encoding='UTF-8') as data_file:
        data = json.load(data_file)
        for entry in data:
            #print(entry)
            name = entry['name']

            api_id = entry['id']


            #reviews

            image = "None"
            if 'url' in entry:
                image = entry['url']

            website = "None"
            if 'website' in entry:
                website = entry['website']
            summary = "None"
            if 'summary' in entry:
                summary = entry['summary']
            #print(name,summary,genre,image,ts,website)
            platform = Platform()
            platform.api_id = api_id
            platform.name = name
            platform.image = image
            platform.website = website
            platform.summary=summary
            db.session.add(platform)
            db.session.commit()


def game():
    with open('games.json',encoding='UTF-8') as data_file:
        data = json.load(data_file)
        for entry in data:
            #print(entry)
            name = entry['name']

            api_id = entry['id']
            if 'genres' in entry:
                genre = genres[entry['genres'][0]]
            #reviews
            image = "None"
            if 'cover' in entry:
                image = "https:"+entry['cover']['url']

            #do platform and studio?
            #platform = ['platform']

            if 'first_release_date' in entry:
                ts = datetime.datetime.fromtimestamp(entry['first_release_date']/1000)

            website = "None"
            if 'url' in entry:
                website = entry['url']
            summary = "None"
            if 'summary' in entry:
                summary = entry['summary']
            #print(name,summary,genre,image,ts,website)
            game = Game()
            game.name = name

            game.api_id = api_id

            game.genre = genre
            game.image = image
            game.release_date = ts
            game.website = website
            game.summary=summary
            db.session.add(game)
            db.session.commit()

game()
platform()
reviews()
studio()
