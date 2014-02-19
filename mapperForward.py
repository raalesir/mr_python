#!/usr/bin/python

import sys
import re
import  hashlib

def read_input(files):
	for line in files:
	        yield line.strip()

sep = sys.argv[1]
if sep == 'space': 
	sep=' '
elif sep == 'none':
	sep=None
mate='.1'
#print 'the sep is', sep

def main(sep):
	list =[]
	# read FASTQ file using python iterators
	lines = read_input(sys.stdin)
	nLines=0;  tmp=100
	while True:
		line = next(lines)
		nLines+=1
		if (line[0] == '@'):	tmp = nLines
		elif (line[0] == '+'):
			if nLines - tmp == 2: break 
	next(lines)
	while True:
		try: 
			line = next(lines)
			line = ''.join(line.split('.'))
			if sep: 
				list.append('@'+ hashlib.sha1(''.join(line.split(sep)[0])).hexdigest()+mate)
			else:
				list.append('@'+hashlib.sha1(line).hexdigest() +mate)
			list.append(next(lines))
			_=next(lines)
			#list.append(next(lines))
			list.append(next(lines))
		except StopIteration: break
		print "%s\t%s\t%s" % (list[0], list[1], list[2])
		list = []

if __name__ == "__main__":
	main(sep)
