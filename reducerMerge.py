#!/usr/bin/python

import sys

def read_input(files):
        for line in files:
                yield line.strip()

prevId = None
prevRead = None
lines = read_input(sys.stdin)
for line in lines:
	# the mapper uses tab as the separator between key and value.
	readID,  read = line.strip().split('\t',1)
	if prevId:
		if prevId.split('.')[0] == readID.split('.')[0]:
		#  this effectively prints only pair-ended reads omitting ones without
			print '%s\t%s\t%s' %( prevId, '\t'.join(prevRead.split()), '\t'.join(read.split()) )
		#	print "%s\t%s" %(readID, read)		
			prevId = None
		else:
			prevId = readID
			prevRead = read

	else:
		prevId = readID
		prevRead = read

