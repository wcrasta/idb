from app import db

class Game(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique = True)

	#Need to disuss how Genre is implemented
	genre = db.Column(db.String(80))
	studio = db.relationship('Studio', backref='Game', lazy='dynamic')
	image = db.Column(db.LargeBinary)
	release_date = db.Column(db.DateTime)
	reviews = db.Column(db.Text)
	website = db.Column(db.String(80))

	def __init__(self):
		pass

	def __repr__(self):
		pass

class Platform(db.Model):
	name = db.Column(db.String(80), unique = True)
	summary = db.Column(db.Text)
	
	#discuss relationship of game
	#games = 

	image = db.Column(db.LargeBinary)
	website = db.Column(db.String(80))

class Studio(db.Model):
	name = db.Column(db.String(80), unique = True)
	logo = db.Column(db.LargeBinary)
	description = db.Column(db.Text)
	
	#need to discuss
	#published_games =
	#platforms = 

class Reviews(db.Model):
	title = db.Column(db.String(128), unique = True)
	
	#need to discuss
	#game
	#platform

	introduction = db.Column(db.Text)
	content = db.Column(db.Text)
	conclusion = db.Column(db.Text)
	positive = db.Column(db.Text)
	negative = db.Column(db.Text)
	url = db.Column(db.String(80))
