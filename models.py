from database import db
#from app import db



class Game(db.Model):
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

    #image = db.Column(db.LargeBinary)
    image = db.Column(db.String(128))
    release_date = db.Column(db.DateTime)
    website = db.Column(db.String(80))

class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer)

    created_at = db.Column(db.DateTime)
    name = db.Column(db.String(80))
    summary = db.Column(db.Text)
    games = db.relationship('Game', backref='platform', lazy="dynamic")
    review = db.relationship('Reviews', backref='platform', lazy="dynamic")
    # discuss relationship of game
    # games =
    generation = db.Column(db.Integer)
    #image = db.Column(db.LargeBinary)
    image = db.Column(db.String(128))
    website = db.Column(db.String(80))
    studio = db.relationship('Studio', backref='platform',lazy="dynamic")


class Studio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    #logo = db.Column(db.LargeBinary, nullable = True)

    #platform = db.Column(db.String(128))
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))

    logo = db.Column(db.String(128))
    description = db.Column(db.Text, nullable = True)
    game = db.relationship('Game', backref = 'studio', lazy= "dynamic")
    created_at = db.Column(db.DateTime)
    website = db.Column(db.String(128))

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

    video = db.Column(db.String(128))
    introduction = db.Column(db.Text, nullable = True)
    content = db.Column(db.Text)
    conclusion = db.Column(db.Text)
    positive = db.Column(db.Text)
    negative = db.Column(db.Text)
    url = db.Column(db.String(80))
