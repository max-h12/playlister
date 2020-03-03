import json
import http_request as request
from os import path

ALL_GENRES = ["classic rock","electronic","jazz","country","pop","rap","classical","folk"]

#get the attribute averages for a particular genre of music
#uses playlist_no to determine how many playlists to bring in
def get_genre_attr(genre, playlist_no, token):
    songs = {}
    temp = {}
    #averages
    genre_avg = {"duration_ms":0, "key":0, "mode":0, "time_signature":0, 
                "acousticness":0, "danceability":0, "energy":0, "instrumentalness":0, 
                "liveness":0, "loudness":0, "speechiness":0, "valence":0, "tempo":0}

    #get the top (playlist_no) playlists pertaining to the genre
    ids = request.search_for_playlists(genre,playlist_no,token)
    #for every playlist found, get all of its songs
    for playlist_id in ids:
        request.get_playlist_tracks(temp, token, playlist_id)
        songs = {**songs, **temp}
    #after we have all the songs, get their attributes and save partial averages
    request.get_song_features(songs,genre_avg,token)
    return genre_avg

def init():
    GENRE_ATTRS = {}

    #if genre data has not been found, gather it
    #this will take a long time (up to 30min)
    if not path.exists("genre_data.json"):
        token = request.get_token()
        for genre in ALL_GENRES:
            GENRE_ATTRS[genre] = get_genre_attr(genre,5,token)
        with open('genre_data.json','w') as f:
            json.dump(GENRE_ATTRS, f, indent=4)
        f.close()
    else:
        with open('genre_data.json') as f:
            data = json.load(f)
            GENRE_ATTRS = data
        f.close()

    print(GENRE_ATTRS)

def main():
    init()

if __name__ == "__main__":
    main()