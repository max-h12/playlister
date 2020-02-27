import requests
import base64
import re

import key

#get an auth key from spotify using client id
TOKEN_URL = "https://accounts.spotify.com/api/token"
PARAMS = {'grant_type':'client_credentials'}

r = requests.post(url = TOKEN_URL, data = PARAMS, auth = (key.client_id, key.client_secret))
token = 'Bearer ' + r.json()['access_token']

#get the playlist url
playlist_url = input("Please enter a public spotify playlist url\n")
id = re.search("/playlist/([a-zA-Z0-9]*)", playlist_url)
playlist_id = id.group()[10::]

URL = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
content = "application/json"

PARAMS = {'Accept':content, 'Content-Type':content, 'Authorization':token} 
  
# sending get request and saving the response as response object 
r = requests.get(url = URL, headers = PARAMS) 
  
# extracting data in json format 
data = r.json() 

print("Tracks Found:")
for item in data["items"]:
    print(">> "+item["track"]["name"])
