from flask import Flask, request
import urllib.parse
from config import SPOTIFY_PLAYLIST_ID, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, YOUTUBE_PLAYLIST_ID, YOUTUBE_API_KEY
from youtube.youtube_fetch import fetch_youtube_playlist
from spotify.spotify_client import search_track, add_song_to_playlist, get_playlist_tracks
from spotify.spotify_auth import get_access_token
from utils import print_playlist_details

app = Flask(__name__)

@app.route('/')
def home():
    scope = 'playlist-modify-public playlist-modify-private'
    auth_url = 'https://accounts.spotify.com/authorize'
    params = {
        'response_type': 'code',
        'client_id': SPOTIFY_CLIENT_ID,
        'scope': scope,
        'redirect_uri': SPOTIFY_REDIRECT_URI,
    }
    url = f"{auth_url}?{urllib.parse.urlencode(params)}"
    return f'<a href="{url}">Authorize Spotify</a>'

@app.route('/callback')
def callback():
    auth_code = request.args.get('code')
    if not auth_code:
        return "Authorization code not found in the URL.", 400

    tokens = get_access_token(auth_code)
    if tokens:
        access_token = tokens['access_token']
        youtube_songs = fetch_youtube_playlist(YOUTUBE_PLAYLIST_ID, YOUTUBE_API_KEY)
        
        if not youtube_songs:
            return "No songs found in the YouTube playlist."

        print_playlist_details("YouTube Playlist", len(youtube_songs))
        existing_tracks = get_playlist_tracks(access_token, SPOTIFY_PLAYLIST_ID)

        for track in youtube_songs:
            track_id = search_track(access_token, track)
    
            if track_id:
                print(f"Found track: {track}")
                if track_id not in existing_tracks:
                    add_song_to_playlist(access_token, SPOTIFY_PLAYLIST_ID, track_id)
                    print(f"Successfully added '{track}' to the playlist.")
                else:
                    print(f"Track '{track}' is already in the playlist. Skipping...")
            else:
                print(f"Track not found: {track}")

        return "Every track is dealt with"

if __name__ == "__main__":
    app.run(port=3000)