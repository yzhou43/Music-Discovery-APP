import flask
import os
from dotenv import find_dotenv, load_dotenv
from lyrics import genius
from top_tracks import get_tracks
from form_fields import *
from flask_login import LoginManager, login_user, current_user, logout_user
from form_fields import *
from models import *

load_dotenv(find_dotenv())

artists = ["06HL4z0CvFAxyc27GXpf02", "43ZHCT0cAZBISjO8DG9PnE", "41MozSoPIsD1dJM0CLPjZF"]

app = flask.Flask(__name__)
app.secret_key=os.environ.get('SECRET')

# Configure database
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# Configure flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# The sign up page
@app.route("/", methods=['GET', 'POST'])
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

        flask.flash('You were successfully signed up! Please log in.')
        return flask.redirect(flask.url_for('login'))

    return flask.render_template("signup.html", form=signup_form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Check if the login is successful
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        if current_user.is_authenticated:
            return current_user.username
            # return flask.redirect(flask.url_for('index'))
        else:
            return "Failed to log in"

    return flask.render_template("login.html", form=login_form)

# User log out
@app.route("/logout", methods=['GET'])
def logout():

    logout_user()
    flask.flash('You have logged out successfully')
    return flask.redirect(flask.url_for('login'))
    



@app.route("/index")
def index():
    # Get an Artist's Top Tracks
    song_info = get_tracks(artists)
    name = song_info["name"]

    # use the genius API
    lyrics_url, artist_img, artist_url, name_genius = genius(name)
    # its song name, song artist, song-related image, song preview URL
    return flask.render_template(
        "index.html",
        name=name,
        artist=song_info["album"]["artists"][0]["name"],
        preview=song_info["preview_url"],
        img=song_info["album"]["images"][0]["url"],
        lyrics_url=lyrics_url,
        artist_img=artist_img,
        artist_url=artist_url,
        name_genius=name_genius,
    )


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
