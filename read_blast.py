#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import sys 

def read_blast_to_dict (filename):
	with open(filename) as fh:
		blast_dict = {}
		tax_dict = {}
		taxid_disparity = 0
		ordered_contigs = []
		for line in fh:
			temp_list = line.rstrip("\n").rsplit("\t")
			current_query = temp_list[0] # Subsequence ID
			current_contig = current_query.rsplit('_',1)[0]
			current_subseq = current_query.rsplit('_',1)[1]
			current_taxid = temp_list[1]
			current_evalue = temp_list[11] 
			if (current_contig in blast_dict):
				blast_dict[current_contig][current_query] = (current_taxid, current_evalue)
				if current_taxid not in tax_dict:
					taxid_disparity = 1
			else:
				if (taxid_disparity):
					print "# " + ordered_contigs[-1]
					for query in sorted(blast_dict[ordered_contigs[-1]]):
						print query + "\t" + blast_dict[ordered_contigs[-1]][query][0] + "\t" + blast_dict[ordered_contigs[-1]][query][1]
				taxid_disparity = 0
				tax_dict = {}
				blast_dict[current_contig] = {}
				blast_dict[current_contig][current_query] = (current_taxid, current_evalue)
				tax_dict[current_taxid] = 1
				ordered_contigs.append(current_contig)
		if (taxid_disparity):
			print "# " + ordered_contigs[-1]
			for query in sorted(blast_dict[ordered_contigs[-1]]):
				print query + "\t" + blast_dict[ordered_contigs[-1]][query][0] + "\t" + blast_dict[ordered_contigs[-1]][query][1]
	return blast_dict

if __name__ == "__main__":
	blast_file = sys.argv[1]
	blast_dict = read_blast_to_dict(blast_file)