# GGnoSWE

A web application, about video games, created by a group of 6 (Kaden Brown, Zihao Zhu, Warren Crasta, Colin Thornton, Anurag Papineni, and Kaivan Shah) as a project for [CS 373: Software Engineering](http://www.cs.utexas.edu/users/downing/cs373/).

Previously available at http://ggnoswe.me. The website was taken down on May 12, 2017 due to our AWS Free Tier expiring. To run the website on a Flask server locally, see **How to Run** below.

**Key Technologies Used:** AWS EC2 to host all content, Apache web server, AWS RDS (PostgreSQL) + SQLite for database, Python + Flask for backend, Bootstrap + React for frontend. See the "About" page and our Technical Report, both located in our repo, for more information regarding technologies/tools that were used.

## How to Run

1. Clone this repository. `git clone https://github.com/wcrasta/idb.git`
2. Make sure you have Python (code was tested for 3.5, might work with 2.7) and pip. Install required modules by `pip install -r app/requirements.txt`
3. Run the web application with `python app/__init__.py`. Our database was hosted through AWS RDS, which we shut down due to free tier expiring. Instead, you can edit **app/models.py** to use a local database, found at **app/app.db**.
