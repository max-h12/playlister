#run the main script
import requests
import re

import playlister_io as io
import http_request as request
import feat_dist as dist


def main():
    #map of songs, key being song-title, value is a map of attributes
    songs = {}
    #map to hold average of all songs in respective categories
    attribute_avg = {"duration_ms":0, "key":0, "mode":0, "time_signature":0, 
                    "acousticness":0, "danceability":0, "energy":0, "instrumentalness":0, 
                    "liveness":0, "loudness":0, "speechiness":0, "valence":0, "tempo":0}

    #initialize all the distributions
    dist.init()
        
    #get authorization and playlist id from input
    playlist_id = io.get_playlist_id()
    token = request.get_token()

    #get the songs, then load in their features
    request.get_album_tracks(songs, token, playlist_id)
    request.get_song_features(songs, attribute_avg, token)

    io.format_oput(attribute_avg)

if __name__ == "__main__":
    main()

