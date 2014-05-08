#!/usr/bin/perl
use strict;
use warnings;
use Data::Dumper;

my @data;
my ($count, $min, $max, $sum,$sqsum, $mean, $median, $stdev);

while(<>){
	chomp $_;
	push @data, $_;
}
my @sorted_data= sort {$a <=> $b} @data;

$count = scalar(@sorted_data);
if ($count%2==1){ # Uneven
	$median=sprintf("%3.2f",$sorted_data[$count/2]);
}
else{
	$median=sprintf("%3.2f",($sorted_data[$count/2]+$sorted_data[$count/2+1])/2);
}
$sum += $_ for @sorted_data;
$sqsum+=$_*$_ for @sorted_data;
$mean = sprintf("%3.2f", $sum/$count);
$stdev = sprintf("%3.2f", sqrt(($sqsum-$mean*$mean*$count)/($count-1)));
$min = $sorted_data[0];
$max = $sorted_data[-1];

print "Count\t: $count\n";
print "Mean\t: $mean\n";
print "Median\t: $median\n";
print "Min\t: $min\n";
print "Max\t: $max\n";
print "sd\t: $stdev\n";
