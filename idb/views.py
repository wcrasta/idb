from flask import render_template
from idb import app
@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')
