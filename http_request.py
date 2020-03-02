#sends all http requests to spotifys API
import requests
import re

import key
import distributions as dist

#get an auth key from spotify using client id
def get_token():
    request_url = "https://accounts.spotify.com/api/token"
    params = {'grant_type':'client_credentials'}
    r = requests.post(url = request_url, data = params, auth = (key.client_id, key.client_secret))

    #auth token for all subsequent requests
    token = 'Bearer ' + r.json()['access_token']
    return token



#gets all songs from playlist_id, using token as authentication, loading into the dict 'songs'
def get_album_tracks(songs, token, playlist_id):

    #send a request to get all tracks from the playlist_id
    request_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    content = "application/json"
    params = {'Accept':content, 'Content-Type':content, 'Authorization':token} 
    offset = 0

    r = requests.get(url = request_url, headers = params, params={"offset":str(offset)}) 

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
        r = requests.get(url = request_url, headers = params, params={"offset":str(offset)}) 
        data = r.json()

#gets all the features for each song in the songs map
def get_song_features(songs, attribute_avg, token):
    #setup the request
    request_url = "https://api.spotify.com/v1/audio-features/"
    params = {'Authorization':token} 

    #go through every song
    for id in songs:
        #request the attributes for that song
        r = requests.get(url = request_url + id, headers = params) 
        data = r.json()

        #add each attribute into the map and add its partial average in
        #putting both avoids having to double loop
        for key in attribute_avg:
            songs[id][key] = data[key]
            attribute_avg[key] += ((data[key])/(len(songs)))