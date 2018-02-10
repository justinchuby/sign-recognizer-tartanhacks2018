import numpy as np
import scipy as sy
import scipy.fftpack as syfp
import pylab as py

array = np.loadtext("data.csv")
length = len(array)

x = sy.linspace(0.0001, length*0.00001, num=length)

FFT = sy.fft(array)
freqs = syfp.fftfreq(array.size)