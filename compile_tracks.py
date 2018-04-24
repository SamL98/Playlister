import os
from functools import reduce

import spotipy.util as util
import requests

from lfuncs import *

def read_file(filename):
	text = ''
	with open(filename, 'r') as f:
		text = f.readlines()
	return text

def get_features_for_seg(seg, token):
    params={'ids': ','.join(seg[:min(100, len(seg))])}
    url = 'https://api.spotify.com/v1/audio-features'
    r = requests.get(url, params=params, headers={'Authorization': 'Bearer ' + token})
    feats = lfilter(lambda x: not x is None, r.json()['audio_features'])
    feats = lmap(format_features, feats)
    if len(seg) < 100:
	    return feats
    else:
        feats.extend(get_features_for_seg(seg[100:], token))
        return feats

def get_features_for_file(filename, token):
    seg = lmap(lambda x: x.split(',')[-3], read_file(filename))
    ids = seg
    feats = get_features_for_seg(seg, token)
    #feats = lfilter(lambda x: not x is None, feats)
    #feats = lmap(format_features, feats)
    return feats, ids

def get_features_for_file2(filename, token):
    seg = lmap(lambda x: x.split(':')[-1][:-1], read_file(filename))
    ids = seg
    feats = get_features_for_seg(seg, token)
    #feats = lfilter(lambda x: not x is None, feats)
    #feats = lmap(format_features, feats)
    return feats, ids

def format_features(feat):
    return [feat['danceability'], feat['energy'], feat['speechiness'], feat['acousticness'], feat['instrumentalness'], feat['liveness'], feat['valence']]

def get_features(token):
    files = os.listdir('data')
    files = lfilter(lambda x: x.endswith('.csv'), files)
    files = sorted(files, reverse=True)

    all_tracks = []
    for track in lmap(read_file, lmap(lambda x: os.path.join('data', x), files)):
	    all_tracks.extend(track) 
    all_tracks = lmap(lambda x: x.split(','), all_tracks)

    segments = []
    curr_seg = [all_tracks[0][-3]]
    last_time = int(round(float(all_tracks[0][-1])))

    for track in all_tracks[1:]:
        time = int(round(float(track[-1])))
        if last_time - time >= 3600:
	        segments.append(curr_seg)
	        curr_seg = [track[-3]]
        else:
	        curr_seg.append(track[-3])	
        last_time = time
    segments.append(curr_seg)

    features = []
    for seg in segments:
	    feats = get_features_for_seg(seg, token)
	    #feats = lfilter(lambda x: not x is None, feats)
	    #feats = lmap(format_features, feats)
	    features.append(feats)
    return features

def get_feats():
    global features
    if features is None:
        features = get_features(token)
    return features

def get_feats_for_file(filename):
    return get_features_for_file(filename, token)

def get_feats_for_file2(filename):
    return get_features_for_file2(filename, token)

client_id = os.environ['SPOTIPY_CLIENT_ID']
client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
redirect_uri = 'http://localhost:8080/callback'
token = util.prompt_for_user_token('lerner98', 'user-read-recently-played user-library-read', client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

features = None
if __name__ == '__main__':
    if token:
        features = get_features(token)
    else:
        print('Could not get spotipy token')
