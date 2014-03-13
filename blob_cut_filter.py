from __future__ import division
import sys
###############################################################################
contaminants = ["Ascomycota", "Bacteroidetes", "Proteobacteria", "Actinobacteria"];
regions = ['A', 'B', 'C', 'D', 'E']
min_blast_hit_len = 100
max_blast_hit_eval = 1e-50
high_cov = 200
low_cov = 10
high_gc = 0.7
low_gc = 0.0
contig_dict = {}
###############################################################################
def read_blob_to_dict(filename):
	with open(filename) as fh:
		blob_dict = {}
		for line in fh:
			if line.startswith("contig"):
				temp_list = line.rstrip("\n").rsplit("\t")
				contig = temp_list[0]
				blob_info = temp_list[1:]
				if contig not in blob_dict:
					blob_dict[contig] = blob_info
				else:
					print "Warning: Something wrong with " + contig
		return blob_dict

def read_blast_to_dict (filename):
	with open(filename) as fh:
		blast_dict = {}
		for line in fh:
			if line.startswith("contig"):
				temp_list = line.rstrip("\n").rsplit("\t")
				contig = temp_list[0]
				hit = temp_list[1:]
				if (contig in blast_dict):
					pass
				else:
					blast_dict[contig] = hit
	return blast_dict

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
###############################################################################
blast_dict = read_blast_to_dict(sys.argv[1])
blob_dict = read_blob_to_dict(sys.argv[2])
fasta_dict = read_fasta_to_dict(sys.argv[3])
print(str(len(fasta_dict)) + " contigs in file " + sys.argv[3])
###############################################################################
number_of_contigs = len(blob_dict)
number_of_contigs_with_blast_hits = len(blast_dict)
percentage_contigs_with_blast_hits = float(number_of_contigs_with_blast_hits / number_of_contigs)
###############################################################################
# 		cov
# 		^
# 		|	  |	   D	|
#  cov2	+     +---------+
#		|	  |			|
#		|   E |	   A	| C
#		|	  |			|
#  cov1	+     +---------+
#		|	  |	   B	|
#		|-----+---------+----> GC
#			 GC1       GC2
# A = [GC1,	GC2,	Cov1,	Cov2 ]
# B = [GC1, GC2, <= Cov1 ]
# C = [>= GC2]
# D = [GC1, GC2, 	>= Cov2]
# E = [<= GC1]
###############################################################################
region = {'A': {'contigs' : 0 , 'hits' : 0,'good' : 0, 'bad' : 0, 'cum_len' : 0}, 'B': {'contigs' : 0 ,'hits' : 0, 'good' : 0,'bad' : 0, 'cum_len' : 0}, 'C': {'contigs' : 0 ,'hits' : 0 ,'good' : 0, 'bad' : 0, 'cum_len' : 0}, 'D': {'contigs' : 0 ,'hits' : 0 ,'good' : 0, 'bad' : 0, 'cum_len' : 0}, 'E': {'contigs' : 0 ,'hits' : 0 ,'good' : 0, 'bad' : 0, 'cum_len' : 0}}
###############################################################################
outfile_high_cov_fh = open (sys.argv[2] + "_high_cov_contigs.fa", "w")
outfile_included_fh = open (sys.argv[2] + "_included_contigs.fa", "w")
outfile_excluded_fh = open (sys.argv[2] + "_excluded_contigs.fa", "w")
outfile_high_cov_txt_fh = open (sys.argv[2] + "_high_cov_contigs.txt", "w")
outfile_included_txt_fh = open (sys.argv[2] + "_included_contigs.txt", "w")
outfile_excluded_txt_fh = open (sys.argv[2] + "_excluded_contigs.txt", "w")

###############################################################################

# BLOB 0 = length, 1 = GC, 2 = Cov, 3 = sp, 4 = Order, 5 = phylum, 6 = kingdom
# BLAST 1 = hit accession; 3 = len; 10 = eval

for contig in blob_dict:
	#contig_len = int(blob_dict[contig][0])
	contig_gc = float(blob_dict[contig][1])
	contig_cov = float(blob_dict[contig][2])
	contig_phylum = str(blob_dict[contig][5])
	# Area C
	if contig_gc >= high_gc:
		contig_dict[contig] = "C"
	# Area E
	elif contig_gc <= low_gc:
		contig_dict[contig] = "E"
	# Area D, B or A
	else:
		# Area D
		if (contig_cov >= high_cov):
			contig_dict[contig] = "D"
		# Area B
		elif (contig_cov <= low_cov):
			contig_dict[contig] = "B"
		# Area A
		else:
			contig_dict[contig] = "A"

	# Add to number of contigs
	region[contig_dict[contig]]['contigs'] += 1
	# Add to cummulative length
	region[contig_dict[contig]]['cum_len'] += int(blob_dict[contig][0])

	if contig in blast_dict:
	# Annotated contigs
		# hit_phylum = blob[5], hit_len = blast[3], hit_eval = blast[10]
		region[contig_dict[contig]]['hits'] += 1
		if (contig_dict[contig] != "A") and (blob_dict[contig][5] in contaminants) and (int(blast_dict[contig][3]) >= min_blast_hit_len) and (float(blast_dict[contig][10]) <= max_blast_hit_eval):
			# Contaminant contigs
			region[contig_dict[contig]]['bad'] += 1
			outfile_excluded_fh.write(">" + contig + "\n" + fasta_dict[contig] + "\n")
			outfile_excluded_txt_fh.write(contig + "\n")
		elif (contig_dict[contig] == "D"):
			# Annotated non-contaminant high coverage contigs
			outfile_high_cov_fh.write(">" + contig + "\n" + fasta_dict[contig] + "\n")
			outfile_high_cov_txt_fh.write(contig + "\n")
		else:
			# Annotated non-contaminant contigs
			region[contig_dict[contig]]['good'] += 1
			outfile_included_fh.write(">" + contig + "\n" + fasta_dict[contig] + "\n")
			outfile_included_txt_fh.write(contig + "\n")
	# Non-Annotated contigs
	elif (contig_dict[contig] == "D"):
		# high coverage non-annotated contigs
		outfile_high_cov_fh.write(">" + contig + "\n" + fasta_dict[contig] + "\n")
		outfile_high_cov_txt_fh.write(contig + "\n")
	else:
		region[contig_dict[contig]]['good'] += 1
		outfile_included_fh.write(">" + contig + "\n" + fasta_dict[contig] + "\n")
		outfile_included_txt_fh.write(contig + "\n")

total_contigs = 0
total_good = 0
total_bad = 0

print "#"*80
print str(number_of_contigs) + " contigs hitting " + str(number_of_contigs_with_blast_hits) + " sequences in nt => " + str("{0:.2f}".format(percentage_contigs_with_blast_hits*100)) + "%"
print "#"*80
print "Contaminants : " + str(contaminants)
print "Min hit len : " + str(min_blast_hit_len) + "\t Max hit eval : " + str(max_blast_hit_eval)
print "HighCov : " + str(high_cov) + "\t LowCov : " + str(low_cov) + "\t HighGC : " + str(high_gc) + "\t LowGC : " + str(low_gc)
print "#"*80
for i in regions:
	if region[i]['contigs'] == 0:
		print i + ": No contigs found."
	else:
		print i + ": " + str(region[i]['contigs']) + " contigs | cumLen " + str(region[i]['cum_len']) + " nt | AvgLen : " + str("{0:.2f}".format(region[i]['cum_len']/region[i]['contigs'])) + " | Bad : " + str(region[i]['bad']) + " | Hits : " + str(region[i]['hits'])
	total_contigs += region[i]['contigs']
	total_bad += region[i]['bad']
	total_good += region[i]['good']
total_high_cov = total_contigs - total_good - total_bad
print "Total : " + str(total_contigs) + " contigs"
print "#"*80
print "Written ... Good: " + str(total_good) + " (" + str("{0:.2f}".format(total_good*100/total_contigs)) + "%) ... Bad: " + str(total_bad) + " (" + str("{0:.2f}".format(total_bad*100/total_contigs)) + "%) ... HighCov: " + str(total_high_cov) + " (" + str("{0:.2f}".format(total_high_cov*100/total_contigs)) + "%)"
print "#"*80
#print "Contigs included : " + str(len(list_of_included_contigs)) + " (" + str("{0:.2f}".format(len(list_of_included_contigs)/number_of_contigs)) + "%)\t Contigs excluded : " + str(len(list_of_excluded_contigs)) + " (" + str("{0:.2f}".format(len(list_of_excluded_contigs)/number_of_contigs)) + "%)"

outfile_high_cov_fh.close()
outfile_included_fh.close()
outfile_excluded_fh.close()
outfile_high_cov_txt_fh.close()
outfile_included_txt_fh.close()
outfile_excluded_txt_fh.close()
