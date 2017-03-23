#from models import Game, Platform, Reviews, Studio
from models import *
from app import db
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import json
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData

genres={33:"Arcade", 32:"Indie", 31:"Adventure", 30:"Pinball", 26:"Quiz/Trivia", 25:"Hack and slash/Beat 'em up", 24:"Tactical", 16:"Turn-based strategy (TBS)", 15:"Strategy", 14:"Sport", 13:"Simulator", 12:"Role-playing (RPG)",11:"Real Time Strategy (RTS)", 10:"Racing", 9:"Puzzle", 8:"Platform", 7:"Music", 5:"Shooter", 4:"Fighting", 2:"Point-and-click"}
esrbs = {1:"RP", 2:"EC", 3:"E", 4:"E10+", 5:"T", 6:"M", 7:"AO"}
game_category = { 0:"Main Game", 1:"DLC/Add on", 2:"Expansion", 3:"Bundle", 4:"Standalone expansion"}
game_status = {0:"Released", 2:"Alpha", 3:"Beta", 4:"Early Access", 5:"offline", 6:"Cancelled"}

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

            ts = datetime.datetime.now()
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

            url = ''
            if 'url' in entry:
                url = entry['url']

            video = "None"
            if 'video' in entry:
                video = 'https://www.youtube.com/embed/'+entry['video']

            review = Reviews()

            review.title = name
            review.created_at = ts
            review.views = view
            review.introduction = introduction
            review.content = content
            review.conclusion = conclusion
            review.positive = positive
            review.negative = negative

            review.video = video
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
            name = ''
            if 'name' in entry:
                name = entry['name']


            #reviews
            image = "None"
            if 'logo' in entry:
                image = "https:"+entry['logo']['url']

            games = set()
            if 'published' in entry:
                for game in entry['published']:
                    games.add(game)
            if 'developed' in entry:
                for game in entry['developed']:
                    games.add(game)

            ts = datetime.datetime.now()
            if 'created_at' in entry:
                ts = datetime.datetime.fromtimestamp(entry['created_at']/1000)

            website = "None"

            if 'website' in entry:
                website = entry['website']
            summary = "None"
            if 'description' in entry:
                summary = entry['description']
            #print(name,summary,genre,image,ts,website)
            final_game_list = list()


            platform_id = 0
            for game in games:
                temp_game = db.session.query(Game).get(game)
                if temp_game == None:
                    continue
                final_game_list.append(temp_game)
                if temp_game.platform != None:
                    platform_id = temp_game.platform_id

            studio = Studio()
            studio.name = name
            studio.logo = image
            studio.description=summary
            studio.created_at = ts
            studio.platform_id = platform_id
            studio.website = website

            for x in final_game_list:
                studio.game.append(x)


            db.session.add(studio)

            #Needs work

            for game in games:
                temp_game = db.session.query(Game).get(game)
                if temp_game == None:
                    continue
                if temp_game.platform != None:
                    temp_game.platform.studio.append(studio)
            db.session.commit()

def platform():
    with open('platforms.json',encoding='UTF-8') as data_file:
        data = json.load(data_file)
        for entry in data:

            name = ''
            if 'name' in entry:
                name = entry['name']

            api_id = 0
            if 'id' in entry:
                api_id = entry['id']

            #created_at = "None"
            ts = datetime.datetime.now()
            if 'created_at' in entry:
                ts = datetime.datetime.fromtimestamp(entry['created_at']/1000)

            generation = 0
            if 'generation' in entry:
                generation = entry['generation']
            #reviews
            games = list()
            if 'games' in entry:
                games = entry['games']


            #DO IT UNDER LOGO URL    
            image = "None"
            if 'logo' in entry:
                image = entry['logo']['url']

            website = "None"
            if 'website' in entry:
                website = entry['website']
            summary = "None"
            if 'summary' in entry:
                summary = entry['summary']

            final_game_list = list()
            for game in games:
                #("INFINITy")
                #if db.session.query(Game).filter_by(api_id=game).scalar() is not None:
                #    temp_game = db.session.query(Game).filter_by(api_id=game).first()
                temp_game = db.session.query(Game).get(game)
                if temp_game == None:
                    continue
                final_game_list.append(temp_game)
            #print(name,summary,genre,image,ts,website)
            platform = Platform()
            platform.api_id = api_id
            platform.name = name
            platform.image = image
            platform.website = website
            platform.summary=summary
            platform.created_at = ts
            platform.generation = generation

            for x in final_game_list:
                platform.games.append(x)

            db.session.add(platform)
            db.session.commit()


def game():
    with open('games.json',encoding='UTF-8') as data_file:
        data = json.load(data_file)
        for entry in data:
            #print(entry)
            name = ''
            if 'name' in entry:
                name = entry['name']
            
            api_id = 0
            if 'id' in entry:
                api_id = entry['id']

            if 'genres' in entry:
                genre = genres[entry['genres'][0]]
            #reviews
            image = "None"
            if 'cover' in entry:
                image = "https:"+entry['cover']['url']

            rating = 0
            if 'rating' in entry:
                rating = entry['rating']

            storyline = "None"
            if 'storyline' in entry:
                storyline = entry['storyline']

            category = "None"
            if 'category' in entry:
                category = game_category[entry['category']]

            esrb = "None"
            if 'esrb' in entry:
                #print (entry['esrb'])
                esrb = esrbs[entry['esrb']['rating']]

            status = "None"
            if 'status' in entry:
                status = game_status[entry['status']]

            video = "None"
            if 'videos' in entry:
                category = 'https://www.youtube.com/embed/'+entry['videos'][0]['video_id']
            #do platform and studio?
            #platform = ['platform']
            ts = datetime.datetime.now()
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
            game.rating = rating
            game.storyline = storyline
            game.category = category
            game.esrb = esrb
            game.status = status
            game.image = image
            game.release_date = ts
            game.website = website
            game.summary = summary
            game.video = video

            db.session.add(game)
            db.session.commit()

game()
print("games done")
platform()
print("platforms done")
reviews()
print("reviews done")
studio()
print("studios done")
