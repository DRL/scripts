#!/usr/bin/env perl
use strict;
use warnings;
use Getopt::Long qw(:config pass_through no_ignore_case);
# This creates $fragment_len long fragments of contigs
use Data::Dumper;

my $fragment_len ;
my $len_threshold ;
my $assembly_file = $ARGV[0];

open IN, "<$assembly_file" || die "Can't read\n";

my $header = '';
my $seq    = '';
my %hash;
my @array;
my $seq_count = 0;
my $n_count = 0; 
my $n_total = 0;
my $n_nucs = 0;
my $total_len = 0;
my $nuc_len = 0;
my $gc_count = 0;
my $gc_total = 0;
my $gc_nucs = 0;
print "# header\ttotal_len\tnuc_len\tn_count\tn_total\tn_nucs\tgc_count\tgc_total\tgc_nucs\n";
while ( my $line = <IN> ) {
    if ( $line =~ /^>(\S+)\n/ ) {
        if ( $header ne '' ) {
            #$seq =~ s/N{11,}/NNNNNNNNNN/g; # replace ocurrence of more than 10 N's with 10 N's
            $n_count = &count_N($seq);
            $total_len = length($seq);
            $nuc_len = $total_len - $n_count;
            if ($n_count != 0){
                $n_total = sprintf("%.2f", $n_count/$total_len);
                $n_nucs = sprintf("%.2f", $n_count/$nuc_len);    
            }
            else{
                $n_total = 0.00;
                $n_nucs = 0.00 ;  
            }
            $gc_count = &count_GC($seq);
            $gc_total = sprintf("%.2f", $gc_count/$total_len);
            $gc_nucs = sprintf("%.2f", $gc_count/$nuc_len);
            print  $header . "\t". $total_len . "\t". $nuc_len . "\t". $n_count . "\t". $n_total . "\t". $n_nucs . "\t". $gc_count . "\t". $gc_total . "\t". $gc_nucs ."\n";
        }
        $header = $1;
        $seq    = '';
        $seq_count++;
    }
    else {
        chomp $line;
        $seq .= $line;
    }
}
$n_count = &count_N($seq);
$total_len = length($seq);
$nuc_len = $total_len - $n_count;
$gc_count = &count_GC($seq);
$gc_total = sprintf("%.2f", $gc_count/$total_len);
$gc_nucs = sprintf("%.2f", $gc_count/$nuc_len);
print  $header . "\t". $total_len . "\t". $nuc_len . "\t". $n_count . "\t". $n_total . "\t". $n_nucs . "\t". $gc_count . "\t". $gc_total . "\t". $gc_nucs ."\n";
close IN;

sub count_N(){
    my $seq = shift; 
    my $n_count = $seq =~ tr/N//; # fastest way to count something in perl 
    return $n_count;
}

sub count_GC(){
    my $seq = shift;
    my $gc_count = $seq =~ tr/G|C//;
    return $gc_count;
}