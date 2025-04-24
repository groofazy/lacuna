from auth import get_token
from spotify_api_logic import search_for_artist, get_artists_top_tracks, get_artists_albums, print_top_tracks_and_popularity
token = get_token()

artist_name = input("Enter artist name: ")
result = search_for_artist(token, artist_name)
artist_id = result["id"]
top_tracks = get_artists_top_tracks(token, artist_id)
artists_albums =  get_artists_albums(token, artist_id)

print_top_tracks_and_popularity(token, artist_id)