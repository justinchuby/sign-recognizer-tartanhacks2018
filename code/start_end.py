from __future__ import division
import numpy as np
import math

def find_startend(path, thres):

    data = np.genfromtxt(path, delimiter=",", names=True, dtype=None)
    start, end = 0, 0
    for i in range(len(data)):
        if (data[i][1] < thres and start == 0):
            start = i
        if (data[len(data)-i-1][1] < thres and end == 0):
            end = len(data)-i-1
    
    return (start, end)















