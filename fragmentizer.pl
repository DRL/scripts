#!/usr/bin/env perl
use strict;
use warnings;
# This creates $fragment_len long fragments of contigs
use Data::Dumper;

my $fragment_len = $ARGV[0];
my $assembly_file = $ARGV[1];

my $header='';
my %hash; 
my @array;

open IN, "<$assembly_file" || die "Can't read\n";

while (my $line = <IN>) {
    if ($line =~ /^>(\S+)\n/) {
        if ($header ne ''){
            push @array, %hash;
        }
    $header = $1;
    $hash{'header'} = $header;
    }   
    else {   
        chomp $line;
        $hash{'seq'}     .= $line;
        $hash{'len'}     += length $line;
    }
}
close IN;

my $out_file = $assembly_file."_".$fragment_len.".fa";

open OUT, ">$out_file" || die "Can't write\n";
foreach my $contig (keys %hash){        
    my $len = int($hash{$contig}{'len'});
    my $limit = $len/$fragment_len;
    my $fragment_header = '';        
    my $subsequence = '';
    for (my $i=1 ; $i < $limit + 1 ;$i++){
        $fragment_header=$contig."_$i";                
        if ($len < $i*$fragment_len) {
            $subsequence = substr($hash{$contig}{'seq'}, ($i-1)*$fragment_len, $fragment_len-($i*$fragment_len-$len ));
        }                
        else{   
            $subsequence = substr($hash{$contig}{'seq'}, ($i-1)*$fragment_len, $fragment_len);
        }                
        print OUT ">".$fragment_header."\n".$subsequence."\n";        
    }
}
close OUT;
