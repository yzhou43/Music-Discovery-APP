import flask
import requests
import os
import random
from dotenv import find_dotenv, load_dotenv

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
           '6qqNVTkY8uBg9cP3Jd7DAH', '66CXWjxzNUsdJxJ2JdwvnR']

# use the genius api
genius_access_token = '4paquYljmAe_uvMWGtnGa8ebLJgUHwVM7ite6KxlLMizZonJj6nOQcdYO7Tj80qq'

app = flask.Flask(__name__)


@app.route("/")  # Python decorator
def main():
    # Get an Artist's Top Tracks
    rand_artist = random.randint(0, len(artists)-1)
    toptrack = requests.get('https://api.spotify.com/v1/artists/%s/top-tracks' %
                            artists[rand_artist], headers=headers, params={'market': 'US'})
    toptrack_json = toptrack.json()
    print(toptrack.status_code)
    rand_song = random.randint(0, len(toptrack_json['tracks'])-1)
    song_info = toptrack_json['tracks'][rand_song]
    name = song_info['name']
    # search for the lyrics
    genius_search_url = f"http://api.genius.com/search?q={name}&access_token={genius_access_token}"
    lyrics = requests.get(genius_search_url)
    lyrics_json = lyrics.json()
    lyrics_url = lyrics_json['response']['hits'][0]['result']['url']
    # its song name, song artist, song-related image, song preview URL
    return flask.render_template("index.html", name=name, artist=song_info['album']['artists'][0]['name'],
                                 preview=song_info['preview_url'], img=song_info['album']['images'][0]['url'],
                                lyrics_url=lyrics_url )


app.run(
    debug=True
)
