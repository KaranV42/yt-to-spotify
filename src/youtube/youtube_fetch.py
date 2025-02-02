import requests
import re
from config import YOUTUBE_API_KEY, YOUTUBE_PLAYLIST_ID
youtube_api_key = YOUTUBE_API_KEY
playlist_id = YOUTUBE_PLAYLIST_ID

def clean_track_title(title):
    # to deal with brackets
    title = re.sub(r'\[.*?\]', '', title)
    title = re.sub(r'\(.*?\)', '', title)
    
    # for non alphanumerics
    title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
    title = re.sub(r'\s+', ' ', title).strip()
    
    return title

def fetch_youtube_playlist(playlist_id, youtube_api_key):
    url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults=50&key={youtube_api_key}' 
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        tracks = [clean_track_title(item['snippet']['title']) for item in data['items']]
        return tracks
    else:
        print(f"Error fetching playlist: {response.status_code}")
        return []

if __name__ == "__main__":
    youtube_tracks = fetch_youtube_playlist(YOUTUBE_PLAYLIST_ID, YOUTUBE_API_KEY)
    
    if youtube_tracks:
        print(f"Found {len(youtube_tracks)} tracks in the YouTube playlist:")
        for track in youtube_tracks:
            print(track)
    else:
        print("No tracks found or there was an error.")
