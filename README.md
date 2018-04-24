# Playlister
Desktop application to create Spotify playlists by leveraging listening habits.

## Data Collection
Data is collected through the Spotify API. Spotify only allows you to grab the last 50 tracks listened to, so the get_data.py script must be run intermittently in order to grab more listening history. Hopefully, this can either be automated or a new method of data collection can be found.

## Model
As of right now, all tracks are compiled into one 2d array of audio features (again obtained via the Spotify API). This array is then normalized and partitioned into time-slices of length 5 so that the first four vectors of audio features can be inputted into the model and the last vector is predicted. The model is an LSTM and an SGD/RMSProp optimizer (I go back and forth).

## Playlist Creation
There are 3 test files (test{2-4}.csv) consisting of the Spotify URI's for four hand-picked tracks. The audio features for these four tracks are obtained and the data is prepared as previously described. The saved model then outputs a new feature vector.

The Euclidean distance between every track (feature vector) in the user's library and the denormalized, output vector is calculated. The track with the smallest distance is then put as the most recent element in the 4-track array, pushing out the oldest one. This process is repeated 20 times then a playlist is created and populated with the tracks.

### Sample Output:
Input:
1. "Dream To Me" - "Dom Kennedy"
2. "Birthdaze" - "Quelle Chris"
3. "Mutant Vengeance" - "Fly Anakin"
4. "Graduate" - "Dom Kennedy"

Output:
1. "Red and Gold"-"MF DOOM"
2. "Keep It Low"-"Generationals"
3. "Miracle"-"Jurassic Shark"
4. "Throw Sum Mo"-"Rae Sremmurd"
5. "Nothin' At All (feat. Skoolie 300)"-"Chuuwee"
6. "Not U"-"HOMESHAKE"
7. "Kenwood Ave."-"Mir Fontane"
8. "Still Dreaming"-"Nas"
9. "93 Vitals'"-"J-Tek"
10. "Sagittarius Rapp"-"Edan"
11. "Vomitspit"-"MF DOOM"
12. "Write Wrongs"-"Oh No"
13. "do u"-"lojii"
14. "Drive Slow"-"Kanye West"
15. "Slang Blade (feat. Senim Silla)"-"Senim Silla"
16. "Tick Tock"-"The Alchemist"
17. "The Dreamer"-"Anderson .Paak"
18. "I Used To Love Her (Again)"-"Murs & 9th Wonder"
19. "Nigga Concentrate"-"Scotty Atl"
20. "Inside"-"Earl Sweatshirt"

As you can see, the model is not great at this point in time. Many of the 20 predicted songs are tolerable such as "Nothin' At All" or "do u" considering the input. However, when there are songs that are poor predictions such as "Keep it Low" or "Not U", they greatly take away from the quality and flow of the playlist.