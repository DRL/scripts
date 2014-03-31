#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import sys 

def print_taxid_disparities (filename, cutoff):
	eval_cutoff = cutoff
	with open(filename) as fh:
		blast_dict = {} 
		tax_dict = {} # only taxids for which a hit with an eval below the cutoff get added
		ordered_contigs = [] # this is for keeping track of the order and getting the last contig for printing
		for line in fh:
			temp_list = line.rstrip("\n").rsplit("\t")
			current_query = temp_list[0] # Subsequence ID
			current_contig = current_query.rsplit('_',1)[0]
			current_subseq = current_query.rsplit('_',1)[1]
			current_taxid = temp_list[1]
			current_evalue = temp_list[11]
			if (current_contig in blast_dict): # if contig not seen for the first time
				if current_query not in blast_dict[current_contig]: # if first HSP
					blast_dict[current_contig][current_query] = (current_taxid, current_evalue) # add taxid and eval to the dict 
					if float(current_evalue) <= float(eval_cutoff): # if eval below cutoff
						if current_taxid not in tax_dict: # if taxid new
							tax_dict[current_taxid] = current_evalue # add taxid 
			else:
				if (len(tax_dict) > 1):
					print "# " + ordered_contigs[-1]
					for query in sorted(blast_dict[ordered_contigs[-1]]):
						print query + "\t" + blast_dict[ordered_contigs[-1]][query][0] + "\t" + blast_dict[ordered_contigs[-1]][query][1]
				tax_dict = {}
				blast_dict[current_contig] = {}
				blast_dict[current_contig][current_query] = (current_taxid, current_evalue)
				if float(current_evalue) <= float(eval_cutoff): # if eval below cutoff
					tax_dict[current_taxid] = current_evalue # add taxid 
				ordered_contigs.append(current_contig)
		if (len(tax_dict) > 1):
			print "# " + ordered_contigs[-1]
			for query in sorted(blast_dict[ordered_contigs[-1]]):
				print query + "\t" + blast_dict[ordered_contigs[-1]][query][0] + "\t" + blast_dict[ordered_contigs[-1]][query][1]
	return blast_dict

if __name__ == "__main__":
	blast_file = sys.argv[1]
	if (len(sys.argv) >= 3):
		eval_cutoff = sys.argv[2]
	else:
		eval_cutoff = "1"
	print_taxid_disparities(blast_file, eval_cutoff)