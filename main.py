from auth import get_token
from db import insert_artist
import spotify_api_logic as SAL


token = get_token()
user_search_name = input("Enter artist name: ")
artist_result = SAL.search_for_artist(token, user_search_name)
artist_id = artist_result["id"]
top_tracks_names = SAL.get_artists_top_tracks_string(token, artist_id)
artist_popularity = SAL.get_artists_top_tracks_popularity(token, artist_id)
score = SAL.get_avg_pop_score(token, artist_id)
num_albums = SAL.get_num_artist_albums(token, artist_id)


artist_name = SAL.get_artist_name(token, user_search_name)

def db_insert(artist_name, num_albums, score, top_tracks_names):
    insert_artist(artist_name, num_albums, score, top_tracks_names)


db_insert(artist_name, num_albums, score, top_tracks_names)