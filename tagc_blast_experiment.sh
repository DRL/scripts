#! /usr/bin/bash

# take 10% of contigs at random / run 3 times ?
# masked/unmasked
# time
# http://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=ProgSelectionGuide

contig_file = $1 # absolute path
mkdir tagc_blast_experiment
cd tagc_blast_experiment

mkdir blastn
mkdir blastn/megablast/nt
mkdir blastn/megablast/est
mkdir blastn/megablast/env_nt

mkdir blastn/discontiguous_megablast/nt
mkdir blastn/discontiguous_megablast/est
mkdir blastn/discontiguous_megablast/env_nt

mkdir blastn/blastn/nt
mkdir blastn/blastn/est
mkdir blastn/blastn/env_nt

mkdir blastx
mkdir blastx/nr 
mkdir tblastx/

