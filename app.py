from flask import Flask, url_for, request, jsonify, send_from_directory
from markupsafe import escape
import db
import spotify_api_logic
from auth import get_token
import sqlite3

app = Flask(__name__)

db.initalize_db()

@app.route('/')
def index():
    return send_from_directory("static", "index.html")

def artists_get():
    artists = []
    for artist in db.get_all_artists():
        artists.append({
            "name": artist[0],
            "num_albums": artist[1],
            "popularity": artist[2],
            "top_tracks": artist[3]
        })
    return jsonify(artists)

def artists_post():
    data = request.get_json()

    if not data or 'artist_name' not in data: # returns error code for missing artist name
        return jsonify({"error": "artist_name is required"}), 400

    # get the request data
    artist_name = data.get("artist_name")
    
    # get auth token
    token = get_token()

    # search for artist
    artist_result = spotify_api_logic.search_for_artist(token, artist_name)

    if artist_result is None:
        return jsonify({"error": "Artist not found on Spotify"}), 404
    
    # extract info from json
    real_name = artist_result['name']
    artist_id = artist_result['id']

    if db.artist_in_db(real_name): # returns error code for duplicate entries
        return jsonify({"error": f"Artist '{real_name}' already exists in the database."}), 409

    num_albums = spotify_api_logic.get_num_artist_albums(token, artist_id)
    avg_popularity = spotify_api_logic.get_avg_pop_score(token, artist_id)
    top_tracks = spotify_api_logic.get_artists_top_tracks_string(token, artist_id)

    # insert into database
    db.insert_artist(real_name, num_albums, avg_popularity, top_tracks)

    return jsonify({"message": f"Artist '{real_name}' added successfully."}), 201

# route to db.py
@app.route('/artists', methods=['GET', 'POST'])
def artists():
    if request.method == 'GET': # take in raw SQL data into dictionary, return JSON response
        return artists_get()
    else:
        return artists_post()

@app.route('/artists/<name>', methods=['DELETE'])
def delete_artist(name): # name is passed in as kwarg from route
    # can call spotify api and do search for artist, to get the exact name from spotify and delete from db, since they are the same name y'know?


    # check if artist exists
    artist_result = db.artist_in_db(name)

    if artist_result is False:
        return jsonify({"error": f"Artist '{name}' does not exist in the database."}), 404
    else:
        db.delete_artist(name)
        return jsonify({"message": f"Artist '{name}' deleted successfully."}), 200

if __name__ == "__main__":
    app.run(debug=True)