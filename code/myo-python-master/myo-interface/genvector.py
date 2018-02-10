from __future__ import division, print_function
from dft import *
from scale import *

#######
#generate feature of one gesture sample
def gen_samp_feat(samplepath):
	raw_data = transform(samplepath)
	vector = []
	for axis in raw_data:
		for time_frame in axis:
			for x in time_frame:
				vector.append(x)
	return vector	



