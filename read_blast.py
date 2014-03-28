#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import sys 

def read_blast_to_dict (filename):
	with open(filename) as fh:
		blast_dict = {}
		taxid_disparity = 0
		ordered_contigs = []
		for line in fh:
			temp_list = line.rstrip("\n").rsplit("\t")
			current_query = temp_list[0] # Subsequence ID
			current_contig = current_query.rsplit('_',1)[0]
			current_subseq = current_query.rsplit('_',1)[1]
			current_taxid = temp_list[1]
			current_evalue = temp_list[11] 
			print current_query + "\t" + current_contig + "\t" + current_subseq + "\t" + current_taxid + "\t" + current_evalue + "\n"
			if (current_contig in blast_dict and current_query not in blast_dict[current_contig]): # if neither first sequence nor multiple hsps
				for query in blast_dict[current_contig]:
					last_taxid = blast_dict[current_contig][query].keys()[0]
					if current_taxid != last_taxid:
						print current_taxid + " != " + last_taxid
						taxid_disparity = 1
				blast_dict[current_contig][current_query] = { }
				blast_dict[current_contig][current_query][current_taxid] = current_evalue
			else:
				blast_dict[current_contig] = { }
				blast_dict[current_contig][current_query] = { }
				blast_dict[current_contig][current_query][current_taxid] = current_evalue
				ordered_contigs.append(current_contig)
				print blast_dict
				if taxid_disparity == 1:
					print blast_dict
					last_contig = ordered_contigs[-1]
					print "last : " + last_contig
					for subseq in blast_dict[last_contig]: 
						for taxid in blast_dict[last_contig][subseq]:
							evalue = blast_dict[last_contig][subseq][taxid]
							print subseq + "\t" + taxid + "\t" + evalue + "\n"
				taxid_disparity = 0
	return blast_dict

if __name__ == "__main__":
	blast_file = sys.argv[1]
	blast_dict = read_blast_to_dict(blast_file)