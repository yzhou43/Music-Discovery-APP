import requests
import os
import random
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

AUTH_URL = "https://accounts.spotify.com/api/token"

# POST
auth_response = requests.post(
    AUTH_URL,
    {
        "grant_type": "client_credentials",
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
    },
)

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data["access_token"]

headers = {"Authorization": "Bearer {token}".format(token=access_token)}


def get_tracks(artist):
    # Get an Artist's Top Tracks
    try:
        toptrack = requests.get(
            "https://api.spotify.com/v1/artists/%s/top-tracks" % artist,
            headers=headers,
            params={"market": "US"},
        )
        toptrack_json = toptrack.json()
        rand_song = random.randint(0, len(toptrack_json["tracks"]) - 1)
        song_info = toptrack_json["tracks"][rand_song]
    except:
        return None
    return song_info
