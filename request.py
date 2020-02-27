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

#given a url, gets the spotify playlist id
def get_playlist_id():
    #get the playlist url using regex
    playlist_url = input("Please enter a public spotify playlist url\n")
    id = re.search("/playlist/([a-zA-Z0-9]*)", playlist_url)
    if id==None: 
        print("Bad Playlist URL")
        exit(-1)

    playlist_id = id.group()[10::]
    return playlist_id

#gets all songs from playlist_id, using token as authentication, loading into the dict 'songs'
def get_album_tracks(songs, token, playlist_id):

    #send a request to get all tracks from the playlist_id
    URL = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    content = "application/json"
    PARAMS = {'Accept':content, 'Content-Type':content, 'Authorization':token} 
    offset = 0

    r = requests.get(url = URL, headers = PARAMS, params={"offset":str(offset)}) 

    #payload of the http response
    data = r.json()

    #if not items, bad request
    if "items" not in data:
        print("Bad HTTP Request")
        exit(-2)

    #continue to request more songs until we run out
    while(("items" in data) and len(data["items"])>0):
        for item in data["items"]:
            songs[item["track"]["name"]] = {"id":item["track"]["id"]}

        offset+=100
        r = requests.get(url = URL, headers = PARAMS, params={"offset":str(offset)}) 
        data = r.json()


def main():
    #map of songs, key being song-title, value is a map of attributes
    songs = {}

    token = get_token()
    playlist_id = get_playlist_id()

    get_album_tracks(songs, token, playlist_id)
    print(len(songs))


if __name__ == "__main__":
    main()

