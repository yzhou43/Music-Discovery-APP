import flask
import requests
import os

# use the genius api
genius_access_token = os.getenv("genius_access_token")

# search for the lyrics
def genius(name):
    genius_search_url = (
        f"http://api.genius.com/search?q={name}&access_token={genius_access_token}"
    )
    try:
        lyrics = requests.get(genius_search_url)
        lyrics_json = lyrics.json()
        lyrics_url = lyrics_json["response"]["hits"][0]["result"]["url"]
        artist_img = lyrics_json["response"]["hits"][0]["result"]["primary_artist"][
            "image_url"
        ]
        artist_url = lyrics_json["response"]["hits"][0]["result"]["primary_artist"][
            "url"
        ]
        name_genius = lyrics_json["response"]["hits"][0]["result"]["primary_artist"][
            "name"
        ]
    except:
        return flask.render_template(
            "error.html", error_state="Failed to fetch the lyrics page!"
        )
    return lyrics_url, artist_img, artist_url, name_genius
