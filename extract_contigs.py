#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import sys

def read_table_to_dict (filename):
	with open(filename) as fh:
		table_dict = {}
		for line in fh:
			line = line.rstrip("\n")
			field = line.split("\t")
			key = field[0]
			table_dict[key] = "_" + field[4] + "_" + field[5] + "_" + field[6] + "_" + field[7] + "_"
	return table_dict

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
suffix = sys.argv[2][0:-19]

for name in table_dict:
	search = name + "_" + suffix
	if search in fasta_dict:
		print ">" + search + table_dict[name] + "\n" + fasta_dict[search] 


