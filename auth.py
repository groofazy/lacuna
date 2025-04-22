from dotenv import load_dotenv
import os
from requests import post
import base64
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token(): # client credentials workflow
    # take client id, 
    auth_string = client_id +":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    
    headers = {
        "Authorization": "Basic " + auth_base64, # sending auth data, verify if its correct, returns token
        "Content-Type": "application/x-www-form-urlencoded"

    }

    data = {"grant_type": "client_credentials"}

    # sends post request
    result = post(url, headers=headers, data=data)

    # convert json data into python dictionary
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token): # see Concepts: Access Token example in API Documentation for implementation reference
    return {"Authorization" : "Bearer " + token}