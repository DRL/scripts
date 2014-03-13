#!/usr/bin/perl
use strict;
use warnings;
use Data::Dumper;

my $bam_file         = $ARGV[0];
my $bad_contigs      = $ARGV[1];
my $high_cov_contigs = $ARGV[2];

my $number_of_reads          = 0;
my $number_of_good_reads     = 0;
my $number_of_bad_reads      = 0;
my $number_of_high_cov_reads = 0;

sub revcom_with_flag{
    my $seq = $_[0];
    my $flag = $_[1];
    if ($flag & 16) {
        $seq = reverse $seq;
        $seq =~tr/AGCT/TCGA/;
    }
    return $seq;
}
sub read_contig_file {
    my %contigs;
    open( CONTIG_FILE, "<" . $_[0] )
        || die "Reading $_[0] : No no !\n";
    while ( my $contig_line = <CONTIG_FILE> ) {
        chomp($contig_line);
        if ( $contig_line =~ m/contig_/i ) {
            $contigs{ $contig_line . "/" } = 0;
        }
    }
    return %contigs;
}
my %bad_contigs      = &read_contig_file($bad_contigs);
my %high_cov_contigs = &read_contig_file($high_cov_contigs);

open( GOOD, ">" . $bam_file . "_plus_reads_mapping_good_contigs.txt" )
    || die "Writing $bam_file.good_contigs_reads_mapping.txt : No no !\n";
open( BAD, ">" . $bam_file . "_plus_reads_mapping_bad_contigs.txt" )
    || die "Writing $bad_contigs._reads_mapping.txt : No no !\n";
open( HIGHCOV, ">" . $bam_file . "_plus_reads_mapping_high_cov_contigs.txt" )
    || die "Writing $high_cov_contigs._reads_mapping.txt : No no !\n";

open BAM_FILE, "samtools view $bam_file | " or die $!;

my @array;
# @array : pair, read1, contig1, bam_flag1, seq1, read2, contig2, bam_flag2, seq2

while ( my $bam_line = <BAM_FILE> ) {
    if ( $number_of_reads > 0 && $number_of_reads % 1000000 == 0 ) {
        print "Total: "
            . $number_of_reads
            . "\tGood: "
            . $number_of_good_reads . " ("
            . sprintf( '%.2f%%',
            100 * $number_of_good_reads / $number_of_reads )
            . ")\tBad: "
            . $number_of_bad_reads . " ("
            . sprintf( '%.2f%%',
            100 * $number_of_bad_reads / $number_of_reads )
            . ")\tHighCov: "
            . $number_of_high_cov_reads . " ("
            . sprintf( '%.2f%%',
            100 * $number_of_high_cov_reads / $number_of_reads )
            . ")\n";
    }
    next unless ( $bam_line =~ m/^ERR/ );
    $number_of_reads++;
    my @bam_fields = split /\t/, $bam_line;
    ###########
    my $read   = $bam_fields[0];
    # my $pair   = substr $read, 0, -1; # for when \1 \2
    my $pair   = $read;	
    my $bam_flag = $bam_fields[1];
    my $seq = $bam_fields[9];
    my $contig = $bam_fields[2];
    #if ( $read =~ m/1$/ ) { # when \1 \2
    if ( $read =~m/^ERR/ ) {
        push @array, $pair;
        push @array, $read;
        push @array, $contig;
        push @array, $seq;
        push @array, $bam_flag;
    }
    #elsif ( $read =~ m/2$/ ) { when \1 \2
    #    push @array, $pair;
    #    push @array, $read;
    #    push @array, $contig;
    #    push @array, $seq;
    #    push @array, $bam_flag;
    #}
    else {
        print "Warning: $bam_fields[0]\n";
    }
    if ( scalar(@array) >= 10 ) {
        # print Dumper(\@array); #DEBUGGIN site
        # @array : pair, read1, contig1, bam_flag1, seq1, read2, contig2, bam_flag2, seq2
        my $fasta = ">".$array[1]."\n".&revcom_with_flag($array[3], $array[4])."\n>".$array[6]."\n".&revcom_with_flag($array[8], $array[9])."\n";
        if (   exists( $bad_contigs{ $array[2] . "/" } )
            && exists( $bad_contigs{ $array[7] . "/" } ) )
        {
            # Both contigs are contaminants
            $number_of_bad_reads += 2;
            #$bad_contigs{ $array[2] . "/" } = 1;
            #$bad_contigs{ $array[4] . "/" } = 1;
            print BAD $fasta;
            @array = ();
        }
        elsif (exists( $high_cov_contigs{ $array[2] . "/" } )
            && exists( $high_cov_contigs{ $array[7] . "/" } ) )
        {
            # Both contigs are high coverage
            $number_of_high_cov_reads += 2;
            #$high_cov_contigs{ $array[2] . "/" } = 1;
            #$high_cov_contigs{ $array[4] . "/" } = 1;
            print HIGHCOV $fasta;
            @array = ();
        }
        else {
            $number_of_good_reads += 2;
            print GOOD $fasta;
            @array = ();
        }
    }
}
close BAM_FILE;
close GOOD;
close BAD;
close HIGHCOV;

open( LOG, ">" . $bam_file . "_plus_log.txt" )
    || die "Writing " . $bam_file . "_plus_log.txt : No no !\n";
print LOG "Total: "
    . $number_of_reads
    . "\tGood: "
    . $number_of_good_reads . " ("
    . sprintf( '%.2f%%', 100 * $number_of_good_reads / $number_of_reads )
    . ")\tBad: "
    . $number_of_bad_reads . " ("
    . sprintf( '%.2f%%', 100 * $number_of_bad_reads / $number_of_reads )
    . ")\tHighCov: "
    . $number_of_high_cov_reads . " ("
    . sprintf( '%.2f%%', 100 * $number_of_high_cov_reads / $number_of_reads )
    . ")\n";
close LOG;