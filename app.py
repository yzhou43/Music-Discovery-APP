import flask
import os
import re
import random
from dotenv import find_dotenv, load_dotenv
from lyrics import genius
from top_tracks import get_tracks
from form_fields import *
from flask_login import LoginManager, login_user, current_user, logout_user
from form_fields import *
from models import *

load_dotenv(find_dotenv())

app = flask.Flask(__name__)
app.secret_key = os.environ.get("SECRET")


# Configure database
uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = uri
db = SQLAlchemy(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
    
# Configure flask login
login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# The sign up page
@app.route("/", methods=["GET", "POST"])
def signup():

    signup_form = SignupForm()

    # Check if the sign up is successful
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        # Add the username and password to the database
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        flask.flash("You were successfully signed up! Please log in.")
        return flask.redirect(flask.url_for("login"))

    return flask.render_template("signup.html", form=signup_form)


@app.route("/login", methods=["GET", "POST"])
def login():

    login_form = LoginForm()

    # Check if the login is successful
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        if current_user.is_authenticated:
            return flask.redirect(flask.url_for("index"))
        else:
            return "Failed to log in"

    return flask.render_template("login.html", form=login_form)


# User log out
@app.route("/logout", methods=["GET"])
def logout():

    logout_user()
    flask.flash("You have logged out successfully")
    return flask.redirect(flask.url_for("login"))


@app.route("/index", methods=["GET", "POST"])
def index():
    if flask.request.method == "POST":
        artist_id = flask.request.form.get("artist_id")
        # Check if the input is correct
        if not get_tracks(artist_id):
            flask.flash("The artist ID is incorrect!")
        elif Artist.query.filter_by(
            artistid=artist_id, user_id=current_user.id
        ).first():
            # flask.flash("The artist ID is already saved!")
            pass
        else:
            # Add favorite artists
            artist_new = Artist(artistid=artist_id, user_id=current_user.id)
            db.session.add(artist_new)
            db.session.commit()

    if not Artist.query.filter_by(user_id=current_user.id).first():
        return flask.render_template(
            "index.html",
            empty=True,
            user=current_user.username,
        )

    artists_list = Artist.query.filter_by(user_id=current_user.id).all()
    artists = []
    for item in artists_list:
        artists.append(item.artistid)

    rand_artist = random.randint(0, len(artists) - 1)
    artist = artists[rand_artist]

    # Get an Artist's Top Tracks
    song_info = get_tracks(artist)
    name = song_info["name"]

    # use the genius API
    lyrics_url, artist_img, artist_url, name_genius = genius(name)
    # its song name, song artist, song-related image, song preview URL
    return flask.render_template(
        "index.html",
        user=current_user.username,
        name=name,
        artist=song_info["album"]["artists"][0]["name"],
        preview=song_info["preview_url"],
        img=song_info["album"]["images"][0]["url"],
        lyrics_url=lyrics_url,
        artist_img=artist_img,
        artist_url=artist_url,
        name_genius=name_genius,
        empty=False,
    )


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
