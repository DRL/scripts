#!/usr/bin/bash

# masked/unmasked ?
# time ?

contig_file = $1 
out_format = '6 qseqid staxids std sskingdom sscinames sblastnames stitle'

sge_blast blastn -task megablast -query $contig_file -db $BLASTDB/nt -out $contig_file.megablast.out -outfmt $out_format -num_jobs 200 -evalue 1e-5 -max_target_seqs 1 
sge_blast blastn -task dc-megablast -query $contig_file -db $BLASTDB/nt -out $contig_file.dc-megablast.out -outfmt $out_format -num_jobs 200 -evalue 1e-5 -max_target_seqs 1 
sge_blast blastn -task blastn -query $contig_file -db $BLASTDB/nt -out $contig_file.blastn.out -outfmt $out_format -num_jobs 200 -evalue 1e-5 -max_target_seqs 1 

# program that then takes the blast output files and reports for each contig the kingdom and species of best hit and eval, length and gc 
# make a blobplot for each blast
# report number of non annotated, number of nematodes, number of fungi, number of baks contigs, number of others
# PCA ? https://stackoverflow.com/questions/1730600/principal-component-analysis-in-python


