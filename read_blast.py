#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import sys, os, argparse

def check_file(infile):
	"""Checks for existence of file."""
	if not os.path.exists(infile):
		sys.exit("The file %s does not exist!"%infile)
	else:
		return infile

def get_input():
	parser = argparse.ArgumentParser(
		prog=sys.argv[0],
		usage = '%(prog)s infile [-e eval_cutoff] [-t target_tax_group] [-c tax_column] [-h]',
		add_help=True)
	parser.add_argument('i', metavar = 'infile', help='Input file (tabular blast output)')
	parser.add_argument('-e', metavar = 'eval_cutoff', default=1e-40, type = float, help='E-value cutoff below which taxonomic disparities count (Default = 1e-40)')
	parser.add_argument('-c', metavar = 'tax_column', default=12, type = int, help='Column in tabular blast input file that holds taxids/tax group names (Default = 12, starting at 0)')
	parser.add_argument('-t', metavar = 'target_tax_group', default='', help='If taxonomic group name or taxid specified the program also reports all hits below E-value cutoff that hit other groups') 

	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)

	args = parser.parse_args()
	input_file = check_file(args.i)
	eval_cutoff = args.e
	tax_column = args.c
	target_tax_group = args.t
	return input_file, eval_cutoff, tax_column, target_tax_group

def print_taxid_disparities (filename, cutoff, tax_column):
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
			current_taxid = temp_list[tax_column]
			current_evalue = temp_list[10]
			current_group = temp_list[13]
			if (current_contig in blast_dict): # if contig not seen for the first time
				if current_query not in blast_dict[current_contig]: # if first HSP
					blast_dict[current_contig][current_query] = (current_taxid, current_evalue, current_group) # add taxid and eval to the dict 
					if float(current_evalue) <= float(eval_cutoff): # if eval below cutoff
						if current_taxid not in tax_dict: # if taxid new
							tax_dict[current_taxid] = current_evalue # add taxid 
			else:
				if (len(tax_dict) > 1):
					print "# " + ordered_contigs[-1]
					for query in sorted(blast_dict[ordered_contigs[-1]]):
						print query + "\t" + blast_dict[ordered_contigs[-1]][query][0] + "\t" + blast_dict[ordered_contigs[-1]][query][1] + "\t" + blast_dict[ordered_contigs[-1]][query][2]
				tax_dict = {}
				blast_dict[current_contig] = {}
				blast_dict[current_contig][current_query] = (current_taxid, current_evalue, current_group)
				if float(current_evalue) <= float(eval_cutoff): # if eval below cutoff
					tax_dict[current_taxid] = current_evalue # add taxid 
				ordered_contigs.append(current_contig)
		if (len(tax_dict) > 1):
			print "# " + ordered_contigs[-1]
			for query in sorted(blast_dict[ordered_contigs[-1]]):
				print query + "\t" + blast_dict[ordered_contigs[-1]][query][0] + "\t" + blast_dict[ordered_contigs[-1]][query][1] + "\t" + blast_dict[ordered_contigs[-1]][query][2]
	return blast_dict

if __name__ == "__main__":
	input_file, eval_cutoff, tax_column, target_tax_group = get_input()
	print_taxid_disparities(input_file, eval_cutoff, tax_column)