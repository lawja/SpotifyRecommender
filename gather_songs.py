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

playlists_obj = sp.current_user_playlists()


master_list = []
id_list = []

for playlist in playlists_obj['items']:
    playlist_id = playlist['id']
    print(playlist['name'])

    last_run = False
    playlist_offset = 0
    i = 1
    while(not(last_run)):
        playlist_tracks = sp.user_playlist_tracks(
            username, playlist_id, limit=100, offset=playlist_offset)
        playlist_offset += len(playlist_tracks['items'])

        if(len(playlist_tracks['items']) < 100):
            last_run = True

        print(i)
        print(len(playlist_tracks['items']))
        i += 1

        # print(playlist_id)
        for track_obj in playlist_tracks['items']:
            # pprint(track_obj)
            # pprint(track_obj)
            try:
                audio_features = sp.audio_features(track_obj['track']['id'])
            except Exception as e:
                print('Error: ' + track_obj['track']['name'])
                continue
            if(len(audio_features) != 1):
                print(track_obj['track']['name'])
                print(track_obj['track']['id'])
                print(audio_features)
                print('\n')
                break

            audio_features = audio_features[0]

            song_obj = {
                'name': track_obj['track']['name'],
                'artist': track_obj['track']['album']['artists'][0]['name'],
                'acousticness': audio_features['acousticness'],
                'danceability': audio_features['danceability'],
                'duration_ms': audio_features['duration_ms'],
                'energy': audio_features['energy'],
                'explicit': track_obj['track']['explicit'],
                'id': track_obj['track']['id'],
                'instrumentalness': audio_features['instrumentalness'],
                'key': audio_features['key'],
                'liveness': audio_features['liveness'],
                'loudness': audio_features['loudness'],
                'popularity': track_obj['track']['popularity'],
                'mode': audio_features['mode'],
                'speechiness': audio_features['speechiness'],
                'tempo': audio_features['tempo'],
                'time_signature': audio_features['time_signature'],
                'valence': audio_features['valence']
            }

            if(not(track_obj['track']['id'] in id_list)):
                id_list.append(track_obj['track']['id'])
                master_list.append(song_obj)
        print('Now added %s songs' % str(len(id_list)))

with open(songs_file, 'w') as f:
    f.write(json.dumps(master_list))
print("output written to %s" % songs_file)
