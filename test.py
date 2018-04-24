import sys

from sklearn.preprocessing import normalize
from keras.models import model_from_json
import numpy as np

from compile_tracks import get_feats_for_file2
from search_feats import get_track_from_features, get_tracks_by_ids, get_track_by_id
from create_playlist import create_playlist
from lfuncs import lmap

def norm_reversible(dataset):
    mins = np.amin(dataset, axis=0)
    maxs = np.amax(dataset, axis=0)
    dataset = normalize(dataset, axis=1, norm='l1')
    return dataset, mins, maxs

def reverse_norm(vec, mins, maxs):
    return (maxs - mins) * vec + mins

test_no = sys.argv[1]

lib_feats, lib_ids = get_feats_for_file2('library.csv')
feats, ids = get_feats_for_file2(test_no + '.csv')

all_ids = ids

dataset = np.array(feats)
lib_dataset = np.array(lib_feats)

dataset, mins, maxs = norm_reversible(dataset)
lib_dataset, lib_mins, lib_maxs = norm_reversible(lib_dataset)

batches = np.array(np.split(dataset, 1))

X = batches

jfile = open('mode.json')
model_json = jfile.read()
jfile.close()

model = model_from_json(model_json)
model.load_weights('model.h5')
model.compile(loss='mse', optimizer='sgd')

playlist_ids = all_ids[:]

tracks = get_tracks_by_ids(all_ids)
for track in tracks:
    print(track['name'] + ' - ' + track['artist'])

for _ in range(20):
    pred_feats = model.predict(X)
    denorm_pred = reverse_norm(pred_feats, mins, maxs)

    target = denorm_pred[0]
    tracks = get_tracks_by_ids(ids)

    target_mat = np.tile(target, (len(lib_dataset), 1))
    rex = np.sqrt((target_mat - lib_dataset)**2).sum(axis=1)
    closest = np.argsort(rex).tolist()

    rex_ids = [lib_ids[i] for i in closest[:50]]
    rex = get_tracks_by_ids(rex_ids)

    i = 0
    rec = rex[i]
    while rec['id'] in ids and i < len(rex)-1:
        i = i+1
        rec = rex[i]

    lib_dataset = np.delete(
        lib_dataset,
        lib_dataset[lib_ids.index(rec['id'])], 0
    )
    playlist_ids.append(rec['id'])
    
    print(rec['name'] + '-' + rec['artist'])

    X[0][:-1] = X[0][1:]
    X[0][-1] = target

    ids[:-1] = ids[1:]
    ids[-1] = rec['id']

create_playlist(test_no, playlist_ids)