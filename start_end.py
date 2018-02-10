from __future__ import division
import math

def read_one(path, thres):

    data = np.genfromtxt(path, delimiter=",", names=True, dtype=None)
    start, end = 0, 0
    for i in range(len(data)):
        if (abs(data[i][1]) < thres and start == 0):
            start = data[i][0]
        if (abs(data[len(data)-i-1][1]) < thres and end == 0):
            end = data[len(data)-i-1][0]
    return (start, end)















