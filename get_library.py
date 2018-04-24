import requests

from search_feats import return_token, format_track
from lfuncs import lmap

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