from app import app
from db import delete_artist
from flask import jsonify
import pytest

# simulates sending POST request to /artists route
def test_post_artist_success():

    delete_artist("Aphex Twin")

    app.testing = True
    client = app.test_client()

    # send POST request with valid artist name
    response = client.post('/artists', json= {
        "artist_name": "Aphex Twin"
    })

    # Check for valid status code
    assert response.status_code == 201

    # check that response contains success message
    data = response.get_json()
    assert "message" in data
    assert "Aphex Twin" in data["message"]

# simulates duplicate artist
def test_post_artist_duplicate():    

    delete_artist("Aphex Twin")

    app.testing = True
    client = app.test_client()

    artist_data = {"artist_name": "Aphex Twin"}

    # First POST
    response1 = client.post("/artists", json=artist_data)
    assert response1.status_code == 201

    # Second POST (detects duplicate)
    response2 = client.post("/artists", json=artist_data)
    assert response2.status_code == 409

    json_data = response2.get_json()
    assert "error" in json_data # checks that server returned structured error message
    assert "already exists" in json_data["error"]

# simulates missing artist name
def test_post_artist_missing_name():

    app.testing = True
    client = app.test_client()

    response = client.post('/artists', json={})

    # check for valid status code (400 = bad request)
    assert response.status_code == 400 

    json_data = response.get_json()

    assert "error" in json_data 

def test_post_artist_not_found():
    app.testing = True
    client = app.test_client()

    artist_data = {"artist_name": "some_random_name_that_does_not_exist"}
    
    response = client.post("/artists", json=artist_data)

    assert response.status_code == 404

    json_data = response.get_json()

    assert "error" in json_data

    

    

