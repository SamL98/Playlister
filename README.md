# Playlister
Desktop application to create Spotify playlists by leveraging listening habits.

## Data Collection
Data is collected through the Spotify API. Spotify only allows you to grab the last 50 tracks listened to, so the get_data.py script must be run intermittently in order to grab more listening history. Hopefully, this can either be automated or a new method of data collection can be found.

## Model
As of right now, all tracks are compiled into one 2d array of audio features (again obtained via the Spotify API). This array is then normalized and partitioned into time-slices of length 5 so that the first four vectors of audio features can be inputted into the model and the last vector is predicted. The model is an LSTM and an SGD optimizer.

## Playlist Creation
There are 3 test files (test{2-4}.csv) consisting of the Spotify URI's for four hand-picked tracks. The audio features for these four tracks are obtained and the data is prepared as previously described. The saved model then outputs a new feature vector.

The Euclidean distance between every track (feature vector) in the user's library and the denormalized, output vector is calculated. The track with the smallest distance is then put as the most recent element in the 4-track array, pushing out the oldest one. This process is repeated 20 times then a playlist is created and populated with the tracks.