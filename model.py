from sklearn.preprocessing import normalize
from keras.layers import Dense, TimeDistributed, LSTM
from keras.models import Sequential
from keras.optimizers import SGD
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

#data = np.hsplit(batches, np.array([timesteps, 1]))
X = batches[:,:-1,:]
y = batches[:,-1,:]

model = Sequential()
model.add(LSTM(128, input_shape=(timesteps, data_dim), return_sequences=False))
#model.add(TimeDistributed(Dense(data_dim, activation='sigmoid'), input_shape=(timesteps, data_dim)))
model.add(Dense(data_dim, activation='sigmoid'))
model.compile(loss='mse', optimizer='sgd')

sgd = SGD(lr=0.01, momentum=0.9, decay=1e-6)
model.fit(X, y, batch_size=2, epochs=100)

model_json = model.to_json()
with open('mode.json', 'w') as jfile:
	jfile.write(model_json)
model.save_weights('model.h5')
