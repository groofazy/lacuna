from auth import get_token
from spotify_api_logic import search_for_artist, get_artists_top_tracks, get_artists_top_tracks_popularity, get_avg_pop_score, get_num_artist_albums, get_artist_name
from db import insert_artist
import sqlite3

token = get_token()
user_search_name = input("Enter artist name: ")
artist_result = search_for_artist(token, user_search_name)
artist_id = artist_result["id"]
top_tracks = get_artists_top_tracks(token, artist_id)
artist_popularity = get_artists_top_tracks_popularity(token, artist_id)
score = get_avg_pop_score(token, artist_id)
num_albums = get_num_artist_albums(token, artist_id)

artist_name = get_artist_name(token, user_search_name)

def db_insert(artist_name, num_albums, score):
    insert_artist(artist_name, num_albums, score)


db_insert(artist_name, num_albums, score)