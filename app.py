import flask
import requests
import os
import random
from dotenv import find_dotenv, load_dotenv
from lyrics import genius

load_dotenv(find_dotenv())


CLIENT_ID = 'a0e467772f0c481b9810cf2b5abc094a'

AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': os.getenv("CLIENT_SECRET")
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

artists = ['06HL4z0CvFAxyc27GXpf02', '43ZHCT0cAZBISjO8DG9PnE',
           '41MozSoPIsD1dJM0CLPjZF']

app = flask.Flask(__name__)


@app.route("/")  # Python decorator
def main():
    # Get an Artist's Top Tracks
    rand_artist = random.randint(0, len(artists)-1)
    try:
        toptrack = requests.get('https://api.spotify.com/v1/artists/%s/top-tracks' %
                                artists[rand_artist], headers=headers, params={'market': 'US'})
        toptrack_json = toptrack.json()
        rand_song = random.randint(0, len(toptrack_json['tracks'])-1)
        song_info = toptrack_json['tracks'][rand_song]
        name = song_info['name']
    except:
          return flask.render_template("error.html", error_state='Failed to get the song\'s infomation!') 
    
    # use the genius API
    lyrics_url, artist_img, artist_url, name_genius = genius(name)
    # its song name, song artist, song-related image, song preview URL
    return flask.render_template("index.html", name=name, artist=song_info['album']['artists'][0]['name'],
                                 preview=song_info['preview_url'], img=song_info['album']['images'][0]['url'],
                                lyrics_url=lyrics_url, artist_img=artist_img, artist_url=artist_url,
                                name_genius=name_genius)


app.run(
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080)),
    debug=True
)
