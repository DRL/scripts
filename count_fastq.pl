#! /usr/bin/env perl

my $i = 0;
my $seq_count = 0;
my $base_count = 0;
while (<STDIN>){
	$i++;
	if ($i == 4){
		$i = 0;
	}
	if ($i == 1){
		$seq_count++;
	}
	if ($i == 2){
		chomp;
		$base_count += length();
	}
}
print $seq_count."\n";
print $base_count."\n";