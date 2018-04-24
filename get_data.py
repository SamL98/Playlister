from datetime import datetime
import time
import os

import spotipy.util as util
import requests

from lfuncs import *

base_url = 'https://api.spotify.com/v1/'

def format_track(track):
	track_obj = track['track']
	played_at = datetime.strptime(track['played_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
	return {
		'artist': '"' + track_obj['artists'][0]['name'] + '"',
		'duration': track_obj['duration_ms'],
		'id': track_obj['id'],
		'name': '"' + track_obj['name'] + '"',
		'timestamp': played_at.timestamp() }

def get_recently_played(token):
	params = {'limit': 49}

	if os.path.isfile('.next.txt'):
		with open('.next.txt') as f:
			params['after'] = int(f.readlines()[0])
	r = requests.get(base_url + 'me/player/recently-played', params, headers={'Authorization': 'Bearer ' + token})

	with open('.next.txt', 'w') as f:
		f.write((r.json())['cursors']['after'])	

	tracks = (r.json())['items']
	tracks = lmap(format_track, tracks)

	timestamp = int(time.time())
	tfile = open(f'data/tracks-{timestamp}.csv', 'w')
	for track in tracks:
		tfile.write(','.join([track['artist'], str(track['duration']), track['id'], track['name'], str(track['timestamp'])]) + '\n')
	tfile.close()

client_id = os.environ['SPOTIPY_CLIENT_ID']
client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
redirect_uri = 'http://localhost:8080/callback'

token = util.prompt_for_user_token('lerner98', 'user-read-recently-played', client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
if token:
	get_recently_played(token)
else:
	print('Could not get spotipy token')
