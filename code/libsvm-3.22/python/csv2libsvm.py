#!/usr/bin/env python

"""
Modified:
(1) -1 is now accepted as argv[2], this will print result to stdout instead of writing to file
(2) string labels(classes) are now mapped to categorical float values
Convert CSV file to libsvm format. Works only with numeric variables.
Put -1 as label index (argv[3]) if there are no labels in your file.
Expecting no headers. If present, headers can be skipped with argv[4] == 1.
"""

import sys
import csv

def construct_line( label, line ):
	new_line = []
	try:
		if float( label ) == 0.0:
			label = "0"
	except:
		return -9999

	new_line.append( label )
	
	for i, item in enumerate( line ):
		if item == '' or float( item ) == 0.0:
			continue
		new_item = "%s:%s" % ( i + 1, item )
		new_line.append( new_item )
	new_line = " ".join( new_line )
	new_line += "\n"
	return new_line

def construct_line_string( label, line, class_dict):
	new_line = []
	new_line.append( label )
	
	for i, item in enumerate( line ):
		if item == '' or float( item ) == 0.0:
			continue
		new_item = "%s:%s" % ( i + 1, item )
		new_line.append( new_item )
	new_line = " ".join( new_line )
	return new_line

# ---

input_file = sys.argv[1]

if sys.argv[2] == '-1':
	pass
else:
	output_file = sys.argv[2]

try:
	label_index = int( sys.argv[3] )
except IndexError:
	label_index = 0
	
try:
	skip_headers = sys.argv[4]
except IndexError:
	skip_headers = 0	

i = open( input_file )
if sys.argv[2] == '-1':
	pass
else:
	o = open( output_file, 'wb' )

reader = csv.reader( i )
if skip_headers:
	headers = reader.next()

trigger = False
for line in reader:
	if label_index == -1:
		label = 1
	else:
		label = line.pop( label_index )
		
	if trigger == False:
		new_line = construct_line( label, line )
	else:	
		new_line = construct_line_string( label, line, class_dict )
	
	if new_line == -9999:
		trigger = True
		class_dict = {}
		
	if sys.argv[2] == '-1':
		print new_line
	else:
		o.write( new_line + '\n' )