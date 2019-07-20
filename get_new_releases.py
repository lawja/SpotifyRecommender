import json
from pprint import pprint
import spotipy
import spotipy.util as util
import sys

scope = 'user-library-read'
username = '1280113573'

songs_file = 'new_releases.txt'

nmf_id = '37i9dQZF1DWXJfnUiYjUKT'

token = util.prompt_for_user_token(username, scope)

sp = spotipy.Spotify(auth=token)

# print(dir(sp))
new_releases = sp.new_releases()['albums']['items']

master_list = []

nmf_playlist = sp.user_playlist('spotify', nmf_id)

tracks = nmf_playlist['tracks']['items']

for track in tracks:
    song_id = track['track']['id']
    try:
        audio_features = sp.audio_features(song_id)[0]
    except Exception as e:
        print('Error: %s' % track['name'])
        continue

    song_obj = {
        'name': track['track']['name'],
        'artist': track['track']['artists'][0]['name'],
        'acousticness': audio_features['acousticness'],
        'danceability': audio_features['danceability'],
        'duration_ms': audio_features['duration_ms'],
        'energy': audio_features['energy'],
        'explicit': track['track']['explicit'],
        'id': song_id,
        'instrumentalness': audio_features['instrumentalness'],
        'key': audio_features['key'],
        'liveness': audio_features['liveness'],
        'loudness': audio_features['loudness'],
        'popularity': 0,
        'mode': audio_features['mode'],
        'speechiness': audio_features['speechiness'],
        'tempo': audio_features['tempo'],
        'time_signature': audio_features['time_signature'],
        'valence': audio_features['valence']
    }

    master_list.append(song_obj)

with open(songs_file, 'w') as f:
    f.write(json.dumps(master_list))
print("output written to %s (%d songs)" % (songs_file, len(master_list)))
