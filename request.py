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
            songs[item["track"]["id"]] = {"name":item["track"]["name"]}
            
        offset+=100
        r = requests.get(url = URL, headers = PARAMS, params={"offset":str(offset)}) 
        data = r.json()

def get_song_features(songs, attribute_avg, token):
    #setup the request
    URL = "https://api.spotify.com/v1/audio-features/"
    PARAMS = {'Authorization':token} 

    #go through every song
    for id in songs:
        #request the attributes for that song
        r = requests.get(url = URL + id, headers = PARAMS) 
        data = r.json()

        #add each attribute into the map and add its partial average in
        for key in attribute_avg:
            songs[id][key] = data[key]
            attribute_avg[key] += (data[key]/len(songs))

def main():
    #map of songs, key being song-title, value is a map of attributes
    songs = {}

    #average of all songs in respective categories
    attribute_avg = {"duration_ms":0, "key":0, "mode":0, "acousticness":0, "danceability":0, "energy":0, "instrumentalness":0, "liveness":0, "loudness":0, "speechiness":0, "valence":0, "tempo":0}

    #get authorization and playlist id from input
    token = get_token()
    playlist_id = get_playlist_id()

    #get the songs, then load in their features
    get_album_tracks(songs, token, playlist_id)
    get_song_features(songs, attribute_avg, token)

if __name__ == "__main__":
    main()

