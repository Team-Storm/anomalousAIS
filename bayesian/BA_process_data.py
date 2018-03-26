import numpy as np
#import csv
import math
#import operator
#import cPickle as pickle
#import sys
#import pandas as pd
#from os import listdir
#from os.path import isfile, join
#from collections import Counter

#Adjusted from BIRDNEST author's source code to fit project purposes

NUM_BUCKETS = 500 #Changed from 5
TIME_LOG_BASE = 5

def load_data(df):
    #Take data from csv file to sequence/lists to later process into histograms
    outfile = open('preproc_out.txt', 'w')
    dict_lat = {}
    dict_long = {}
    dict_deltime={}
    usermap = list()  # {user: (bidder_id, label)}
    counter = 1
    usernames = df['VESSEL_ID']#df['mmsi']
    lat = df['LATITUDE']
    longit = df['LONGITUDE']
    del_time=df['DelTime']
    idx = 0
    for username in usernames:
        if math.isnan(lat[idx]) or math.isnan(longit[idx]) or math.isnan(del_time[idx]):
            idx +=1
            continue #for all ais that do not have lat or long specify, ignore
        if username not in usermap:
            bidder=counter
            usermap.append(username)
            counter += 1
        if bidder not in dict_long:
            dict_long[bidder] = []
        if bidder not in dict_lat:
            dict_lat[bidder] = []
	if bidder not in dict_deltime:
            dict_deltime[bidder] = []
        dict_long[bidder].append(longit[idx])
        dict_lat[bidder].append(lat[idx])
	dict_deltime[bidder].append(del_time[idx])
        idx+=1
    print >> outfile, '%s bidders before taking out users with not enough data' %(bidder)
    return dict_long, dict_lat,dict_deltime,usermap 


def processing_data(dict_long, dict_lat,dict_deltime,dataname):
    lat_arr = []
    long_arr = []
    iat_arr=[]
    ids = []
    #find bounds for the histogram
    sorted_lat=[]
    sorted_long = []
    sorted_time=[]
    max_time_diff = -1
    dict_data={}
    for (k1,v1),(k2,v2),(k3,v3) in zip(dict_lat.iteritems(),dict_long.iteritems(),dict_deltime.iteritems()):
	if k1==k2 and k2==k3:
	    dict_data[k1]=zip(v1,v2,v3)
    for key, values in dict_lat.iteritems():
        for value in values:
            sorted_lat.append(value)
    for key, values in dict_long.iteritems():
        for value in values:
            sorted_long.append(value)
    for key, values in dict_deltime.iteritems():
        for value in values:
            sorted_time.append(value)
    print len(dict_data)
    #print zip(sorted_long,sorted_lat,sorted_time)
    #sorted_lat = sorted(dict_lat.items(), key=operator.itemgetter(1))
    #sorted_long = sorted(dict_long.items(), key=operator.itemgetter(1))
    max_long = max(sorted_long)+.00000001
    max_lat = max(sorted_lat)+.000000001
    min_long = min(sorted_long)
    min_lat = min(sorted_lat)
    max_time=max(sorted_time)
    # already sorted

    # number of buckets
    Slo = NUM_BUCKETS
    Sla = NUM_BUCKETS

    #ranges in bucket
    range_lat=[min_lat]
    range_long = [min_long]
    for m in range(1,NUM_BUCKETS):
        range_lat.append(min_lat + ((max_lat - min_lat) / NUM_BUCKETS)*m)
        range_long.append(min_long + ((max_long - min_long)/NUM_BUCKETS)*m)

    range_lat[-1] = max_lat
    range_long[-1] = max_long

    for user in dict_long:
        long_counts = [0] * Slo
        lat_counts = [0] * Sla
        
        for longs in dict_long[user]:
            bucket = [index for index in range(1,len(range_long)) if longs < range_long[index] and longs >= range_long[index-1] ]#calculate which bucket the point belongs in
            long_counts[bucket[0]-1]+=1
        long_arr.append(long_counts)
        for lats in dict_lat[user]:
            bucket = [index for index in range(1,len(range_lat)) if lats < range_lat[index] and lats >= range_lat[index-1] ]#calculate which bucket the point belongs in
            lat_counts[bucket[0]-1]+=1
        lat_arr.append(lat_counts)
        ids.append(user)

    S = int(1 + math.floor(math.log(1 + max(max_time,max_time_diff), TIME_LOG_BASE)))
    count=0
    for vessel,data in dict_data.iteritems():
	#if len(data) <= 1: continue
	count+=1
	#vesseldata_counts = [0] * len(dict_data[vessel])
	iat_counts = [0] * S
	#cur_data = sorted(ratings[user], key=operator.itemgetter(1))
	#vesseldata_counts[data[0][2] - 1] += 1
	#print data
	for i in data:
                #print i,"     ",i[2]
                #print vessel
		time_diff = max(float(i[2]),max_time_diff)#cur_ratings[i][1] - cur_ratings[i-1][1]
		iat_bucket = int(math.floor(math.log(1 + time_diff, TIME_LOG_BASE)))
		#rating_counts[cur_ratings[i][2] - 1] += 1
		iat_counts[iat_bucket] += 1
	#rating_arr.append(rating_counts)
	iat_arr.append(iat_counts)
	#ids.append(user)
    print "count",count

    with open('%s_lat_bucketed.txt' % (dataname), 'w') as lat_file:
        for row in lat_arr:
            print >> lat_file, ' '.join([str(x) for x in row])
    with open('%s_long_bucketed.txt' % (dataname), 'w') as long_file:
        for row in long_arr:
            print >> long_file, ' '.join([str(x) for x in row])
    with open('%s_iat_bucketed.txt' % (dataname), 'w') as iat_file:
	for row in iat_arr:
	    print >> iat_file, ' '.join([str(x) for x in row])

    lat_arr = np.array(lat_arr)
    long_arr = np.array(long_arr)
    time_arr=np.array(iat_arr)
    return (lat_arr, long_arr, time_arr, ids)
