import json
from pprint import pprint
import spotipy
import spotipy.util as util
import sys

scope = 'user-library-read'
username = '1280113573'

songs_file = 'songs.txt'

token = util.prompt_for_user_token(username, scope)

sp = spotipy.Spotify(auth=token)

query = input('Enter the desired artist\'s name > ')

search_results = sp.search(query, type='artist')

try:
    artist_id = search_results['artists']['items'][0]['id']
    artist_name = search_results['artists']['items'][0]['name']
except:
    print('Unable to find artist')
    sys.exit(0)

artist_albums = sp.artist_albums(artist_id)

master_list = []
name_list = []
id_list = []

for album in artist_albums['items']:
    album_id = album['id']

    album_tracks = sp.album_tracks(album_id)

    for track in album_tracks['items']:
        try:
            audio_features = sp.audio_features(track['id'])[0]
        except Exception as e:
            print('Error: %s' % track['name'])
            continue

        song_obj = {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'acousticness': audio_features['acousticness'],
            'danceability': audio_features['danceability'],
            'duration_ms': audio_features['duration_ms'],
            'energy': audio_features['energy'],
            'explicit': track['explicit'],
            'id': track['id'],
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
        if(not(track['id'] in id_list) and not(track['name'] in name_list) and
           track['artists'][0]['name'] == artist_name):
            id_list.append(track['id'])
            name_list.append(track['name'])
            master_list.append(song_obj)

pprint(name_list)
query = query.replace(' ', '_')
with open(query + '.txt', 'w') as f:
    f.write(json.dumps(master_list))
print("output written to %s.txt (%d songs)" % (query, len(master_list)))
