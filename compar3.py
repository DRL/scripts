#!/usr/bin/env python
# coding=utf-8

# File   : compar3.py
# Author : Dominik R. Laetsch, dominik.laetsch at gmail dot com 

# # # # # 
# MODULES										
# # # # # 

from __future__ import division
import sys 

def read_fasta_to_dict (filename):
	with open(filename) as fh:
		fasta_dict = {}
		contig = ''
		seq = ''
		for line in fh:
		    line = line.rstrip("\n")
		    if line.startswith(">"):
		        fasta_dict[contig] = seq
		        seq = ''
		        contig = line[1:]
		    else:
		        seq += line
		fasta_dict[contig] = seq
	return fasta_dict

def read_blast_to_dict (filename):
	with open(filename) as fh:
		blast_dict = {}
		for line in fh:
			temp_list = line.rstrip("\n").rsplit("\t")
			contig = temp_list[0]
			hit = temp_list[2]
			if (contig in blast_dict):
				pass
			else:
				blast_dict[contig] = hit
	return blast_dict

if __name__ == "__main__":
	file_A = sys.argv[1]
	file_B = sys.argv[2]
	file_C = sys.argv[3]
	fasta_A = read_fasta_to_dict(file_A)
	fasta_B = read_fasta_to_dict(file_B)
	fasta_C = read_fasta_to_dict(file_C)
	blast_A_to_B = read_blast_to_dict(sys.argv[4])
	blast_B_to_A = read_blast_to_dict(sys.argv[5])
	blast_A_to_C = read_blast_to_dict(sys.argv[6])
	blast_C_to_A = read_blast_to_dict(sys.argv[7])
	blast_B_to_C = read_blast_to_dict(sys.argv[8])
	blast_C_to_B = read_blast_to_dict(sys.argv[9])

	count_A = len(fasta_A) # Number of sequences in A
	count_B = len(fasta_B) # Number of sequences in B
	count_C = len(fasta_C) # Number of sequences in C

	A_hitting_B = len(blast_A_to_B) # Number of sequences in A hitting B
	B_hitting_A = len(blast_B_to_A) # Number of sequences in B hitting A
	A_hitting_C = len(blast_A_to_C) # Number of sequences in A hitting C
	C_hitting_A = len(blast_C_to_A) # Number of sequences in C hitting A
	B_hitting_C = len(blast_B_to_C) # Number of sequences in B hitting C
	C_hitting_B = len(blast_C_to_B) # Number of sequences in C hitting B

	print "A_hitting_B " + str(A_hitting_B)
	print "B_hitting_A " + str(B_hitting_A)
	print "A_hitting_C " + str(A_hitting_C)
	print "C_hitting_A " + str(C_hitting_A)
	print "B_hitting_C " + str(B_hitting_C)
	print "C_hitting_B " + str(C_hitting_B)

	# Make files containing sequences that:
	# - All sequences in A that hit B and C : Gpal in rsem and no_rsem
	# - All sequences in A that hit B  		: Gpal only in rsem
	# - All sequences in A that hit C       : Gpal only in no_rsem
	# - All sequences in A alone
	# - All sequences in B that hit A and C : rsem in Gpal and no_rsem
	# - All sequences in B that hit A   	: rsem only in Gpal
	# - All sequences in B that hit C   	: rsem only in no_rsem
	# - All sequences in B alone
	# - All sequences in C that hit A and B : no_rsem in Gpal and rsem
	# - All sequences in C that hit A       : no_rsem in Gpal
	# - All sequences in C that hit B 		: no_rsem in rsem
	# - All sequences in C alone

	A_BC = open ("set_" + file_A + "_" + file_B + "_" + file_C + ".fa", "w")
	A_B = open ("set_" + file_A + "_" + file_B + ".fa", "w")
	A_C = open ("set_" + file_A + "_" + file_C + ".fa", "w")
	A_ = open ("set_" + file_A + ".fa", "w")
	B_AC = open ("set_" + file_B +"_" + file_A +"_" + file_C + ".fa", "w")
	B_A = open ("set_" + file_B + "_" +file_A + ".fa", "w")
	B_C = open ("set_" + file_B +"_" + file_C + ".fa", "w")
	B_ = open ("set_" + file_B + ".fa", "w")
	C_AB = open ("set_" + file_C +"_" + file_A + "_" +file_B + ".fa", "w")
	C_A = open ("set_" + file_C +"_" + file_A + ".fa", "w")
	C_B = open ("set_" + file_C +"_" + file_B + ".fa", "w")
	C_ = open ("set_" + file_C + ".fa", "w")

	for read in fasta_A:
		if (read in blast_A_to_B) and (read in blast_A_to_C):
			A_BC.write(">" + read + "\n" + fasta_A[read] + "\n")
		elif(read in blast_A_to_B):
			A_B.write(">" + read + "\n" + fasta_A[read] + "\n")
		elif(read in blast_A_to_C):
			A_C.write(">" + read + "\n" + fasta_A[read] + "\n")	
		else:
			A_.write(">" + read + "\n" + fasta_A[read] + "\n")	
	for read in fasta_B:
		if (read in blast_B_to_A) and (read in blast_B_to_C):
			B_AC.write(">" + read + "\n" + fasta_B[read] + "\n")
		elif(read in blast_B_to_A):
			B_A.write(">" + read + "\n" + fasta_B[read] + "\n")
		elif(read in blast_B_to_C):
			B_C.write(">" + read + "\n" + fasta_B[read] + "\n")	
		else:
			B_.write(">" + read + "\n" + fasta_B[read] + "\n")	
	for read in fasta_C:
		if (read in blast_C_to_A) and (read in blast_C_to_B):
			C_AB.write(">" + read + "\n" + fasta_C[read] + "\n")
		elif(read in blast_C_to_A):
			C_A.write(">" + read + "\n" + fasta_C[read] + "\n")
		elif(read in blast_C_to_B):
			C_B.write(">" + read + "\n" + fasta_C[read] + "\n")	
		else:
			C_.write(">" + read + "\n" + fasta_C[read] + "\n")	
