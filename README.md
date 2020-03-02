# playlister
## Analyze Spotify songs/playlists.
* Uses Python HTTP requests to Spotify API to gather data for songs and playlists.

##### **TO RUN**: 
##### 1) Download folder 
##### 2) create 'key.py' and set variables client_id and client_secret to respective keys (from spotify developer account)
##### 3) run main.py

Current Functionality
* Take a public playlist URL, grabs all tracks, request interesting statistics
* Uses published spotify data to create realistic data distributions (used to calculate percentile values)
* Reports playlist averages in many attribute categories 
* Reports percentiles for these attribute averages
* Reports most extreme songs in attribute categories (with percentiles)

TODO
* ~~Implement distributions to compute percentiles overall~~
* ~~Calculate extreme songs and percentiles~~
* Implement a 'genre' guesser
	* Gather data on main generes
	* Compare found statistics to guess
* Create a front end
* Host online
