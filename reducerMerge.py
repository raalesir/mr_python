#!/usr/bin/python

import sys

prevId = None
prevRead = None
for line in sys.stdin:
	# the mapper uses tab as the separator between key and value.
	readID,  read = line.strip().split('\t',1)
	if prevId:
		if prevId.split('.')[0] == readID.split('.')[0]:
#  this effectively prints only pair-ended reads omitting ones without
			print '%s\t%s\t%s' %( prevId, '\t'.join(prevRead.split()), '\t'.join(read.split()) )
			prevId = None
		else:
			prevId = readID
			prevRead = read

	else:
		prevId = readID
		prevRead = read

