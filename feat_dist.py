#creates distributions of values corresponding to spotifys data
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

#descriptions of distributions of said key
#see more about these distributions at https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/
#TODO: create all dists
ALL_DIST = {"acousticness":[3000,800,625,500,450,400,390,380,350,348,345,340,350,345,320,340,400,405,410,500],
            "danceability":[20,40,75,180,198,250,375,450,600,775,950,1010,1020,1050,1000,825,625,350,175,75],
            "energy":[190,150,200,240,250,300,350,400,495,560,600,650,640,750,770,800,725,720,705,535],
            "instrumentalness":[7600,100,75,50,75,75,50,50,50,25,25,50,50,60,75,100,150,225,300,125],
            "liveness":[250,2450,2900,965,650,500,625,480,200,175,160,155,150,155,160,150,140,145,145,145,160,175]}

#creates an array distributed such that values correspond a histogram described by 'vals'
def create_distribution(vals):
    dist = np.zeros(1)
    i=0
    offset = 0

    #fill array with linearly spaced numbers found from 'vals'
    while i<20:
        temp = np.linspace(offset, offset+0.05, vals[i])
        dist = np.concatenate((dist, temp))
        i+=1
        offset+=0.05
    return dist

#calculates 'num' percentile in distribution 'dist'
def get_percentile(name, num):
    return stats.percentileofscore(ALL_DIST[name],num)

def init():
    #create all the distributions
    for descrip in ALL_DIST:
        ALL_DIST[descrip] = create_distribution(ALL_DIST[descrip])
    
    #song length is normally distributed, approx described as below
    ALL_DIST["duration_ms"] = np.random.normal(242000, scale=75000, size=10000)

    graph = plt.hist(ALL_DIST["liveness"], bins=20)
    plt.show()

def main():
    init()

if __name__ == "__main__":
    main()



