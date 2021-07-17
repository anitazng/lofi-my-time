import django
django.setup()

import requests
import random
import json
import sys

"""
Step 1: Get 300 lofi songs from Lofi Beats playlist
Step 2: Get correct number of songs from all lofi songs
Step 3: Create playlist on user's profile
Step 4: Add correct number of lofi songs from Lofi Beats playlist to user playlist

"""

class CreatePlaylist:
    
    def __init__(self, access_token, time_in_minutes):
        self.access_token = access_token
        self.time = time_in_minutes*60000
    
    # Step 1: Get lofi songs from Lofi Beats playlist
    def get_300_lofi_songs(self):
        offset = random.randint(0, 200)
        track_uris = []
        track_ids = []
        
        for i in range(3):
            url = f'https://api.spotify.com/v1/playlists/37i9dQZF1DWWQRwui0ExPn/tracks?offset={offset}'
            
            response = requests.get(
                url, 
                headers={
                    "Content-Type": "application/json", 
                    "Authorization": f'Bearer {self.access_token}'
                    }
                )
            
            response_json = response.json()

            for item in response_json['items']:
                track_uri = item['track']['uri']
                track_id = item['track']['id']
                track_uris.append(track_uri)
                track_ids.append(track_id)
                
            offset += 100

        return track_ids, track_uris
        
    # Step 2: Get correct number of songs from all lofi songs
    def get_correct_lofi_songs(self, track_ids, track_uris):
        
        new_track_uris = []
        playlist_length = 0
        song_num = 0
        
        for track_id in track_ids:
            url = f'https://api.spotify.com/v1/audio-features/{track_id}'
            
            response = requests.get(
            url, 
            headers={
                "Content-Type": "application/json", 
                "Authorization": f'Bearer {self.access_token}'
                }
            )
            
            response_json = response.json()

            if playlist_length + response_json['duration_ms'] <= self.time+30000:
                playlist_length += response_json['duration_ms']
                song_num += 1
            else: 
                break
        
        # create list of track uris according to number of songs    
        for i in range(song_num):
            new_track_uris.append(track_uris[i])

        return new_track_uris
    
    # Step 3: Create playlist on user's profile
    def create_playlist(self):
        # get url
        url = 'https://api.spotify.com/v1/me'
        response = requests.get(
            url, 
            headers={
                "Content-Type": "application/json", 
                "Authorization": f'Bearer {self.access_token}'
                }
            )
            
        response_json = response.json()

        # make playlist
        url = str(response_json['href']) + '/playlists'
        request_body = json.dumps({
            "name": "your study playlist",
            "description": "brought to you by lofi my time :)",
            "public": True
            })
        
        response = requests.post(
            url, 
            data = request_body,
            headers={
                "Content-Type": "application/json", 
                "Authorization": f'Bearer {self.access_token}'
                }
            )
        
        playlist_id = response.json()['id']

        return playlist_id
    
    # Step 4: Add correct number of lofi songs from Lofi Beats playlist to user playlist
    def add_lofi_songs(self, track_uris, playlist_id):
        half_of_tracks = int(len(track_uris)/2)
        
        # split into 2 since spotify can't handle that many tracks at once
        track_uris_1 = track_uris[:half_of_tracks]
        track_uris_2 = track_uris[half_of_tracks:]
        
        # first request
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        request_body = json.dumps({
            'uris': track_uris_1
            })
        
        response = requests.post(
            url,
            data = request_body,
            headers={
                "Content-Type": "application/json", 
                "Authorization": f'Bearer {self.access_token}'
                }
            )
        
        # second request
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        request_body = json.dumps({
            'uris': track_uris_2
            })
        
        response = requests.post(
            url,
            data = request_body,
            headers={
                "Content-Type": "application/json", 
                "Authorization": f'Bearer {self.access_token}'
                }
            )

# get access token
access_token = sys.argv[2]

# get study session length
time =  int(sys.argv[1])

playlist = CreatePlaylist(access_token, time)

track_ids, track_uris = playlist.get_300_lofi_songs()
new_track_uris = playlist.get_correct_lofi_songs(track_ids, track_uris)
playlist_id = playlist.create_playlist()

playlist.add_lofi_songs(new_track_uris, playlist_id)

