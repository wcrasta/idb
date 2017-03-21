#!flask/bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path

db.create_all()

if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(
        SQLALCHEMY_MIGRATE_REPO))

"""from models import *
>>> game1=Game()
>>> studio1=Game()
>>> game1.name
>>> game1.name = "Zelda"
>>> game1.name
'Zelda'
>>> game1.genre = "Adventure"
>>> import datetime
>>> game1.release_date = datetime.datetime.utcnow
>>> game1.website = "www.zelda.com"
>>> stdio2 = Studio()
>>> stdio2.name = "Nintendo"
>>> stdio2.game = game1
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/zihaozhu/Desktop/sem6/softwareEngineering/project3/idb/flask/lib/python3.4/site-packages/sqlalchemy/orm/attributes.py", line 224, in __set__
    instance_dict(instance), value, None)
  File "/Users/zihaozhu/Desktop/sem6/softwareEngineering/project3/idb/flask/lib/python3.4/site-packages/sqlalchemy/orm/attributes.py", line 1049, in set
    given, wanted))
TypeError: Incompatible collection type: Game is not list-like
>>> stdio2.game.append(game1)
>>> game1.studio
<models.Studio object at 0x103dfac50>
>>> game1.studio.name
'Nintendo'
>>> db.session.add(game1)
>>> db.session.add(stdio2)
>>> db.session.commit()"""
