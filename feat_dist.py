#creates distributions of values corresponding to spotifys data
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

#descriptions of distributions of said key
#see more about these distributions at https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/
FRACTION_DIST = {"acousticness":[3000,800,625,500,450,400,390,380,350,348,345,340,350,345,320,340,400,405,410,500],
            "danceability":[20,40,75,180,198,250,375,450,600,775,950,1010,1020,1050,1000,825,625,350,175,75],
            "energy":[190,150,200,240,250,300,350,400,495,560,600,650,640,750,770,800,725,720,705,535],
            "instrumentalness":[7600,100,75,50,75,75,50,50,50,25,25,50,50,60,75,100,150,225,300,125],
            "liveness":[250,2450,2900,965,650,500,625,480,200,175,160,155,150,155,160,150,140,145,145,145,160,175],
            "speechiness":[4800,2660,800,400,330,250,200,150,100,75,30,30,5,5,5,5,30,50,150,0],
            "valence":[320,380,440,550,510,595,600,650,550,575,585,650,525,540,490,485,475,400,360,315]}

#tempo and loudness are unique, represented by their actual value not a fraction
LOUDNESS = [5,5,5,20,20,20,50,65,75,100,150,200,350,500,960,1550,2750,2850,550,25]
TEMPO = [25,0,0,0,20,40,135,760,1125,1375,1200,1740,1300,760,510,500,250,100,75,10]

#hold all created distributions keyed by their name
ALL_DIST = {}

#creates an array distributed such that values correspond a histogram described by 'vals'
def create_distribution(vals, starting_val, bin_width):
    dist = np.zeros(1)
    i=0
    offset = starting_val

    #fill array with linearly spaced numbers found from 'vals'
    while i<20:
        temp = np.linspace(offset, offset+bin_width, vals[i])
        dist = np.concatenate((dist, temp))
        i+=1
        offset+=bin_width
    return dist

#calculates 'num' percentile in distribution 'dist'
def get_percentile(name, num):
    return stats.percentileofscore(ALL_DIST[name],num)

def init():
    #create all the distributions
    for descrip in FRACTION_DIST:
        ALL_DIST[descrip] = create_distribution(FRACTION_DIST[descrip], 0, 0.05)

    #loudness and tempo are scaled differently, create seperately
    ALL_DIST["loudness"] = create_distribution(LOUDNESS, -40, 2)
    ALL_DIST["tempo"] = create_distribution(TEMPO, 0, 11)

    #song length is normally distributed, approx described as below
    ALL_DIST["duration_ms"] = np.random.normal(242000, scale=75000, size=10000)

    '''
    #If we want to look at the distribution of a particular attribute
    graph = plt.hist(ALL_DIST["speechiness"], bins=20)
    plt.show()
    '''

def main():
    init()

if __name__ == "__main__":
    main()



