from flask_whooshalchemyplus import index_all
from models import app

with app.app_context():
    index_all(app)
