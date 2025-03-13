#!/usr/bin/perl
use strict;
use warnings;

if (@ARGV != 2) {
    die "Usage: $0 <family_file> <tblout_file>\n";
}

my ($family_file, $tblout_file) = @ARGV;

# 从family文件中读取rfam_id和family信息
my %rfam_to_family;
open(FAM, $family_file) or die "Cannot open $family_file: $!";
while (<FAM>) {
    chomp;
    my @fields = split(/\t/);
    my ($rfam_id, $family) = ($fields[0], $fields[18]);
    $rfam_to_family{$rfam_id} = $family;
}
close(FAM);

print "##gff-version 3\n";

open(TBL, $tblout_file) or die "Cannot open $tblout_file: $!";
while (<TBL>) {
    next if /^#/;  # Skip comment lines
    chomp;
    my @fields = split(/\s+/);
    my ($seqid, $rfam_name, $start, $end, $strand) = @fields[3, 1, 9, 10, 11];
    my $rfam_id = $fields[2];
    my $score = $fields[16];
    my $evalue = $fields[17];
    my $family = $rfam_to_family{$rfam_id} || "NA";  # 如果没有找到family信息，则默认为"NA"
    print "$seqid\tcmscan\tncRNA\t$start\t$end\t$score\t$strand\t.\tID=$rfam_id;Name=$rfam_name;Evalue=$evalue;Family=\"$family\"\n";
}
close(TBL);

