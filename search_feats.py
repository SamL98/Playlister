import spotipy.util as util
import requests

from lfuncs import lmap, lfilter

client_id = '9a84cc6bdd8849d4a5270336e60469af'
client_secret = 'eebeea17f3634ac484a98af4f79db418'
redirect_uri = 'http://localhost:8080/callback'
token = util.prompt_for_user_token('lerner98', 'user-read-recently-played user-library-read', client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

def return_token():
    return token

def format_track(track):
    return { 'artist': '"' + track['artists'][0]['name'] + '"',
        'id': track['id'],
        'name': '"' + track['name'] + '"' }

def get_the_shit(features, ids, token):
    params = {}
    feat_list = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']
    for name, feat in zip(feat_list, features):
        params['target_' + name] = feat
    params['seed_tracks'] = ','.join(ids)
    params['limit'] = 5

    r = requests.get('https://api.spotify.com/v1/recommendations', params=params, headers={'Authorization': 'Bearer ' + token})
    if not 'tracks' in r.json():
        return []
    track_json = (r.json())['tracks']
    return lmap(format_track, track_json)

def get_the_shit2(ids, token):
    r = requests.get('https://api.spotify.com/v1/tracks', params={'ids': ','.join(ids)}, headers={'Authorization': 'Bearer ' + token})
    #print(r.json())
    if not 'tracks' in r.json():
        return []
    tracks = (r.json())['tracks']
    tracks = lmap(format_track, tracks)
    return tracks

def get_the_shit3(id, token):
    r = requests.get('https://api.spotify.com/v1/tracks/' + id, headers={'Authorization': 'Bearer ' + token})
    return format_track(r.json())

def get_track_from_features(features, ids):
    return get_the_shit(features, ids, token)

def get_tracks_by_ids(ids):
    return get_the_shit2(ids, token)

def get_track_by_id(id):
    return get_the_shit3(id, token)


if token:
	print('')
else:
    print('Could not get spotipy token')