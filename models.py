from app import db

#gameToPlatform = db.Table('gamestoplatform', db.Column('game_id', db.Integer, db.ForeignKey(
#    'game.id')), db.Column('platform_id', db.Integer, db.ForeignKey('platform.id')))


#studioToPlatform = db.Table('studioToPlatform', db.Column('studio_id', db.Integer, db.ForeignKey(
#    'studio.id')), db.Column('platform_id', db.Integer, db.ForeignKey('platform.id')))

genres={33:"Arcade", 32:"Indie", 31:"Adventure", 30:"Pinball", 26:"Quiz/Trivia", 25:"Hack and slash/Beat 'em up", 24:"Tactical", 16:"Turn-based strategy (TBS)", 15:"Strategy", 14:"Sport", 13:"Simulator", 12:"Role-playing (RPG)",11:"Real Time Strategy (RTS)", 10:"Racing", 9:"Puzzle", 8:"Platform", 7:"Music", 5:"Shooter", 4:"Fighting", 2:"Point-and-click"}

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    api_id = db.Column(db.Integer)
    summary = db.Column(db.Text)

    genre = db.Column(db.String(80))


    studio_id = db.Column(db.Integer, db.ForeignKey('studio.id'))

    reviews = db.relationship('Reviews', backref='game')

    #image = db.Column(db.LargeBinary)
    image = db.Column(db.String(128))
    release_date = db.Column(db.DateTime)
    website = db.Column(db.String(80))

class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer)

    name = db.Column(db.String(80), unique=True)
    summary = db.Column(db.Text)
    review = db.relationship('Reviews', backref='platform')
    # discuss relationship of game
    # games =

    #image = db.Column(db.LargeBinary)
    image = db.Column(db.String(128))
    website = db.Column(db.String(80))


class Studio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    #logo = db.Column(db.LargeBinary, nullable = True)
    logo = db.Column(db.String(128))
    description = db.Column(db.Text, nullable = True)
    game = db.relationship('Game', backref = 'studio')


#    platform = db.relationship(
#        'Platform', secondary=studioToPlatform, backref=db.backref('studio', lazy='dynamic'))

class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))

    # need to discuss
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"))
    #platform = db.relationship('Platform', backref="reviews")
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    created_at = db.Column(db.DateTime)
    views = db.Column(db.Integer)

    introduction = db.Column(db.Text, nullable = True)
    content = db.Column(db.Text)
    conclusion = db.Column(db.Text)
    positive = db.Column(db.Text)
    negative = db.Column(db.Text)
    url = db.Column(db.String(80))
