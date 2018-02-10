from __future__ import division
import start_end
import csv, sys, math, os
import numpy as np

def make2dList(rows, cols):
    a=[]
    for row in range(rows): a += [[0]*cols]
    return a

def interpolate(L, length):
    xp = np.linspace(0, len(L), num=len(L))
    x = np.linspace(0, len(L), num=length)
    fp = L
    return np.interp(x, xp, fp)

# 1acceleration file 2target file 3threshold for deciding start 


def scale(file_acc, file, thres, bigL=100, smallL=10):

    (start, end) = start_end.find_startend(file_acc, thres)

    data = np.genfromtxt(file, delimiter=",", names=True, dtype='float64')

    feat_ll = make2dList(len(data[0]), len(data))  

    feat_LL = np.array(feat_ll, dtype='float64')

    for i in range(len(feat_LL)):
        for j in range(len(feat_LL[0])):
            feat_LL[i][j] = data[j][i]

    feat_LL = feat_LL[1::]

    result0 = make2dList(len(data[0])-1, start-end+1)

    for i in range(len(result0)):
        result0[i] = interpolate(feat_LL[i][start:end], bigL)
        #result0[i] = feat_LL[i][start:end]

    result = np.array(result0, dtype='float64').flatten()
    result = np.reshape(result, (-1, smallL))

    return result

