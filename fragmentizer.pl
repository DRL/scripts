#!/usr/bin/env perl
use strict;
use warnings;

# This creates $fragment_len long fragments of contigs
use Data::Dumper;
my $fragment_len  = $ARGV[0];
my $len_threshold = $ARGV[1];
my $assembly_file = $ARGV[2];
open IN, "<$assembly_file" || die "Can't read\n";

my $header = '';
my $seq    = '';
my $len    = 0;
my %hash;
my @array;

while ( my $line = <IN> ) {
    if ( $line =~ /^>(\S+)\n/ ) {
        if ( $header ne '' ) {
            push @array,
                { 'header' => $header, 'seq' => $seq, 'len' => $len };
        }
        $header = $1;
        $seq    = '';
        $len    = 0;
    }
    else {
        chomp $line;
        $seq .= $line;
        $len += length $line;
    }
}
push @array, { 'header' => $header, 'seq' => $seq, 'len' => $len };
close IN;
my $out_file = $assembly_file . "_" . $fragment_len . ".fa";

# command line args and usage

open OUT, ">$out_file" || die "Can't write\n";
for my $i ( 0 .. $#array ) {
    my $header       = $array[$i]{'header'};
    print $header;
    my $seq          = $array[$i]{'seq'};
    my $len          = $array[$i]{'len'};
    my $modulo       = $len % $fragment_len;
    my $limit        = ( $len - $modulo ) / $fragment_len;
    my @subsequences = ( $seq =~ /(.{1,$fragment_len})/g );
    if ( $limit == 0 ) {
        print OUT ">" . $header . "_1\n" . $subsequences[0] . "\n";
        next;
    }
    if ( ( $modulo / $fragment_len ) <= $len_threshold ) {
        $subsequences[-2] .= pop @subsequences;
    }
    for my $j ( 0 .. $#subsequences ) {
        print OUT ">"
            . $header . "_"
            . ( $j + 1 ) . "\n"
            . $subsequences[$j] . "\n";
    }
}
close OUT;
print $fragment_len. "\n";
