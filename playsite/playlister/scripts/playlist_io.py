#handles input and output
import requests
import re

PITCH_MAP = {0:"C", 1:"C#", 2:"D", 3:"D#", 4:"E", 5:"F", 6:"F#", 7:"G", 8:"G#", 9:"A", 10:"A#", 11:"B"}
MODE_MAP = {0:"Minor", 1:"Major"}


# given a url, gets the spotify playlist id
def get_playlist_id(playlist_url):
    #get the playlist url using regex
    id = re.search("/playlist/([a-zA-Z0-9]*)", playlist_url)
    if id==None: 
        return(-1)

    playlist_id = id.group()[10::]
    return playlist_id

def get_omap(omap, attribute_avg, attribute_percentile, high_songs,low_songs):
    omap.update(basic_oput(attribute_avg, attribute_percentile))
    #omap.update(extreme_oput(high_songs, low_songs))
    return omap

#formats the attribute averages and percentiles for display to user in terminal
#TODO: reformat awful code
def basic_oput(attribute_avg, attribute_percentile):
    omap = {}

    milli = attribute_avg['duration_ms']
    seconds = round(int((milli/1000)%60),2)
    minutes = round(int((milli/(1000*60))%60),2)

    omap["duration"] = {}
    omap["duration"]["val"] = f"{minutes}:{seconds}"
    omap["duration"]["per"] =  f"{round(attribute_percentile['duration_ms'])}"

    est_pitch = round(attribute_avg['key'])
    if(PITCH_MAP.__contains__(est_pitch)):
        omap["key"] = f"{PITCH_MAP[est_pitch]}"
    else:
        omap["key"] = "Unknown"
    
    omap["mode"] = f"{MODE_MAP[round(attribute_avg['mode'])]}"
    omap["time_signature"] = f"{round(attribute_avg['time_signature'])}"

    omap["acousticness"] = {}
    omap["acousticness"]["val"] = f"{round(attribute_avg['acousticness'],3)}"
    omap["acousticness"]["per"] = f"{round(attribute_percentile['acousticness'])}"

    omap["danceability"] = {}
    omap["danceability"]["val"] = f"{round(attribute_avg['danceability'],3)}"
    omap["danceability"]["per"] = f"{round(attribute_percentile['danceability'])}"

    omap["energy"] = {}
    omap["energy"]["val"] = f"{round(attribute_avg['energy'],3)}"
    omap["energy"]["per"] = f"{round(attribute_percentile['energy'])}"

    omap["instrumentalness"] = {}
    omap["instrumentalness"]["val"] = f"{round(attribute_avg['instrumentalness'],3)}"
    omap["instrumentalness"]["per"] = f"{round(attribute_percentile['instrumentalness'])}"

    omap["liveness"] = {}
    omap["liveness"]["val"] = f"{round(attribute_avg['liveness'],3)}"
    omap["liveness"]["per"] = f"{round(attribute_percentile['liveness'])}"

    omap["loudness"] = {}
    omap["loudness"]["val"] = f"{round(attribute_avg['loudness'],3)}"
    omap["loudness"]["per"] = f"{round(attribute_percentile['loudness'])}"

    omap["speechiness"] = {}
    omap["speechiness"]["val"] = f"{round(attribute_avg['speechiness'],3)}"
    omap["speechiness"]["per"] = f"{round(attribute_percentile['speechiness'])}"

    omap["valence"] = {}
    omap["valence"]["val"] = f"{round(attribute_avg['valence'],3)}"
    omap["valence"]["per"] = f"{round(attribute_percentile['valence'])}"

    omap["tempo"] = {}
    omap["tempo"]["val"] = f"{round(attribute_avg['tempo'],3)}"
    omap["tempo"]["per"] = f"{round(attribute_percentile['tempo'])}"

    return omap

#formats the output for the highest/lowest percentiles in each category
def extreme_oput(high_songs, low_songs):
    omap = {}

    milli = high_songs['duration_ms'][2]
    seconds = round(int((milli/1000)%60),2)
    minutes = round(int((milli/(1000*60))%60),2)
    omap["duration"] = {}
    omap["duration"]["high"] = {}
    omap["duration"]["high"]["song"] = f"{high_songs['duration_ms'][0]}"
    omap["duration"]["high"]["per"] = f"{high_songs['duration_ms'][1]}"
    omap["duration"]["high"]["val"] = f"{minutes}:{seconds}"

    milli = low_songs['duration_ms'][2]
    seconds = round(int((milli/1000)%60),2)
    minutes = round(int((milli/(1000*60))%60),2)
    omap["duration"]["low"] = {}
    omap["duration"]["low"]["song"] = f"{low_songs['duration_ms'][0]}"
    omap["duration"]["low"]["per"] = f"{low_songs['duration_ms'][1]}"
    omap["duration"]["low"]["val"] = f"{minutes}:{seconds}"

    omap["acousticness"] = {}
    omap["acousticness"]["high"] = {}
    omap["acousticness"]["high"]["song"] = f"{high_songs['acousticness'][0]}"
    omap["acousticness"]["high"]["per"] = f"{high_songs['acousticness'][1]}"
    omap["acousticness"]["high"]["val"] = f"{high_songs['acousticness'][2]}"

    omap["acousticness"]["low"] = {}
    omap["acousticness"]["low"]["song"] = f"{low_songs['acousticness'][0]}"
    omap["acousticness"]["low"]["per"] = f"{low_songs['acousticness'][1]}"
    omap["acousticness"]["low"]["val"] = f"{low_songs['acousticness'][2]}"

    omap["danceability"] = {}
    omap["danceability"]["high"] = {}
    omap["danceability"]["high"]["song"] = f"{high_songs['danceability'][0]}"
    omap["danceability"]["high"]["per"] = f"{high_songs['danceability'][1]}"
    omap["danceability"]["high"]["val"] = f"{high_songs['danceability'][2]}"

    omap["danceability"]["low"] = {}
    omap["danceability"]["low"]["song"] = f"{low_songs['danceability'][0]}"
    omap["danceability"]["low"]["per"] = f"{low_songs['danceability'][1]}"
    omap["danceability"]["low"]["val"] = f"{low_songs['danceability'][2]}"

    omap["energy"] = {}
    omap["energy"]["high"] = {}
    omap["energy"]["high"]["song"] = f"{high_songs['energy'][0]}"
    omap["energy"]["high"]["per"] = f"{high_songs['energy'][1]}"
    omap["energy"]["high"]["val"] = f"{high_songs['energy'][2]}"

    omap["energy"]["low"] = {}
    omap["energy"]["low"]["song"] = f"{low_songs['energy'][0]}"
    omap["energy"]["low"]["per"] = f"{low_songs['energy'][1]}"
    omap["energy"]["low"]["val"] = f"{low_songs['energy'][2]}"


    omap["instrumentalness"] = {}
    omap["instrumentalness"]["high"] = {}
    omap["instrumentalness"]["high"]["song"] = f"{high_songs['instrumentalness'][0]}"
    omap["instrumentalness"]["high"]["per"] = f"{high_songs['instrumentalness'][1]}"
    omap["instrumentalness"]["high"]["val"] = f"{high_songs['instrumentalness'][2]}"

    omap["instrumentalness"]["low"] = {}
    omap["instrumentalness"]["low"]["song"] = f"{low_songs['instrumentalness'][0]}"
    omap["instrumentalness"]["low"]["per"] = f"{low_songs['instrumentalness'][1]}"
    omap["instrumentalness"]["low"]["val"] = f"{low_songs['instrumentalness'][2]}"

    omap["liveness"] = {}
    omap["liveness"]["high"] = {}
    omap["liveness"]["high"]["song"] = f"{high_songs['liveness'][0]}"
    omap["liveness"]["high"]["per"] = f"{high_songs['liveness'][1]}"
    omap["liveness"]["high"]["val"] = f"{high_songs['liveness'][2]}"

    omap["liveness"]["low"] = {}
    omap["liveness"]["low"]["song"] = f"{low_songs['liveness'][0]}"
    omap["liveness"]["low"]["per"] = f"{low_songs['liveness'][1]}"
    omap["liveness"]["low"]["val"] = f"{low_songs['liveness'][2]}"
    
    omap["loudness"] = {}
    omap["loudness"]["high"] = {}
    omap["loudness"]["high"]["song"] = f"{high_songs['loudness'][0]}"
    omap["loudness"]["high"]["per"] = f"{high_songs['loudness'][1]}"
    omap["loudness"]["high"]["val"] = f"{high_songs['loudness'][2]}"

    omap["loudness"]["low"] = {}
    omap["loudness"]["low"]["song"] = f"{low_songs['loudness'][0]}"
    omap["loudness"]["low"]["per"] = f"{low_songs['loudness'][1]}"
    omap["loudness"]["low"]["val"] = f"{low_songs['loudness'][2]}"
    
    omap["speechiness"] = {}
    omap["speechiness"]["high"] = {}
    omap["speechiness"]["high"]["song"] = f"{high_songs['speechiness'][0]}"
    omap["speechiness"]["high"]["per"] = f"{high_songs['speechiness'][1]}"
    omap["speechiness"]["high"]["val"] = f"{high_songs['speechiness'][2]}"

    omap["speechiness"]["low"] = {}
    omap["speechiness"]["low"]["song"] = f"{low_songs['speechiness'][0]}"
    omap["speechiness"]["low"]["per"] = f"{low_songs['speechiness'][1]}"
    omap["speechiness"]["low"]["val"] = f"{low_songs['speechiness'][2]}"

    
    omap["valence"] = {}
    omap["valence"]["high"] = {}
    omap["valence"]["high"]["song"] = f"{high_songs['valence'][0]}"
    omap["valence"]["high"]["per"] = f"{high_songs['valence'][1]}"
    omap["valence"]["high"]["val"] = f"{high_songs['valence'][2]}"

    omap["valence"]["low"] = {}
    omap["valence"]["low"]["song"] = f"{low_songs['valence'][0]}"
    omap["valence"]["low"]["per"] = f"{low_songs['valence'][1]}"
    omap["valence"]["low"]["val"] = f"{low_songs['valence'][2]}"

    omap["tempo"] = {}
    omap["tempo"]["high"] = {}
    omap["tempo"]["high"]["song"] = f"{high_songs['tempo'][0]}"
    omap["tempo"]["high"]["per"] = f"{high_songs['tempo'][1]}"
    omap["tempo"]["high"]["val"] = f"{high_songs['tempo'][2]}"

    omap["tempo"]["low"] = {}
    omap["tempo"]["low"]["song"] = f"{low_songs['tempo'][0]}"
    omap["tempo"]["low"]["per"] = f"{low_songs['tempo'][1]}"
    omap["tempo"]["low"]["val"] = f"{low_songs['tempo'][2]}"

    return omap