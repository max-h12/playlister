#creates distributions of values corresponding to spotifys data
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

#descriptions of distributions of said key
#see more about these distributions at https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/
#TODO: create all dists
ALL_DIST = {"acousticness":[3000,800,625,500,450,400,390,380,350,348,345,340,350,345,320,340,400,405,410,500]}

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

    graph = plt.hist(ALL_DIST["duration_ms"], bins='auto')
    plt.show()

def main():
    init()

if __name__ == "__main__":
    main()



