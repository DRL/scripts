#!/usr/bin/env perl

use warnings;
use strict;
use Data::Dumper;

my $current_parent='';
my $current_end='';
my @array;
my $exon_count = 0;

print "##gff-version 3\n";
while (<>){
	chomp;
	my $line = $_;
	my @line_array = split (/\s+/, $line);
	if ($line_array[2] eq 'Internal'){
	 	next;
	}	
	if ($line_array[2] eq 'First'){
		if(@array){
			if ($array[0][6] eq "+"){
				$array[0][4] = $array[-1][4];
			}
			else{
				$array[0][3] = $array[-1][3];
				$array[0][4] = $array[1][4];	
			}
			for my $i (0 .. $#array){
				my @print_array = @{$array[$i]};
				my $print_line = join "\t", @print_array;
				print $print_line;
			}
			@array=();
			$current_parent ='';
			$exon_count = 0;
		}		
		$current_parent = $line_array[0]."-".$line_array[8];
  		$line_array[2] = "match";
  		$line_array[8] = "ID=".$line_array[0]."-".$line_array[8].";Name=".$line_array[8]."\n";
  		push @array, [@line_array];
	}
	if ($line_array[2] eq 'Exon'){
	 	$exon_count++;
	 	$current_end = $line_array[4];
	 	$line_array[2] = "match_part";
	 	$line_array[8] = "ID=".$line_array[0]."-".$line_array[8]."-".$exon_count.";Parent=".$current_parent.";Name=".$line_array[8]."-".$exon_count."\n";
	 	push @array, [@line_array];
	}		
}

$array[0][4] = $current_end;
for my $i (0 .. $#array){
	my @print_array = @{$array[$i]};
	my $print_line = join "\t", @print_array;
	print $print_line;
}
