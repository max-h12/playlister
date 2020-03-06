#sends all http requests to spotifys API
import requests
import re
import time

import key
import distributions as dist

#get an auth key from spotify using client info
def get_token():
    request_url = "https://accounts.spotify.com/api/token"
    params = {'grant_type':'client_credentials'}
    r = requests.post(url = request_url, data = params, auth = (key.client_id, key.client_secret))

    #auth token for all subsequent requests
    token = 'Bearer ' + r.json()['access_token']
    return token

#gets all songs from playlist_id, using token as authentication, loading into the dict 'songs'
def get_playlist_tracks(songs, token, playlist_id):

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
            if item['track'] is None:
                print(f"ERROR READING TRACK \n {item}")
            else:
                 songs[item["track"]["id"]] = {"name":item["track"]["name"]}

        offset+=100
        r = requests.get(url = request_url, headers = params, params={"offset":str(offset)}) 
        data = r.json()

#gets all the features for each song in the songs map, adds in partial averages as well
def get_song_features(songs, attribute_avg, token):

    #setup the request
    request_url = "https://api.spotify.com/v1/audio-features/"
    params = {'Authorization':token} 

    #go through every song
    for song_id in songs:
        #request the attributes for that song, checking for none type
        if song_id is None:
            print("SONG ID ERROR")
        else:
            r = requests.get(url = request_url + song_id, headers = params) 
            data = r.json()

            attempts = 0
            while "error" in data and data["error"]["status"]==429:
                print(f"Error: {data}, trying again in 5 seconds")
                attempts+=1
                if(attempts>25):
                    print(f"Too many failed attempts, exiting")
                    exit
                time.sleep(5)
                r = requests.get(url = request_url + song_id, headers = params) 
                data = r.json()

            #add each attribute into the map and add its partial average in
            #putting both avoids having to double loop
            for key in attribute_avg:
                if key in data:
                    songs[song_id][key] = data[key]
                    attribute_avg[key] += ((data[key])/(len(songs)))
                else:
                    print(f"HTTP Response error, {data} has no key: {key}")

#finds the top 10 playlists relating to the particular 'genere'
def search_for_playlists(genre, limit, token):
    ids = []

    #send a request to search for playlists with a match for 'genre'

    request_url = f"https://api.spotify.com/v1/search?q=%20{genre}%20&type=playlist&market=US&limit={limit}"
    content = "application/json"
    params = {'Accept':content, 'Content-Type':content,'Authorization':token} 

    r = requests.get(url = request_url, headers = params) 

    #payload of the http response
    data = r.json()
    results = data['playlists']['items']

    for playlist in results:
        ids.append(playlist["id"])

    return ids

