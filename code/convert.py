from __future__ import division
import csv, sys, math, os
import numpy as np

##########################helper functions######################################

def make2dList(rows, cols):
    a=[]
    for row in range(rows): a += [[0]*cols]
    return a
    
##########################main######################################

###read

def reduce(L):
    result = []
    for i in range(0, len(L), 12):
        result.append(round(sum(L[i:i+12])/12, 3))
    #print(result)
    #print("\n")
    return result


def read_one(path):
    data = np.genfromtxt(path, delimiter=",", names=True, dtype=None)
    names = list(data.dtype.names)

    feat_LL = make2dList(len(data[0]), len(data))

    for i in range(len(feat_LL)):
        for j in range(len(feat_LL[0])):
            feat_LL[i][j] = data[j][i]

    timestamp = feat_LL.pop(0)

    for i in range(len(feat_LL)):
        feat_LL[i] = reduce(feat_LL[i])

    merged_L = []

    for x in feat_LL:
        merged_L+=x

    return merged_L

result_L = []
path_true = sys.argv[1]
path_false = sys.argv[2]

for filename in os.listdir(path_true):
    if not (filename.startswith('.')):
        result_L.append(read_one(path_true + "/" + filename))

true_len = len(result_L)

for filename in os.listdir(path_false):
    if not (filename.startswith('.')):
        result_L.append(read_one(path_false + "/" + filename))

####write

len_L = []
for x in result_L:
    len_L.append(len(x))
length = min(len_L)

result_str = ""
file = open(sys.argv[3], 'w')

for i in range(true_len):
    result_str += "1" + " "
    for j in range(length):
        result_str += str(j) + ":" + str(result_L[i][j]) + " "
    result_str += "\n"

for i in range(true_len, len(result_L)):
    result_str += "0" + " "
    for j in range(length):
        result_str += str(j) + ":" + str(result_L[i][j]) + " "
    result_str += "\n"

file.write(result_str)
file.close()

















