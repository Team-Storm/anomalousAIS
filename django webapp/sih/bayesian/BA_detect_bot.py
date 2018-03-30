from __future__ import division
import math
from operator import itemgetter
import operator
import random,os
import cPickle as pickle
import numpy as np
import sklearn
from sklearn.cluster import KMeans
from scipy.special import gammaln, psi

#BIRDNEST source code from author (adjusted for project purposes)
# runs bayesian fraud detection; returns vector of suspiciousness
# (in same order as iat_arr)

# @profile
def fit_alpha(D):
    (m, S) = D.shape
    S = int(S)
    if m <= 1: return [1] * S
    alpha = np.array([3] * S)
    alpha_next = np.array([None] * S)
    row_tot = np.sum(D, axis=1)
    MAX_FIT_ITERS = 100
    for it in range(MAX_FIT_ITERS):
        alpha_sum = np.sum(alpha)
        for s in range(S):
            D_col = D[:, s]
            numer = np.sum(D_col / (D_col + (-1 + alpha[s]) * np.ones(m)))
            denom = np.sum(row_tot / (row_tot + (-1 + alpha_sum) * np.ones(m)))
            alpha_next[s] = alpha[s] * numer / denom
        if np.sum(np.abs(alpha - alpha_next)) < 0.01:
            print "fitting iteration stopped early at iteration", it
            break
        alpha = alpha_next.copy()
        print alpha
    return alpha + 1

# @profile
def lbeta(alpha):
    return sum(math.lgamma(a) for a in alpha) - math.lgamma(sum(alpha))

# @profile
def ldirichlet_pdf(theta, alpha):
    kernel = sum((a - 1) * math.log(t) for a, t in zip(alpha, theta))
    return kernel - lbeta(alpha)

# @profile
def ldirich_multi_pdf(z, alpha):
    npalpha = alpha + z
    return (gammaln(np.sum(alpha)) - gammaln(np.sum(npalpha)) +
            np.sum(gammaln(npalpha)) - np.sum(gammaln(alpha)))

# denomiator of KL divergence, i.e. E_P 1/log Q(x), where P and Q have Dirich
# params alpha, beta;
# http://bariskurt.com/kullback-leibler-divergence-between-two-dirichlet-and-beta-distributions/
# @profile
def kl_denom(alpha, beta):
    # psi_sum = psi(sum(alpha))
    # psi_diff = sum([beta[k] * (psi_sum - psi(alpha[k])) for k in range(len(beta))])
    psi_diff = np.sum(beta * (psi(sum(alpha)) - psi(alpha)))
    return -math.lgamma(np.sum(beta)) + np.sum([math.lgamma(x) for x in np.squeeze(beta)]) + psi_diff

def detect_bot(long_arr, lat_arr,del_time,K):
    m = long_arr.shape[0]
    print long_arr.shape,del_time.shape
    long_sums = long_arr.sum(axis=1) + 0.1
    lat_sums = lat_arr.sum(axis=1) + 0.1
    del_timesums = del_time.sum(axis=1) + 0.1
    long_normal = long_arr / long_sums[:, np.newaxis]
    lat_normal = lat_arr / lat_sums[:, np.newaxis] 
    del_timenormal=del_timesums/del_timesums[:,np.newaxis] #Normalize
    user_normal = np.concatenate((long_normal, lat_normal,del_timenormal), axis=1)

    #Itialize cluster assignment with Kmeans
    if "kmeansdata.p" in os.listdir(os.getcwd()):
		est= pickle.load(open('kmeansdata.p', 'rb'))
    else:
		est = KMeans(n_clusters=K)
		est.fit(user_normal) #changed from user_normal that concatenated rating_arr with iat_arr
		pickle.dump(est, open('kmeansdata.p', 'wb'))
    z = np.array(est.labels_)

    pi = [None] * K
    zn = np.array([-1] * m)  # z_next
    (m, S1) = long_arr.shape
    (m, S2) = lat_arr.shape
    (m, S3) = del_time.shape
    alpha1 = np.array([[0] * S1 for _ in range(K)], dtype=float)
    alpha2 = np.array([[0] * S2 for _ in range(K)], dtype=float)
    alpha3 = np.array([[0] * S3 for _ in range(K)], dtype=float)

    NUM_FIT_ITERS = 100
    for it in range(NUM_FIT_ITERS):
        print "iteration ", it
        for k in range(K):
            # All users in k cluster
            cur_idx = np.array((z == k))
            long_sub = long_arr[cur_idx, :]
            lat_sub = lat_arr[cur_idx, :]
            del_timesub = del_time[cur_idx, :]
            # Calculate how many in cluster k to calculate the cluster prior (pi)
            n_k = np.sum(cur_idx)
            # Calculate the cluster prior
            pi[k] = n_k / m
            # Find randomized subsample of data in cluster to get best fit hyperparameters
            if n_k > 1000:
                sample_idx = np.array(random.sample(range(n_k), 1000))
            else:
                sample_idx = range(n_k)
            # print "subset size is ", len(sample_idx)
            long_sub = long_sub[sample_idx, :]
            lat_sub = lat_sub[sample_idx, :]
            del_timesub = del_timesub[sample_idx, :]
            # Use maximum-likelhood to fit hyperparameters to sub sample of distributions in cluster k
            alpha1[k, :] = fit_alpha(long_sub)
            alpha2[k, :] = fit_alpha(lat_sub)
            alpha3[k, :] = fit_alpha(del_timesub)
        # print " alpha1 = ", alpha1
        # print " alpha2 = ", alpha2

        # Reassign the user's cluster assignment (Dirichlet-Mulitnomial Distribution - Max Likelihood)
        print "fitting points"
        for i in range(m):
            log_likes = [(ldirich_multi_pdf(long_arr[i, :], alpha1[k]) +
                          ldirich_multi_pdf(lat_arr[i, :], alpha2[k]) + ldirich_multi_pdf(del_time[i, :], alpha3[k])) for k in range(K)]
            zn[i] = log_likes.index(max(log_likes))
        num_diff = sum(abs(zn - z))
        z = zn
        # Test for convergence
        if num_diff == 0:
            print "Outer iteration stopped early at iteration ", it
            break
    # Calcuate posterior distribution of rsp and iat of each user
    post_long = np.array(long_arr, dtype='float')
    post_lat = np.array(lat_arr, dtype='float')
    post_deltime = np.array(del_time, dtype='float')
    for i in range(m):
		post_long[i, :] += alpha1[z[i]]
		post_lat[i, :] += alpha2[z[i]]
		post_deltime[i, :] += alpha3[z[i]]

    # normalize scores to sum
    susp1 = np.zeros(m)
    susp2 = np.zeros(m)
    susp3 = np.zeros(m)
    for i in range(m):
        if i % 100000 == 0: print i
        susp1[i] = max([kl_denom(post_long[i, :], alpha1[k, :]) for k in range(K)])
        susp2[i] = max([kl_denom(post_lat[i, :], alpha2[k, :]) for k in range(K)])
        susp3[i] = max([kl_denom(post_deltime[i, :], alpha3[k, :]) for k in range(K)])

    susp1n = susp1 / np.std(susp1)
    susp2n = susp2 / np.std(susp2)
    susp3n = susp3 / np.std(susp3)
    suspn = susp1n + susp2n + susp3n
    return suspn