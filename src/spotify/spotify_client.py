import requests

def get_playlist_tracks(access_token, playlist_id):

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'fields': 'items(track(uri))',  
        'limit': 100  
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        tracks = data.get('items', [])
        track_uris = {item['track']['uri'] for item in tracks if item['track']}
        return track_uris
    else:
        print(f"Error fetching playlist tracks: {response.text}")
        return set()

def add_song_to_playlist(access_token, playlist_id, track_uri):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'uris': [track_uri]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print("Song added successfully!")
    else:
        print("Error adding song:", response.text)

def search_track(access_token, track_name):
    search_url = 'https://api.spotify.com/v1/search'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'q': f'track:{track_name}',
        'type': 'track',
        'limit': 1
    }
    response = requests.get(search_url, headers=headers, params=params)
    
    if response.status_code == 200:
        tracks = response.json().get('tracks', {}).get('items', [])
        if tracks:
            uri = tracks[0]['uri']
            print(f"Found track: {track_name}, URI: {uri}")
            return uri
    else:
        print(f"Error searching for track: {response.text}")
    return None