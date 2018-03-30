import simplejson as sj
from os import listdir
from os.path import isfile, join
import pandas as pd
from optics import Optics, Point
import math
import datetime
import sys

def main(i):
    '''
    directory = '../AIS_Sailfish/'
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    frame = []
    for file in files:
        with open(join(directory,file), 'r') as f:
            data = f.readlines()
            data = map(lambda x: x.rstrip(), data)
            data_json_str = "[" + ','.join(data) + "]"
            frame.append(pd.read_json(data_json_str))
    df = pd.concat(frame, ignore_index=True)

    df.to_pickle("dataframe.p")
    '''
    #print df

    df = pd.read_pickle("dataframe.p")
    #find_max_lat_long(df)
    #max_time = df.loc[df['timestamp'].idxmax()]
    #min_time = df.loc[df['timestamp'].idxmin()]
    '''
    #weird headers
    weird = df['heading'] > 360
    weirder = df['heading'] != 511
    print df[weird & weirder] #367147022 and 367078768 have a heading of 510 which is weird
    #weird courses
    print df[df['course'] > 360]

    #split into groups of 60 minutes in time from one another
    group_ranges = []
    group_ranges.append(min_time["timestamp"])
    while group_ranges[-1] <= max_time["timestamp"]:
        group_ranges.append(group_ranges[-1]+datetime.timedelta(days=1))

    for i in range(1,len(group_ranges)):
        dataframe = df[(group_ranges[i-1]<=df['timestamp']) & (df['timestamp']<group_ranges[i])]
        dataframe.to_pickle('group%i.p' % (i))
    '''
    #if i != 0:
    #    dataframe = pd.read_pickle("group%i.p" %(i))
    #    cluster(dataframe,i)

    print "Anomalous Vessel not in Cluster"
    print df[df['mmsi'] == 367012660]

    print "High BIRDNEST score Vessels"
    print df[df['mmsi'] == 507027]
    print "--------------------------------------"
    print df[df['mmsi'] == 367012660]
    print "--------------------------------------"
    print df[df['mmsi'] == 367371830]
    print "--------------------------------------"
    print df[df['mmsi'] == 311000167]
    print "--------------------------------------"
    print df[df['mmsi'] == 366902260]
    print "--------------------------------------"
    print df[df['mmsi'] == 369235000]
    print "--------------------------------------"
    print df[df['mmsi'] == 366643140]
    print "--------------------------------------"
    print df[df['mmsi'] == 538001582]
    print "--------------------------------------"
    print df[df['mmsi'] == 369134000]
    print "--------------------------------------"
    print df[df['mmsi'] == 538003543]
    print "--------------------------------------"
    print df[df['mmsi'] == 367097970]
    print "--------------------------------------"
    print df[df['mmsi'] == 367469560]

def find_max_lat_long(df):
    print df.loc[df['latitude'].idxmax()]
    print df.loc[df['longitude'].idxmax()]

    print df.loc[df['latitude'].idxmin()]
    print df.loc[df['longitude'].idxmin()]

def cluster(df,i):
    lat = df['latitude']
    long = df['longitude']
    mmsi_id = df['mmsi']
    points = []
    for latitude , longitude, userid in zip(lat, long, mmsi_id):
        if math.isnan(latitude) or math.isnan(longitude):
            continue

        points.append(Point(latitude,longitude, str(userid)))


    optics = Optics(points, 50, 5)  # 100m radius for neighbor consideration, cluster size >= 2 points
    optics.run()  # run the algorithm
    clusters = optics.cluster(40)  # 50m threshold for clustering
    j = 1
    for cluster in clusters:
        if j == 1:
            outfile = open('day%i_cluster%i.txt' %(i,j), 'w')
        else:
            outfile = open('day%i_cluster%i.txt' % (i,j), 'a')
        j += 1
        print >> outfile, cluster.points


if __name__ == "__main__":
    #for args in sys.argv:
    #    print args
    #if len(sys.argv) == 2:
    #    main(int(sys.argv[1]))
    #else:
        #print "You have more than one argument that is suppose to be the group number you want to cluster"
        #main(0)
    main(0)