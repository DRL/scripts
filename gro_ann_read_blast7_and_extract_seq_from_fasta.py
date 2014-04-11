#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def read_blast_7_to_dict (filename):
    with open(filename) as fh:
        blast_dict = {}
        query = ''
        subject = ''
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith(">"):
                scaffold = line.lstrip(">")
                fasta_dict[scaffold] = seq
            else:
                fasta_dict[scaffold] += seq
        fasta_dict[scaffold] = seq
    return fasta_dict

fasta_dict = fasta_to_dict(sys.argv[1])

for scaffold in fasta_dict:
    print scaffold + "\t" + str(len(fasta_dict[scaffold]))  


