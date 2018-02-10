from __future__ import division, print_function
import csv, sys, math, os
import numpy as np

#dft_frame for array returned by fft
#time_frame for original array

def fft(time_frame):
    dft_frame = np.fft.fft(time_frame)
    return dft_frame

def find_trans_mean(dft_frame):
    return dft_frame[0]
    
def find_trans_energy(dft_frame):
    return np.average(np.square(dft_frame[1:]))

def find_trans_entropy(dft_frame):
    abs_array = np.abs(dft_frame[1:])
    entropy = abs_array / np.sum(abs_array)
    return np.sum(entropy * np.log(1/entropy))

def find_ori_mean(time_frame):
    return np.average(time_frame)

def find_ori_deviation(time_frame):
    mean = find_ori_mean(time_frame)
    return np.sqrt(np.sum(np.square(time_frame - mean)))

# def find_ori_correlation(signal_1, signal_2):
#     var = np.average(signal_1 * signal_2) / 2
#     mean_product = find_ori_mean(signal_1)





    
    



        

