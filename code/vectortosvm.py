from __future__ import division
import csv, sys, math, os
import numpy as np
from genvector import *

#gestpath = hello
#samplepath = 1
#return string of all samples of one gesture feature
def gen_feat_str(gestpath, flag):
	gestvector = []
	if (flag == 1):
		label = "1"
	else:
		label = "0"

	
	for samplepath in os.listdir(gestpath):
		if (".DS_Store" not in samplepath):
			samplepath = gestpath + "/" + samplepath
			samplevector = gen_samp_feat(samplepath)
			gestvector.append(samplevector)

	vectorstring = ""
	vectorlen = len(gestvector[0])
	for vector in gestvector:
		vectorstring += label + " "
		for index in range(vectorlen):
			vectorstring += str(index) + ":" + str(vector[index]) + " "
		vectorstring += "\n"
	return vectorstring 

#one vs all file
def gen_data_file_one(gestname, inputpath):
	resultstr = ""
	for gestpath in os.listdir(inputpath):
		if not (gestpath.startswith('.')):
			if gestpath == gestname:
				gestpath = inputpath + "/" + gestpath
				resultstr += gen_feat_str(gestpath, True)
			else:
				gestpath = inputpath + "/" + gestpath
				resultstr += gen_feat_str(gestpath, False)
	path =gestname + ".data"
	print(path)
	file = open(path, 'w')
	file.write(resultstr)
	file.close()

#all of the one-vs-all files
def gen_data_file_all(inputpath):
	for gestname in os.listdir(inputpath):
		if not (gestname.startswith('.')):
			gen_data_file_one(gestname, inputpath)


gen_data_file_all(sys.argv[1])









