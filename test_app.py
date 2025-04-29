from app import app
from db import delete_artist
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

    data = response2.get_json()
    assert "error" in data
    assert "already exists" in data["error"]
