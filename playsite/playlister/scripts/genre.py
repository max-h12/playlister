import json
from . import http_request as request
from os import path
from . import distributions as dist

PLAYLIST_NO = 2
NO_SCALE = ["duration_ms","tempo","loudness"]
genre_attr = {}
match_map = {"classic rock":0,"electronic":0,"jazz":0,"country":0,"pop":0,"rap":0,"classical":0,"folk":0}
ALL_GENRES = ["classic rock","electronic","jazz","country","pop","rap","classical","folk"]

#TODO: use percentiles not actual values
def find_best_match(playlist_percentile):    
    global genre_attr
    genre_percentile = {}

    for g in genre_attr:
        dist.get_overall_percentile(genre_attr[g], genre_percentile)
        for key in genre_percentile:
            match_map[g] += (((genre_percentile[key]) - (playlist_percentile[key]))**2)

    
    sort = sorted(match_map.items(), key=lambda x: x[1])
    return sort

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
    global genre_attr
    file_path = f"{path.dirname(path.realpath(__file__))}/genre_data_{PLAYLIST_NO}.json"
    #if genre data has not been found, gather it
    #this will take a long time (up to 30min)
    if not path.exists(file_path):
        print("genre not found")
        token = request.get_token()
        for genre in ALL_GENRES:
            genre_attr[genre] = get_genre_attr(genre,PLAYLIST_NO,token)
        with open(f"genre_data_{PLAYLIST_NO}.json",'w') as f:
            json.dump(genre_attr, f, indent=4)
        f.close()
    else:
        with open(file_path) as f:
            data = json.load(f)
            genre_attr = data
        f.close()
    
def main():
    init()

if __name__ == "__main__":
    main()



