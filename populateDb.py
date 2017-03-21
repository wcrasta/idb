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
#engine = create_engine('sqlite:///%s' % 'app.db', echo=True)
#metadata = MetaData(bind = engine)
#Session = sessionmaker(bind=engine)
#session = Session()
#con = engine.connect()
with open('games.json',encoding='UTF-8') as data_file:
    data = json.load(data_file)
    for entry in data:
        #print(entry)
        name = entry['name']
        print(type(name))
        if 'genres' in entry:
            genre = genres[entry['genres'][0]]
        #reviews
        image = "None"
        if 'cover' in entry:
            image = "https:"+entry['cover']['url']
        #platform = ['platform']
        #release_date = entry['first_release_date']
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
        game.genre = genre
        game.image = image
        game.release_date = ts
        game.website = website
        game.summary=summary
        #game.studio_id = 0
        db.session.add(game)
        db.session.commit()
        #session.add(game)
        #print(game.name,game.genre)
        #session.commit()
