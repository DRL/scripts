#!/usr/bin/env python
# coding=utf-8

import sys, os

def read_fasta_to_dict (filename):
	with open(filename) as fh:
		fasta_dict = {}
		contig = ''
		seq = ''
		for line in fh:
		    line = line.rstrip("\n")
		    if line.startswith(">"):
		    	if (contig):
		        	fasta_dict[contig] = seq
		        seq = ''
		        contig = line[1:]
		    else:
		        seq += line
		fasta_dict[contig] = seq
	return fasta_dict
###############################################################################

fasta_dict = read_fasta_to_dict(sys.argv[1])
print fasta_dict

