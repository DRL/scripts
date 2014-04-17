#!/usr/bin/env perl

use warning;
use strict;

my @current_obj;

while (<>){
	chomp;
	my $line = $_;
	my @line_array = split /\t/, $line;
	my @note_array = split /;/, $line[8];
	my $exon_count = 0;
	if ($line_array[2] eq 'Internal'){
		next;
	}	
	if ($line_array[2] eq 'First'){		
 		$line_array[2] = "match";
 		$line_array[8] = $note_array[0]."-".substr($note_array[1], 5).";".$note_array[1]."\n";
 		print $line;
 		push @current_obj, @line_array;
	}
	if ($line_array[2] eq 'Exon'){
		$exon_count++;
		#$line_array[2] = "match_part";
		#$line_array[8] = $note_array[0]."-".$exon_count.";Parent=".$current_obj[0][";"$note_array[1];
	}		
}