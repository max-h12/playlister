import requests
import re
import key 

playlist_url = input("Please enter a public spotify playlist url\n")
id = re.search("/playlist/([a-zA-Z0-9]*)", playlist_url)
playlist_id = id.group()[10::]

URL = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
content = "application/json"

PARAMS = {'Accept':content, 'Content-Type':content, 'Authorization':key.auth} 
  
# sending get request and saving the response as response object 
r = requests.get(url = URL, headers = PARAMS) 
  
# extracting data in json format 
data = r.json() 

print("Tracks Found:")
for item in data["items"]:
    print(item["track"]["name"])