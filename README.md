INTRO
-------------
These three scripts below, written in Python, are to substitute the Perl script for the preprocessing stage of the Crossbow.
Provided Python scripts are in the MR-style, meaning that they are being executed in a massive parallel fashion, compare to the poorly parallel  Perl script of the Crossbow.
The price for being massively parallel is the requirement of the FASTQ data being:

1) BZIP2 archived, since bzip2 provides  a splittable archive format

2) the FASTQ data have to be accessible by the Hadoop via i.e. sshfs of similar.

mapperForward.py
---------------

reads the FASTQ chunk on each Hadoop datanode, locates the header line, and transforms 4 line format the a singular line format, consisting of the 1st, 2-nd and 4-th lines in the FASTQ block.
The transformed FASTQ header contains just alphanumerics + "@" sign. To the end the ".1" is added in order to be able to identify this read in the following code.

mapperReverse.py
----------------
does exactly the  same, adding the ".2" instead.


mapperMerge.py
-----------------

creates the Crossbow formatted file i.e. each line for the pair-ended read consists of 5 fields, namely

1) read ID 
2) forward read 
3) forward qualities 
4) reverse reads 
5) reverse qualities


COMMENTS
-------------
In fact there is no a real standard in the FASTQ header format: it changes constantly: http://en.wikipedia.org/wiki/FASTQ_format
The only things one can rely on in that the header is unique in the whole FASTQ file.
To distinguish the reads in a pair is not so obvious. The reason is the following:
all the files BUT converted from SRA format have "1" for forward, and "2" for the reverse reads, making the task to distinct them an easy one.
The SRA->FASTQ transformation with SRA-toolkit created IDENTICAL headers for the both reads in a pair.
The latter means that the only way to distinguish the members of a pair is to proceed then in a different Hadoop jobs, using the mapperForward.py and the mapperReverse.py scripts, as these scripts add  ".1" and ".2" correspondingly to  the end of the  headers. 
The ".1" and ".2" are being engaged in the reducerMerge.py.

Example:
------------
SRA-->FASTQ converted reads. (note the identical headers)

Forward: 

@SRR611085.1 FCD0R1VACXX:4:1101:1589:2132 length=100 
ATGACAACTAGAACCATAACCGGATCTTAAAAACCTAAGTATTGANNNTTTGTTAGAAGATACAAAGACAAAGACTCATACGGACTTCGACTACACTATC 
+SRR611085.1 FCD0R1VACXX:4:1101:1589:2132 length=100 
\_bbceeeegggggh\feggeefhffcegiiihiheffgbIXacfgBBBLLaeeghhfgf\bdggbgegac_Zaddddcdcca^^acbbacaaX\`\`\`Y\`\_b 

Reverse:

@SRR611085.1 FCD0R1VACXX:4:1101:1589:2132 length=100 
TTCTTGCTTCTAAAAGCTTTGATGGTTTAGCCGAATTCCGTATGAGAATTTGTCTATGTATCTTCTAACAAGGATACAATATTTAGGCTTTTAAGATCCG 
+SRR611085.1 FCD0R1VACXX:4:1101:1589:2132 length=100 
bbbeeeeegggfgiiiiiiii]ghhggigff`gfhiihhiaafhffafg]effhfhfhghiiihhiihiihhhg[dgegggeeeeeecddddbbcccccc 


This pair after mapperForward.py and the mapperReverse.py:

@SRR6110851FCD0R1VACXX4110115892132length100.1  ATGACAACTAGAACCATAACCGGATCTTAAAAACCTAAGTATTGANNNTTTGTTAGAAGATACAAAGACAAAGACTCATACGGACTTCGACTACACTATC 
\_bbceeeegggggh\feggeefhffcegiiihiheffgbIXacfgBBBLLaeeghhfgf\bdggbgegac_Zaddddcdcca^^acbbacaaX\`\`\`Y\`\_b 

and 

@SRR6110851FCD0R1VACXX4110115892132length100.2  
TTCTTGCTTCTAAAAGCTTTGATGGTTTAGCCGAATTCCGTATGAGAATTTGTCTATGTATCTTCTAACAAGGATACAATATTTAGGCTTTTAAGATCCG 
bbbeeeeegggfgiiiiiiii]ghhggigff`gfhiihhiaafhffafg]effhfhfhghiiihhiihiihhhg[dgegggeeeeeecddddbbcccccc

After the reducerMerge.py

@SRR6110851FCD0R1VACXX4110115892132length100.1  ATGACAACTAGAACCATAACCGGATCTTAAAAACCTAAGTATTGANNNTTTGTTAGAAGATACAAAGACAAAGACTCATACGGACTTCGACTACACTATC 
\_bbceeeegggggh\feggeefhffcegiiihiheffgbIXacfgBBBLLaeeghhfgf\bdggbgegac_Zaddddcdcca^^acbbacaaX\`\`\`Y\`\_b 
TTCTTGCTTCTAAAAGCTTTGATGGTTTAGCCGAATTCCGTATGAGAATTTGTCTATGTATCTTCTAACAAGGATACAATATTTAGGCTTTTAAGATCCG     
bbbeeeeegggfgiiiiiiii]ghhggigff`gfhiihhiaafhffafg]effhfhfhghiiihhiihiihhhg[dgegggeeeeeecddddbbcccccc

