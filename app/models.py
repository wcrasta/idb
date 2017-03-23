from database import db
#from app import db



class Game(db.Model):
    """
        Game model represents the various games and contains information
        regarding their names, esrb ratings, ratings, status, website, images
        and more. It has relationships with other models like studio, reviews
        and companies.
    """

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

    image = db.Column(db.String(128))
    release_date = db.Column(db.DateTime)
    website = db.Column(db.String(80))

class Platform(db.Model):
    """
        Platform is a model that represents the various video game consoles that exist
        and it contains information regarding the games the console supports,
        the reviews of the console, the generation, image, website and etc.
        Platform models also have relationships with the other models such as 
        game, review and studio.
    """

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
    studio = db.relationship('Studio', backref='platform',lazy="dynamic")


class Studio(db.Model):
    """
        Studio is a model that represents the companies that publish and develop
        video games. Studios have informatino regarding the name, the logo, the games
        they built/published, the website and etc. 
        Studio models have relationships with game, platform and reviews.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))

    logo = db.Column(db.String(128))
    description = db.Column(db.Text, nullable = True)
    game = db.relationship('Game', backref = 'studio', lazy= "dynamic")
    created_at = db.Column(db.DateTime)
    website = db.Column(db.String(128))

class Reviews(db.Model):
    """
        Reviews is a model that represents the consumer reviews of various
        games that involve discussing the console the game is on and the company
        that built it. Reviews contain information regarding the title,
        the number of views of the review, website, and written contents
        such as introduction, content and conclusion.
        Reviews have relationships with game,platform and studios.
    """    

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))

    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"))
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