from flask import Flask, render_template

# Create the Flask application.
app = Flask(__name__)
# app.debug = True

@app.route('/')
def index():
    return render_template('home.html')

# Run the Flask app.
if __name__ == '__main__':
    app.run()