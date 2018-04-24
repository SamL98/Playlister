import os

import spotipy.util as util
import requests

from lfuncs import lmap, lfilter

client_id = os.environ['SPOTIPY_CLIENT_ID']
client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
redirect_uri = 'http://localhost:8080/callback'
token = util.prompt_for_user_token('lerner98', 'user-read-recently-played user-library-read', client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

base_url = 'https://api.spotify.com/v1/'
rex_url = base_url + 'recommendations'
trax_url = base_url + 'tracks'

def return_token():
    return token

def format_track(track):
    return { 'artist': '"' + track['artists'][0]['name'] + '"',
        'id': track['id'],
        'name': '"' + track['name'] + '"' }

def get_track_from_features(features, ids):
    params = {}
    feat_list = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']
    for name, feat in zip(feat_list, features):
        params['target_' + name] = feat
    params['seed_tracks'] = ','.join(ids)
    params['limit'] = 5

    r = requests.get(rex_url, params=params, headers={'Authorization': 'Bearer ' + token})
    if not 'tracks' in r.json():
        return []
    track_json = (r.json())['tracks']
    return lmap(format_track, track_json)

def get_tracks_by_ids(ids):
    r = requests.get(trax_url, params={'ids': ','.join(ids)}, headers={'Authorization': 'Bearer ' + token})
    if not 'tracks' in r.json():
        return []
    tracks = (r.json())['tracks']
    tracks = lmap(format_track, tracks)
    return tracks

def get_track_by_id(id):
    r = requests.get(trax_url + '/' + id, headers={'Authorization': 'Bearer ' + token})
    return format_track(r.json())

if token:
	pass
else:
    print('Could not get spotipy token')