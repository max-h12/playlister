#run the main script
import requests
import re

import playlist_io as io
import http_request as request
import distributions as dist

NO_PERCENTILE = ["key","mode","time_signature","name"]

def get_overall_percentile(attribute_avg, attribute_percentile):
    #find the percentiles for the overall attribute averages for the entire playlist
    for attr in attribute_avg:
        if attr not in NO_PERCENTILE:
            attribute_percentile[attr] = round(dist.get_percentile(attr,attribute_avg[attr]))

def calculate_extreme_songs(songs, high_songs, low_songs):
    #finds the most extreme song (percentile wise) for every attribute

    #loop through every song and its attributes
    for song in songs:
        for attr in songs[song]:
            if attr not in NO_PERCENTILE:
                percentile = round(dist.get_percentile(attr, songs[song][attr]))
                #if the percentile is more extreme than anything encountered before, store it
                if percentile > high_songs[attr][1]:
                   high_songs[attr] = [songs[song]["name"],percentile, songs[song][attr]]
                if percentile < low_songs[attr][1]:
                   low_songs[attr] = [songs[song]["name"],percentile, songs[song][attr]]

def main():
    #map of all songs, key being song-title, value is a map of attributes
    songs = {}

    #map to hold average of all songs in respective categories
    attribute_avg = {"duration_ms":0, "key":0, "mode":0, "time_signature":0, 
                    "acousticness":0, "danceability":0, "energy":0, "instrumentalness":0, 
                    "liveness":0, "loudness":0, "speechiness":0, "valence":0, "tempo":0}
    
    #hold the percentile of each attribute for the entire playlist as a whole
    attribute_percentile = {}

    #holds the highest percentile songs in each respective category
    high_songs = {"duration_ms":["",0], "acousticness":["",0], "danceability":["",0], "energy":["",0], 
                        "instrumentalness":["",0], "liveness":["",0], "loudness":["",0], "speechiness":["",0], 
                        "valence":["",0], "tempo":["",0]}

    #holds the lowest percentile songs in each respective category
    low_songs = {"duration_ms":["",999], "acousticness":["",999], "danceability":["",999], "energy":["",999], 
                        "instrumentalness":["",999], "liveness":["",999], "loudness":["",999], "speechiness":["",999], 
                        "valence":["",999], "tempo":["",999]}

    #initialize all the distributions
    dist.init()
        
    #get authorization and playlist id from input
    playlist_id = io.get_playlist_id()
    token = request.get_token()

    #get the songs, then load in their features
    request.get_album_tracks(songs, token, playlist_id)
    request.get_song_features(songs, attribute_avg, token)

    #get percentiles for playlist as a whole and for individual songs
    get_overall_percentile(attribute_avg, attribute_percentile)
    calculate_extreme_songs(songs, high_songs, low_songs)

    #print to terminal
    io.basic_oput(attribute_avg, attribute_percentile)
    io.extreme_oput(high_songs,low_songs)

if __name__ == "__main__":
    main()

