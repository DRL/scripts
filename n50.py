import time
import random
from __future__ import division


# def n50_2(array):
# 	sorted_array=sorted(array)
# 	temp_array = []
# 	for contig_length in sorted_array:
# 		extension = [int(contig_length)] * int(contig_length)
# 		temp_array.extend(extension)
# 	length = len(temp_array)
# 	even = (0 if length % 2 else 1) + 1
# 	half = (length - 1) / 2
# 	return sum(temp_array[half:half + even]) / int(even)

def read_fasta_len_to_list (filename):
	with open(filename) as fh:
		fasta_len_list = []
		contig = ''
		seq = ''
		for line in fh:
		    line = line.rstrip("\n")
		    if line.startswith(">"):
		    	if (contig):
		        	fasta_len_list.append(len(seq))
		        seq = ''
		        contig = line[1:]
		    else:
		        seq += line
		fasta_len_list.append(len(seq))
	return fasta_len_list

def n50(array):
	cum_len = 0
	sorted_array=sorted(array)
	temp_array = []
	for contig_length in sorted_array:
		cum_len += contig_length
		temp_array.append(contig_length)
	teoN50 = cum_len/2.0
	temp_array.reverse()
	testSum = 0
	N50 = 0
	for con in temp_array:
		testSum += con
		if teoN50 < testSum:
			N50 = con
			break
	return N50

filename = sys.argv[1]
fasta_len_list = read_fasta_len_to_list(filename)
start = time.time()
print n50(fasta_len_list)
end = time.time()
elapsed = end - start
print filename + " : Time taken ", elapsed, "seconds."
#start = time.time()
#print n50_2(random_list)
#end = time.time()
#elapsed = end - start
#print "Time taken: ", elapsed, "seconds."