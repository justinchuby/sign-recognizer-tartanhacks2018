from __future__ import division, print_function
from dft import *
from scale import *

#generate feature of one gesture sample
def gen_samp_feat(samplepath):
	raw_data = transform(samplepath)
	vector = []
	for axis in raw_data:
		for time_frame in axis:
			dft_frame = fft(time_frame)
			energy = find_trans_energy(dft_frame)
			entropy = find_trans_entropy(dft_frame)
			mean = find_ori_mean(time_frame)
			deviation = find_ori_deviation(time_frame)
			vector.extend([energy, entropy, mean, deviation])
	return vector	



