#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File    : mask_blastdb_by_taxid.py
Author  : Dominik R. Laetsch, dominik.laetsch at gmail dot com 
Version : 0.1
"""

import argparse
from Bio import Entrez


if __name__ == "__main__":

	# # # # # # # # # # # # # # # # 
	# COMMAND-LINE ARGUMENT PARSING
	# # # # # # # # # # # # # # # # 

	parser = argparse.ArgumentParser(
		prog='mask_blastdb_by_taxid',
		usage = '%(prog)s -db -type -taxid [-merge] [-h]',
		add_help=True)
	parser.add_argument('-db', metavar = 'blastdb', help='input blastdb')
	parser.add_argument('-type', metavar = 'type', default="n", help='blastdb type ("p" or "n", default: "n")')
	parser.add_argument('-taxids', metavar = 'taxids' , default=[], type = int, nargs='+', help='TaxIDs for which BLASTdbs should be generated') 
	parser.add_argument('-merge', action='store_true' , help='Set flag for merging ') 
	args = parser.parse_args()

	blastdb, blastdb_type, taxids, merge_flag = args.blastdb, args.type, args.taxids, args.merge

	gi_taxid_nucl_dmp = '$BLASTDB/ 
	gi_taxid_prot_dmp = 
	if (taxids):
		for taxid in taxids:
		
	

