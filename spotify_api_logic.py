from requests import get
from auth import get_token, get_auth_header
import json

token = get_token()

# function to search for artist
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1" # gives most popular artist

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=CA" # look for specific artist and their top tracks
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result 

# result = search_for_artist(token, "Malcom Todd")
# artist_id = result["id"] 
# songs = get_songs_by_artist(token, artist_id)

# for idx, song in enumerate(songs):
#     print(f"{idx + 1}, {song['name']}")


# result["name"] gets artist name