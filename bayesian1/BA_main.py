from __future__ import division
from collections import Counter
import math
from operator import itemgetter
import operator
import random,os
import numpy as np
import sklearn
from sklearn.cluster import KMeans
from scipy.special import gammaln, psi
import cPickle as pickle
import matplotlib.pyplot as plt
from BA_process_data import *
from BA_detect_bot import *
import pandas as pd
from django.conf import settings

#Adjusted from BIRDNEST author's source code to fit project purposes

np.set_printoptions(threshold='nan')
np.set_printoptions(linewidth=160)

#initializing number of clusters
K = 5
def bayesianmain(filepath=None,K=5):
	#MAIN Function
	# @profile
	#import_data()
	dataname = 'AIS_Sailfish'
	if __name__=='__main__':
		fileis="bayesdata.csv"
	else:
		if filepath:
			fileis=filepath
		else:
			fileis="bayesdata.csv"
	#PROCESS data
	#dict_long, dict_lat,dict_deltime,usermap  = load_data(pd.read_csv(fileis))
	#long_arr, lat_arr, time_arr, ids = processing_data(dict_long, dict_lat, dict_deltime, dataname)
	#SAVE variables as pickle to save time
	#pickle.dump((long_arr, lat_arr, time_arr,ids, usermap), open('%s_bucketed.p' % (dataname), 'wb'))
	
	#LOAD processed data
	if dataname+"_bucketed.p" in os.listdir(os.getcwd()):
		long_arr, lat_arr,time_arr, ids, usermap = pickle.load(open('%s_bucketed.p' % (dataname), 'rb'))
	else:
		dict_long, dict_lat,dict_deltime,usermap  = load_data(pd.read_csv(fileis))
		long_arr, lat_arr, time_arr, ids = processing_data(dict_long, dict_lat, dict_deltime, dataname)
		pickle.dump((long_arr, lat_arr, time_arr,ids, usermap), open('%s_bucketed.p' % (dataname), 'wb'))
		
	#FIND anomalous behavior and output scores of each user
	print "suspecting"
	suspect = detect_bot(long_arr, lat_arr, time_arr, K)
	
	
	
	###############################################################
	NUM_TO_OUTPUT = 1500
	#sort the users' scores from highest to lowest
	susp_sorted = np.array([(x[0]) for x in sorted(enumerate(suspect), key=itemgetter(1), reverse=True)])
	most_susp = susp_sorted[range(len(susp_sorted))]
	#create text files to show ranking and distributions in the ranking from anomalous to least anomalous
	with open('%s_top%d_ids.txt' % (dataname, NUM_TO_OUTPUT), 'w') as outfile:
		with open('%s_top%d_scores.txt' % (dataname, NUM_TO_OUTPUT), 'w') as out_scores:
			with open('%s_top%d_lats.txt' % (dataname, NUM_TO_OUTPUT), 'w') as out_lats:
				with open('%s_top%d_longs.txt' % (dataname, NUM_TO_OUTPUT), 'w') as out_longs:
					for i in most_susp:
						if usermap == None:
							print >> outfile, '%s' % (ids[i], )
						else:
							print >> outfile, '%s %s' % (ids[i], usermap[ids[i]-1])
						print >> out_scores, '%d %f' % (ids[i], suspect[i])
						print >> out_lats, lat_arr[i,:]
						print >> out_longs, long_arr[i, :]
	#calculate the distributions of the supposed "good" and "bad" distributions based on bad = 1-103 most anomalous users and good = 103-end
	TOP_N_SUSPECTS = 20
	bad = susp_sorted[range(TOP_N_SUSPECTS)]
	bad_lat_ave = np.array([0]*lat_arr.shape[1], dtype=float)
	good_lat_ave = np.array([0]*lat_arr.shape[1], dtype=float)
	bad_long_ave = np.array([0]*long_arr.shape[1], dtype=float)
	good_long_ave = np.array([0]*long_arr.shape[1], dtype=float)
	for i in range(len(suspect)):
		if(np.sum(lat_arr[i,:]) > 0): #since using complete_iat_arr then need to handle the situation when dividing by zero
			cur_lat = (lat_arr[i,:] / np.sum(lat_arr[i,:]))
		else:
			cur_lat = lat_arr[i,:]
		if i in bad:
			bad_lat_ave += cur_lat
		else:
			good_lat_ave += cur_lat
	#Calculates the normalized distribution of all users
	lat_sums = lat_arr.sum(axis=1)
	for i in range(len(lat_sums)):
		if lat_sums[i] == 0:
			lat_sums[i] = 1 #keep from dividing by zero when normalizing
	lat_norm = lat_arr / lat_sums[:, np.newaxis]
	lat_hist = lat_norm.sum(axis=0)
	lat_hist = lat_hist / np.sum(lat_hist)
	################
	for i in range(len(suspect)):
		if(np.sum(long_arr[i,:]) > 0): #since using complete_iat_arr then need to handle the situation when dividing by zero
			cur_long = (long_arr[i,:] / np.sum(long_arr[i,:]))
		else:
			cur_long = long_arr[i,:]
		if i in bad:
			bad_long_ave += cur_long
		else:
			good_long_ave += cur_long
	#Calculates the normalized distribution of all users
	long_sums = long_arr.sum(axis=1)
	for i in range(len(long_sums)):
		if long_sums[i] == 0:
			long_sums[i] = 1 #keep from dividing by zero when normalizing
	long_norm = long_arr / long_sums[:, np.newaxis]
	long_hist = long_norm.sum(axis=0)
	long_hist = long_hist / np.sum(long_hist)
	
	#Plot good and bad distributions based on algorithm output
	tx = range(1, len(range(len(lat_arr[1,:])+1)))
	fig = plt.figure(figsize=(8, 5))
	plt.subplot(1,2,1)
	plt.bar(tx, good_lat_ave, color='green')
	plt.title('Normal messages', size=18)
	
	plt.subplot(1,2,2)
	plt.bar(tx, bad_lat_ave, color='red')
	plt.title('Detected ships', size=18)
	plt.xlabel('Latitude (bucketized)', size=14)
	fig.text(0.5, 0.02, 'Latitude bucket', ha='center', size=18)
	print settings.BASE_DIR
	plt.savefig(os.path.join(settings.BASE_DIR,'/static/img/AIS_lat_goodbad.png'))
	
	#Plot good and bad distributions based on algorithm output
	tx = range(1, len(range(len(long_arr[1,:])+1)))
	fig = plt.figure(figsize=(8, 5))
	plt.subplot(1,2,1)
	plt.bar(tx, good_long_ave, color='green')
	plt.title('Normal messages', size=18)
	
	plt.subplot(1,2,2)
	plt.bar(tx, bad_long_ave, color='red')
	plt.title('Detected ships', size=18)
	plt.xlabel('Longitude (bucketized)', size=14)
	fig.text(0.5, 0.02, 'Longitude bucket', ha='center', size=18)
	
	plt.savefig(os.path.join(settings.BASE_DIR,'/static/img/AIS_long_goodbad.png'))
	
	buckets = np.arange(lat_arr.shape[1])
	#plot all users noramlzied distribution
	plt.hold(False)
	fig = plt.figure()
	plt.bar(buckets, lat_hist, color='blue')
	plt.title('All ships normalized')
	plt.xlabel('Latitude buckets')
	plt.ylabel('Frequency')
	plt.savefig(os.path.join(settings.BASE_DIR,'/static/img/Distribution_all_ships_lat_only.png'))	
	
	buckets = np.arange(long_arr.shape[1])
	#plot all users noramlzied distribution
	plt.hold(False)
	fig = plt.figure()
	plt.bar(buckets, long_hist, color='blue')
	plt.title('All ships normalized')
	plt.xlabel('Longitude buckets')
	plt.ylabel('Frequency')
	plt.savefig(os.path.join(settings.BASE_DIR,'/static/img/Distribution_all_ships_long_only.png'))