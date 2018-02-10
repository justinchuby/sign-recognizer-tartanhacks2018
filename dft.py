from __future__ import division, print_function
import csv, sys, math, os
import numpy as np

def transform(ori_array):
    trans_array = np.fft.fft(ori_array)
    return trans_array

def find_trans_energy(trans_array):
    squared_array = list(map(lambda x : x*x, trans_array[1:]))
    energy = math.sum(squared_array) / (len(squared_array))
    return energy

def find_trans_entropy(trans_array):
    abs_array = list(map(lambda x : abs(x), trans_array[1:]))
    abs_sum = math.sum(absval_array)

    def map_entropy(val):
        p = abs(val) / abs_sum
        entropy = p * math.log(1/p)
        return entropy

    entropy_array = list(map(map_entropy, trans_array))
    entropy = math.sum(entropy_array)
    return entropy

def find_ori_mean(ori_array):
    return math.sum(ori_array)/len(ori_array)

def find_ori_deviation(ori_array):
    mean = find_ori_mean(ori_array)

    def map_deviation(val):
        return math.square(val-mean)

    deviation_sum = list(map(map_deviation, ori_array))

    return np.sqrt(deviation_sum)

def find_ori_



    
    



        

