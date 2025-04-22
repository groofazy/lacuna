from auth import get_token
from spotify_api_logic import search_for_artist, get_songs_by_artist

token = get_token()

artist_name = input("Enter artist name: ")

result = search_for_artist(token, artist_name)
artist_id = result["id"] 
songs = get_songs_by_artist(token, artist_id)

for idx, song in enumerate(songs):
    print(f"{idx + 1} , {song['name']}")