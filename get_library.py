#import spotipy.util as util

import requests

from search_feats import return_token, format_track
from lfuncs import lmap

"""
client_id = '9a84cc6bdd8849d4a5270336e60469af'
client_secret = 'eebeea17f3634ac484a98af4f79db418'
redirect_uri = 'http://localhost:8080/callback'
token = util.prompt_for_user_token('lerner98', 'user-read-recently-played', client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
"""

AUTH_HEADER = {'Authorization': 'Bearer ' + return_token()}
call_counter = 0

def lib_params(call_count):
    return {'limit': 50, 'offset': call_count * 50}

def fetch_library(call_counter):
    print(f'{call_counter}th batch')
    r = requests.get('https://api.spotify.com/v1/me/tracks', params=lib_params(call_counter), headers=AUTH_HEADER)
    call_counter += 1
    return lmap(
        lambda x: format_track(x['track'])
        , (r.json())['items']
    ), call_counter

def save_to_disk(tracks):
    with open('library.csv', 'w') as f:
        for track in tracks:
            f.write('spotify:track:' + track['id'] + '\n')

if __name__ == '__main__':
    call_counter = 0
    tracks, call_counter = fetch_library(call_counter)
    new_len = len(tracks)
    while new_len == 50:
        new_tracks, call_counter = fetch_library(call_counter)
        new_len = len(new_tracks)
        tracks.extend(new_tracks)
        
    save_to_disk(tracks)

"""
if token:
    save_to_disk(fetch_library())
else:
    print('Could not get spotipy token')"""