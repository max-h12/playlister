import requests
import base64
import re

import key

#get an auth key from spotify using client id
def get_token():
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    PARAMS = {'grant_type':'client_credentials'}
    r = requests.post(url = TOKEN_URL, data = PARAMS, auth = (key.client_id, key.client_secret))

    #auth token for all subsequent requests
    token = 'Bearer ' + r.json()['access_token']
    return token

def get_playlist_id():
    #get the playlist url using regex
    playlist_url = input("Please enter a public spotify playlist url\n")
    id = re.search("/playlist/([a-zA-Z0-9]*)", playlist_url)
    playlist_id = id.group()[10::]
    return playlist_id

def get_album_tracks(songs, token, playlist_id, offset=0):
    #send a request to get all tracks from the playlist
    URL = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    content = "application/json"
    PARAMS = {'Accept':content, 'Content-Type':content, 'Authorization':token} 
    r = requests.get(url = URL, headers = PARAMS) 

    #payload of the http response
    data = r.json()

    #load into dict
    for item in data["items"]:
        songs[item["track"]["name"]] = {"id":item["track"]["id"]}
        print(">> " + item["track"]["name"])



def main():
    #map of songs, key being song-title, value is a map of attributes
    songs = {}

    token = get_token()
    playlist_id = get_playlist_id()
    get_album_tracks(songs, token, playlist_id)

    #if the playlist is over 100 songs, keep track of how many are left
    #songs_left = int(data["total"]) - len(data["items"])

if __name__ == "__main__":
    main()

