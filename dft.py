from __future__ import division, print_function
import csv, sys, math, os
import numpy as np

#ta for array returned by fft
#oa for original array

def transform(oa):
    ta = np.fft.fft(oa)
    return ta

def find_trans_energy(ta):
    return np.average(np.square(ta[1:]))

def find_trans_entropy(ta):
    entropy = np.abs(ta[1:]) / np.sum(abs_array)
    return np.sum(entropy * np.log(1/entropy))

def find_ori_mean(oa):
    return np.average(oa)

def find_ori_deviation(oa):
    mean = find_ori_mean(oa)
    return np.sqrt(np.sum(np.square(oa - mean)))

def find_ori_correlation(outarray):




    
    



        

