from flask import Flask, render_template

# Create the Flask application.
app = Flask(__name__)
# app.debug = True

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about.html', methods=['GET'])
def about():
    return render_template('about.html',title = "about")

@app.route('/games.html', methods=['GET'])
def games():
    return render_template('games.html', title = "games")

@app.route('/reviews.html', methods = ['GET'])
def reviews():
    return render_template('reviews.html', title="reviews")

@app.route('/platforms.html', methods = ['GET'])
def platforms():
    return render_template('platforms.html', title='platforms')

@app.route('/studios.html', methods = ['GET'])
def studios():
    return render_template('studios.html', title='studios')

# Run the Flask app.
if __name__ == '__main__':
    app.run()
