import os

import spotipy.util as util
import requests

from lfuncs import lmap

def create_playlist(name, tracks):
    headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    r = requests.post(
        'https://api.spotify.com/v1/users/lerner98/playlists', 
        headers=headers,
        json={'name': name}
    )
    assert r.status_code == 200 or r.status_code == 201, "Create playlist status code is: %d" % r.status_code
    url = r.headers['Location']
    assert not url is None, "Location of new playlist is None"

    r = requests.post(
        url + '/tracks', 
        headers=headers,
        json={'uris':
            lmap(lambda id: 'spotify:track:' + id, tracks
        )}
    )
    assert r.status_code == 201, "Add tracks to playlist failed: %d" % r.status_code


client_id = os.environ['SPOTIPY_CLIENT_ID']
client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
redirect_uri = 'http://localhost:8080/callback'
token = util.prompt_for_user_token('lerner98', 'user-read-recently-played user-library-read playlist-modify-public', client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

if __name__ == '__main__':
    if token:
        pass
    else:
        print('Could not get spotipy token')