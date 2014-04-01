#!/usr/bin/env perl
use strict;
use warnings;
use Getopt::Long qw(:config pass_through no_ignore_case);
use Data::Dumper;

my ( $scaffold_file, $number_of_n, $verbose );

GetOptions(
    "file=s"  => \$scaffold_file,
    "n=i"     => \$number_of_n,
    "verbose" => \$verbose
);
$number_of_n = (10) unless $number_of_n;

die <<USAGE
Usage: splitN.pl -f scaffold_file.fa [-n]
-f Scaffold file to be split at N's
-n Minimum number of N's at which to split (default = 10)
-v verbose
USAGE
    unless ($scaffold_file);

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

open IN, "<$scaffold_file" || die "Can't read\n";

my $header = '';
my $seq    = '';

while ( my $line = <IN> ) {
    if ( $line =~ /^>(\S+)\n/ ) {
        if ( $header ne '' ) {
            &print_contigs_of_scaffold( $header, $seq, $number_of_n );
        }
        $header = $1;
        $seq    = '';
    }
    else {
        chomp $line;
        $seq .= $line;
    }
}
&print_contigs_of_scaffold( $header, $seq, $number_of_n );
close IN;

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

sub print_contigs_of_scaffold {
    my $header      = shift @_;
    my $seq         = shift @_;
    my $number_of_n = shift @_;
    my @temp_array  = split( /N{$number_of_n,}/, $seq );
    for my $i ( 0 .. $#temp_array ) {
        print ">"
            . $header
            . "_contig_"
            . ( $i + 1 ) . "_of_"
            . ( $#temp_array + 1 ) . "\n"
            . $temp_array[$i] . "\n";
    }
}

