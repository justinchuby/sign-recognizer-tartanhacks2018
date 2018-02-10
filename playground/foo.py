import numpy as np
from numpy.fft import fft, fftfreq

def foo():
    a = [1,0,1,0,1,-1,0,1,0,-1, 100, 50, -50, -100]
    a_dft = fft(a)
    a_freq = fftfreq(len(a))
    print(a_dft)
    print(a_freq)

foo()