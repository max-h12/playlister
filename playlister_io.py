#handles input and output
import requests
import re

PITCH_MAP = {0:"C", 1:"C#", 2:"D", 3:"D#", 4:"E", 5:"F", 6:"F#", 7:"G", 8:"G#", 9:"A", 10:"A#", 11:"B"}
MODE_MAP = {0:"Minor", 1:"Major"}

# given a url, gets the spotify playlist id
def get_playlist_id():
    #get the playlist url using regex
    playlist_url = input("Please enter a public spotify playlist url\n")
    id = re.search("/playlist/([a-zA-Z0-9]*)", playlist_url)
    if id==None: 
        print("Bad Playlist URL")
        exit(-1)

    playlist_id = id.group()[10::]
    return playlist_id

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
