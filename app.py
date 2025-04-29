from flask import Flask, url_for, request, jsonify
from markupsafe import escape
import db
import spotify_api_logic
from auth import get_token
import sqlite3

app = Flask(__name__)

db.initalize_db()

@app.route('/')
def index():
    return '<p>Index Page<p>'

@app.route('/hello')
def hello_world():
    return 'Hello, World!'

@app.route('/user/<username>') # this can be used for strings, int, float, path, and uuid
def show_user_profile(username): # function takes username as kwargs from @app.route
    return f'User {escape(username)}\'s profile!'

with app.test_request_context(): # builds URL to specific function
    print(url_for('index'))
    print(url_for('hello_world'))
    print(url_for('hello_world', next='/'))
    print(url_for('show_user_profile', username='John Doe'))

def artists_get():
    artists = []
    for artist in db.get_all_artists():
        artists.append({
            "name": artist[0],
            "num_albums": artist[1],
            "popularity": artist[2]
        })
    return jsonify(artists)

def artists_post():
    con = sqlite3.connect('spotify.db')
    cur = con.cursor()

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

    # insert into database
    db.insert_artist(real_name, num_albums, avg_popularity, con)

    return jsonify({"message": f"Artist '{real_name}' added successfully."}), 201

# route to db.py
@app.route('/artists', methods=['GET', 'POST'])
def artists():
    if request.method == 'GET': # take in raw SQL data into dictionary, return JSON response
        return artists_get()
    else:
        return artists_post()


if __name__ == "__main__":
    app.run(debug=True)