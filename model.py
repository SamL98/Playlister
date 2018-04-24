from sklearn.preprocessing import normalize
from keras.layers import Dense, TimeDistributed, LSTM
from keras.models import Sequential
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping
import numpy as np

from compile_tracks import get_feats 

features = get_feats()
feats = []
for feature in features:
	for feat in feature:
		feats.append(feat)

while len(feats) % 5 > 0:
	del feats[-1]

dataset = np.array(feats, dtype=float)
dataset = normalize(dataset, axis=1, norm='l1') 
batches = np.array(np.split(dataset, len(dataset)//5))

timesteps = 4
data_dim = len(dataset[0])

X = batches[:,:-1,:]
y = batches[:,-1,:]

model = Sequential()
model.add(LSTM(128, input_shape=(timesteps, data_dim), return_sequences=False))
model.add(Dense(data_dim, activation='sigmoid'))

#sgd = SGD(lr=0.01, momentum=0.09, decay=1e-6)
model.compile(loss='mse', optimizer='rmsprop')

early_stop = EarlyStopping(monitor='loss', min_delta=1e-4, verbose=0, patience=1, mode='auto')
model.fit(X, y, batch_size=1, epochs=100, callbacks=[early_stop])

model_json = model.to_json()
with open('mode.json', 'w') as jfile:
	jfile.write(model_json)
model.save_weights('model.h5')
