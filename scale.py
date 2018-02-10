from __future__ import division
import start_end
import csv, sys, math, os
import numpy as np

def make2dList(rows, cols):
    a=[]
    for row in range(rows): a += [[0]*cols]
    return a

def scale(file_acc, file, thres, scale_co):

    (start, end) = start_end.find_startend(file_acc, thres)
    print(start, end)

    data = np.genfromtxt(file, delimiter=",", names=True, dtype=None)

    feat_LL = make2dList(len(data[0]), len(data))

    for i in range(len(feat_LL)):
        for j in range(len(feat_LL[0])):
            feat_LL[i][j] = data[j][i]
    timestamp = feat_LL.pop(0)

    print(start, end)

    result = make2dList(len(data[0])-1, start-end+1)

    for i in range(len(result)):
        result[i] = feat_LL[i][start::end]

    return result








    














