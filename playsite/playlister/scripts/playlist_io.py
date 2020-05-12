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

#formats the attribute averages and percentiles for display to user in terminal
def basic_oput(attribute_avg, attribute_percentile):
    oput = []
    oput.append("\nPlaylist Average Stats:\n")
    milli = attribute_avg['duration_ms']
    seconds = round(int((milli/1000)%60),2)
    minutes = round(int((milli/(1000*60))%60),2)
    oput.append(f"Average duration: {minutes}:{seconds}")
    oput.append(f">> This is in the {attribute_percentile['duration_ms']}th percentile")

    est_pitch = round(attribute_avg['key'])
    if(PITCH_MAP.__contains__(est_pitch)):
        oput.append(f"Overall key average: {PITCH_MAP[est_pitch]}")
    else:
        oput.append("Overall key average: Unknown")
    oput.append(f"Major/Minor Average: More {MODE_MAP[round(attribute_avg['mode'])]}")
    oput.append(f"Average Time Signature (beats per bar/measure): {round(attribute_avg['time_signature'])}")

    oput.append(f"Average Acousticness (confidence a track is acoustic)[0.0 - 1.0]: {round(attribute_avg['acousticness'],3)}")
    oput.append(f">> This is in the {attribute_percentile['acousticness']}th percentile")

    oput.append(f"Average Danceability [0.0 - 1.0]: {round(attribute_avg['danceability'],3)}")
    oput.append(f">> This is in the {attribute_percentile['danceability']}th percentile")

    oput.append(f"Average Energy [0.0 - 1.0]: {round(attribute_avg['energy'],3)}")
    oput.append(f">> This is in the {attribute_percentile['energy']}th percentile")
    
    oput.append(f"Average Instrumentalness (confidence there are no words) [0.0 - 1.0]: {round(attribute_avg['instrumentalness'],3)}")
    oput.append(f">> This is in the {attribute_percentile['instrumentalness']}th percentile")

    oput.append(f"Average Liveness (confidence song was recorded in front of an audience) [0.0 - 1.0]: {round(attribute_avg['liveness'],3)}")
    oput.append(f">> This is in the {attribute_percentile['liveness']}th percentile")

    oput.append(f"Average Loudness [-60db - 0db]: {round(attribute_avg['loudness'],3)}db")
    oput.append(f">> This is in the {attribute_percentile['loudness']}th percentile")

    oput.append(f"Average Speechiness [0.0 - 1.0]: {round(attribute_avg['speechiness'],3)}")
    oput.append(f">> This is in the {attribute_percentile['speechiness']}th percentile")

    oput.append(f"Average Valence (how cheerful the track is) [0.0 - 1.0]: {round(attribute_avg['valence'],3)}")
    oput.append(f">> This is in the {attribute_percentile['valence']}th percentile")

    oput.append(f"Average Tempo (BPM): {round(attribute_avg['tempo'],3)}")
    oput.append(f">> This is in the {attribute_percentile['tempo']}th percentile")

    oput.append("============================================================")
    return oput

#formats the output for the highest/lowest percentiles in each category
def extreme_oput(high_songs, low_songs):
    oput = []
    oput.append("\nMost Extreme Individual Songs:\n")

    oput.append(f"The longest song was {high_songs['duration_ms'][0]}, in the {high_songs['duration_ms'][1]}th percentile!")
    milli = high_songs['duration_ms'][2]
    seconds = round(int((milli/1000)%60),2)
    minutes = round(int((milli/(1000*60))%60),2)
    oput.append(f">> duration of {minutes}:{seconds}")

    oput.append(f"The shortest song was {low_songs['duration_ms'][0]}, in the {low_songs['duration_ms'][1]}th percentile!")
    milli = low_songs['duration_ms'][2]
    seconds = round(int((milli/1000)%60),2)
    minutes = round(int((milli/(1000*60))%60),2)
    oput.append(f">> duration of {minutes}:{seconds}")

    oput.append(f"The most acoustic sounding song was {high_songs['acousticness'][0]}, in the {high_songs['acousticness'][1]}th percentile!")
    oput.append(f">> coefficient of {high_songs['acousticness'][2]}")

    oput.append(f"The least acoustic sounding song was {low_songs['acousticness'][0]}, in the {low_songs['acousticness'][1]}th percentile!")
    oput.append(f">> coefficient of {low_songs['acousticness'][2]}")

    oput.append(f"The most danceable song was {high_songs['danceability'][0]}, in the {high_songs['danceability'][1]}th percentile!")
    oput.append(f">> coefficient of {high_songs['danceability'][2]}")

    oput.append(f"The least danceable song was {low_songs['danceability'][0]}, in the {low_songs['danceability'][1]}th percentile!")
    oput.append(f">> coefficient of {low_songs['danceability'][2]}")

    oput.append(f"The most energetic song was {high_songs['energy'][0]}, in the {high_songs['energy'][1]}th percentile!")
    oput.append(f">> coefficient of {high_songs['energy'][2]}")

    oput.append(f"The least energetic song was {low_songs['energy'][0]}, in the {low_songs['energy'][1]}th percentile!")
    oput.append(f">> coefficient of {low_songs['energy'][2]}")

    oput.append(f"The most instrumental song was {high_songs['instrumentalness'][0]}, in the {high_songs['instrumentalness'][1]}th percentile!")
    oput.append(f">> coefficient of {high_songs['instrumentalness'][2]}")

    oput.append(f"The least instrumental song was {low_songs['instrumentalness'][0]}, in the {low_songs['instrumentalness'][1]}th percentile!")
    oput.append(f">> coefficient of {low_songs['instrumentalness'][2]}")

    oput.append(f"The most live song was {high_songs['liveness'][0]}, in the {high_songs['liveness'][1]}th percentile!")
    oput.append(f">> coefficient of {high_songs['liveness'][2]}")

    oput.append(f"The least live song was {low_songs['liveness'][0]}, in the {low_songs['liveness'][1]}th percentile!")
    oput.append(f">> coefficient of {low_songs['liveness'][2]}")

    oput.append(f"The loudest song was {high_songs['loudness'][0]}, in the {high_songs['loudness'][1]}th percentile!")
    oput.append(f">> {high_songs['loudness'][2]}db")

    oput.append(f"The quietest song was {low_songs['loudness'][0]}, in the {low_songs['loudness'][1]}th percentile!")
    oput.append(f">> {low_songs['loudness'][2]}db")

    oput.append(f"The wordiest song was {high_songs['speechiness'][0]}, in the {high_songs['speechiness'][1]}th percentile!")
    oput.append(f">> coefficient of {high_songs['speechiness'][2]}")

    oput.append(f"The least wordy song was {low_songs['speechiness'][0]}, in the {low_songs['speechiness'][1]}th percentile!")
    oput.append(f">> coefficient of {low_songs['speechiness'][2]}")

    oput.append(f"The happiest song was {high_songs['valence'][0]}, in the {high_songs['valence'][1]}th percentile!")
    oput.append(f">> coefficient of {high_songs['valence'][2]}")

    oput.append(f"The saddest song was {low_songs['valence'][0]}, in the {low_songs['valence'][1]}th percentile!")
    oput.append(f">> coefficient of {low_songs['valence'][2]}")

    oput.append(f"The fastests song was {high_songs['tempo'][0]}, in the {high_songs['tempo'][1]}th percentile!")
    oput.append(f">> {high_songs['tempo'][2]}BPM")

    oput.append(f"The slowest song was {low_songs['tempo'][0]}, in the {low_songs['tempo'][1]}th percentile!")
    oput.append(f">> {low_songs['tempo'][2]}BPM")
    return oput