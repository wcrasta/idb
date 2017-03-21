from app import db

#gameToPlatform = db.Table('gamestoplatform', db.Column('game_id', db.Integer, db.ForeignKey(
#    'game.id')), db.Column('platform_id', db.Integer, db.ForeignKey('platform.id')))


studioToPlatform = db.Table('studioToPlatform', db.Column('studio_id', db.Integer, db.ForeignKey(
    'studio.id')), db.Column('platform_id', db.Integer, db.ForeignKey('platform.id')))

genres={33:"Arcade", 32:"Indie", 31:"Adventure", 30:"Pinball", 26:"Quiz/Trivia", 25:"Hack and slash/Beat 'em up", 24:"Tactical", 16:"Turn-based strategy (TBS)", 15:"Strategy", 14:"Sport", 13:"Simulator", 12:"Role-playing (RPG)",11:"Real Time Strategy (RTS)", 10:"Racing", 9:"Puzzle", 8:"Platform", 7:"Music", 5:"Shooter", 4:"Fighting", 2:"Point-and-click"}

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)


    genre = db.Column(db.String(80))

    studio_id = db.Column(db.Integer, db.ForeignKey('studio.id'))

    reviews = db.relationship('Reviews', backref='game')

    image = db.Column(db.LargeBinary)
    release_date = db.Column(db.DateTime)
    website = db.Column(db.String(80))

    # def __init__(self, name, platform = None, genre=None, studio=None, reviews=None, image=None, release_date=None, website=None):
    #     self.name = name
    #     #self.platform = platform
    #     if genre:
    #         self.genre = genres[genre[0]]
    #     if studio:
    #         self.studio = studio
    #     if reviews:
    #         self.reviews = reviews
    #     if image:
    #         self.image = image
    #     if release_date:
    #         self.release_date = release_date
    #     if website:
    #         self.website = website
    #
    # def __repr__(self):
    #     return "<Game(name='%s',game_studio='%s', genres='%s', release_date='%s', website = '%s')>" % (self.name, self.studio.name, self.genre, self.release_date, self.website)

class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    summary = db.Column(db.Text)
    review = db.relationship('Reviews', backref='platform')
    # discuss relationship of game
    # games =

    image = db.Column(db.LargeBinary)
    website = db.Column(db.String(80))

    # def __init__(self, name, summary=None, image=None, website=None):
    #     self.name = name
    #     self.summary = summary
    #     self.image = image
    #     self.website = website
    #
    # def __repr__(self):
    #     print("Platform name: " + self.name)
    #     return '<Platform %r>'%self.name

class Studio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    logo = db.Column(db.LargeBinary, nullable = True)
    description = db.Column(db.Text, nullable = True)
    game = db.relationship('Game', backref = 'studio')
    platform = db.relationship(
        'Platform', secondary=studioToPlatform, backref=db.backref('studio', lazy='dynamic'))

    # Game is taken care of up in class Game
    # def __init__(self, name, logo=None, description=None, platform=None):
    #     self.name = name
    #     self.logo = logo
    #     self.description = description
    #     self.platform = platform
    #
    # def __repr__(self):
    #     print("Studio name: " + self.name)


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True)

    # need to discuss
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"))
    #platform = db.relationship('Platform', backref="reviews")
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

    introduction = db.Column(db.Text, nullable = True)
    content = db.Column(db.Text)
    conclusion = db.Column(db.Text)
    positive = db.Column(db.Text)
    negative = db.Column(db.Text)
    url = db.Column(db.String(80))

    # def __init__(self, title, introduction=None, content=None, conclusion=None, positive=None, negative=None, url=None):
    #     self.title = title
    #     self.introduction = introduction
    #     self.content = content
    #     self.conclusion = conclusion
    #     self.positive = positive
    #     self.negative = negative
    #     self.url = url
    #
    # def __repr__(self):
    #     print("Review title: " + self.title)
