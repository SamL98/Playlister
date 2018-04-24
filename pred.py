from sklearn.preprocessing import normalize
from keras.models import model_from_json
import numpy as np

from compile_tracks import get_feats_for_file
from search_feats import get_track_from_features, get_tracks_by_ids, get_track_by_id
from lfuncs import lmap

feats, ids = get_feats_for_file('test.csv')
while len(feats) % 5 > 0:
	del feats[-1]
	del ids[-1]
dataset = np.array(feats)

mins = np.amin(dataset, axis=0)
maxs = np.amax(dataset, axis=0)

dataset = normalize(dataset, axis=1, norm='l1')
batches = np.array(np.split(dataset, len(dataset)//5))
id_batches = [ids[i*5:(i+1)*5] for i in range(len(dataset)//5)]

X = batches[:,:-1,:]
y = batches[:,-1,:]

jfile = open('mode.json')
model_json = jfile.read()
jfile.close()

model = model_from_json(model_json)
model.load_weights('model.h5')
model.compile(loss='mse', optimizer='rmsprop')
pred_feats = model.predict(X)

diffs = maxs - mins
numerator = diffs * pred_feats
denorm_pred = numerator + mins

for i, feat in enumerate(denorm_pred):
    tracks = get_tracks_by_ids(id_batches[i][:-1])
    for track in tracks:
        print(track['name'] + '-' + track['artist'])
    print('*****')
    target_track = get_track_by_id(id_batches[i][-1])
    print(target_track['name'] + '-' + target_track['artist'])
    print('*****')
    track_ids = lmap(lambda x: x['id'], tracks)
    tracks = get_track_from_features(feat, track_ids)
    for track in tracks:
        print(track['name'] + '-' + track['artist'])
    print('/////')