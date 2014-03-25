#!/usr/bin/env python
from __future__ import division
import sys

def read_table_to_dict (filename):
	with open(filename) as fh:
		table_dict = {}
		contig = ''
		rest = ''
		for line in fh:
			line = line.rstrip("\n")
			if line.startswith("contig"):
				field = line.split("\t")
				table_dict{field[0]}=field[1:] 

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

table_dict = read_table_to_dict(sys.argv[1])
fasta_dict = read_fasta_to_dict(sys.argv[2])

for contig in table_dict:
	print contig

