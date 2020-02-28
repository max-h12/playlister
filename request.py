import requests
import re

import key

PITCH_MAP = {0:"C", 1:"C#", 2:"D", 3:"D#", 4:"E", 5:"F", 6:"F#", 7:"G", 8:"G#", 9:"A", 10:"A#", 11:"B"}
MODE_MAP = {0:"Minor", 1:"Major"}

#get an auth key from spotify using client id
def get_token():
    request_url = "https://accounts.spotify.com/api/token"
    params = {'grant_type':'client_credentials'}
    r = requests.post(url = request_url, data = params, auth = (key.client_id, key.client_secret))

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
        for key in attribute_avg:
            songs[id][key] = data[key]
            attribute_avg[key] += ((data[key])/(len(songs)))

#formats the attribute averages for display to user
def format_oput(attribute_avg):
    milli = attribute_avg['duration_ms']
    seconds = round(int((milli/1000)%60),2)
    minutes = round(int((milli/(1000*60))%60),2)
    print(f"Average duration: {minutes}:{seconds}")
    est_pitch = round(attribute_avg['key'])
    if(PITCH_MAP.__contains__(est_pitch)):
        print(f"Overall key average: {PITCH_MAP[est_pitch]}")
    else:
        print("Overall key average: Unknown")
    print(f"Major/Minor Average: More {MODE_MAP[round(attribute_avg['mode'])]}")
    print(f"Average Time Signature (beats per bar/measure): {round(attribute_avg['time_signature'])}")
    print(f"Average Acousticness (confidence a track is acoustic)[0.0 - 1.0]: {round(attribute_avg['acousticness'],3)}")
    print(f"Average Danceability [0.0 - 1.0]: {round(attribute_avg['danceability'],3)}")
    print(f"Average Energy [0.0 - 1.0]: {round(attribute_avg['energy'],3)}")
    print(f"Average Instrumentalness (confidence there are no words) [0.0 - 1.0]: {round(attribute_avg['instrumentalness'],3)}")
    print(f"Average Liveness (confidence song was recorded in front of an audience) [0.0 - 1.0]: {round(attribute_avg['liveness'],3)}")
    print(f"Average Loudness [-60db - 0db]: {round(attribute_avg['loudness'],3)}db")
    print(f"Average Speechiness [0.0 - 1.0]: {round(attribute_avg['speechiness'],3)}")
    print(f"Average Valence (how cheerful the track is) [0.0 - 1.0]: {round(attribute_avg['valence'],3)}")
    print(f"Average Tempo (BPM): {round(attribute_avg['tempo'],3)}")

def main():
    #map of songs, key being song-title, value is a map of attributes
    songs = {}

    #average of all songs in respective categories
    attribute_avg = {"duration_ms":0, "key":0, "mode":0, "time_signature":0, "acousticness":0, "danceability":0, "energy":0, "instrumentalness":0, "liveness":0, "loudness":0, "speechiness":0, "valence":0, "tempo":0}

    #get authorization and playlist id from input
    token = get_token()
    playlist_id = get_playlist_id()

    #get the songs, then load in their features
    get_album_tracks(songs, token, playlist_id)
    get_song_features(songs, attribute_avg, token)

    print(f"Songs found in playlist: {len(songs)}")
    format_oput(attribute_avg)

if __name__ == "__main__":
    main()

