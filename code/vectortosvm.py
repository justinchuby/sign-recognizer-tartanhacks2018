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

	for samplepath in gestpath:
		samplevector = genvector(samplepath)
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
def gen_data_file_one(gestname, outputpath):
	resultstr = ""
	for gestpath in inputpath:
		if gestpath == gestname:
			resultstr += gen_feat_str(gestpath, true)
		else:
			resultstr += gen_feat_str(gestpath, false)
	path = outputpath + "/" + gestname + ".data"
	file = open(path, 'w')
	file.write(resultstr)
	file.close()

#all of the one-vs-all files
def gen_data_file_all(inputpath, outputpath):
	for gestname in inputpath:
		gen_data_file_one(gestname, outputpath)













