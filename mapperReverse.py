#!/usr/bin/python

import sys
import re
def read_input(files):
	for line in files:
	        yield line.strip()

def main():
	list =[]
	# split pattern for FASTQ header
	#pattern=re.compile("[\s+\\,.:=]")
	pattern=re.compile(r"[^a-zA-Z0-9@]+")
	# read FASTQ file using python iterators
	lines = read_input(sys.stdin)
	nLines=0; match = False; headerLocated = False; tmp=0
	for line in lines:
		if not headerLocated: # looking for the header line
			if match: headerLocated=True;
			nLines+=1
			if (line[0] == '@'):	tmp = nLines
			elif (line[0] == '+'):
				if nLines - tmp == 2: match = True; nLines = 0
		else:	
			if (nLines == 1):	list.append(''.join(re.split(pattern,line))+'.2')
			else: list.append(line)
			if nLines > 3: 
			 nLines =1
			 print "%s\t%s %s" % (list[0], list[1], list[3])
			 list = []
			else:
			 nLines += 1

if __name__ == "__main__":
	main()