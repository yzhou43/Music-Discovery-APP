import flask
import os
from dotenv import find_dotenv, load_dotenv
from lyrics import genius
from top_tracks import get_tracks

load_dotenv(find_dotenv())

artists = ["06HL4z0CvFAxyc27GXpf02", "43ZHCT0cAZBISjO8DG9PnE", "41MozSoPIsD1dJM0CLPjZF"]

app = flask.Flask(__name__)

@app.route("/")  # Python decorator
def main():
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
