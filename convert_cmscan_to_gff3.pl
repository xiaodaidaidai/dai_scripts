#!/usr/bin/env perl
# 
# convert_cmscan_to_gff3.pl: convert cmsearch or cmscan tblout files to GFF format
#                        

use strict;
use warnings;
use Getopt::Long;
use FindBin qw($Bin);
my $in_tblout  = "";   # name of input tblout file

my $usage;
$usage  = "convert_cmscan_to_gff3.pl\n\n";
$usage .= "Usage:\n\n";
$usage .= "convert_cmscan_to_gff3.pl [OPTIONS] <cmsearch tblout file>\n\tOR\n";
$usage .= "convert_cmscan_to_gff3.pl --cmscan [OPTIONS] <cmscan tblout file>\n\tOR\n";
$usage .= "convert_cmscan_to_gff3.pl --cmscan --fmt2 [OPTIONS] <cmscan --fmt 2 tblout file>\n\n";
$usage .= "\tOPTIONS:\n";
$usage .= "\t\t-T <n>       : minimum bit score to include is <n>\n";
$usage .= "\t\t-E <x>       : maximum E-value to include is <x>\n";
$usage .= "\t\t--cmscan     : tblout file was created by cmscan\n";
$usage .= "\t\t--source <s> : specify 'source' field should be <s> (e.g. tRNAscan-SE)\n";
$usage .= "\t\t--fmt2       : tblout file was created with cmscan --fmt 2 option\n";
$usage .= "\t\t--all        : output all info in 'attributes' column   [default: E-value]\n";
$usage .= "\t\t--none       : output no info in 'attributes' column    [default: E-value]\n";
$usage .= "\t\t--desc       : output desc field in 'attributes' column [default: E-value]\n";
$usage .= "\t\t--version <s>: append \"-<s>\" to 'source' column\n";
$usage .= "\t\t--extra <s>  : append \"<s>;\" to 'attributes' column\n";
$usage .= "\t\t--hidedesc   : do not includ \"desc\:\" prior to desc value in 'attributes' column\n";

my $do_minscore = 0;       # set to '1' if -T used
my $do_maxevalue = 0;      # set to '1' if -E used
my $minscore   = undef;    # defined if if -T used
my $maxevalue  = undef;    # defined if -E used
my $do_cmscan  = 0;        # set to '1' if --cmscan used
my $do_fmt2    = 0;        # set to '1' if --fmt
my $do_all_attributes = 0; # set to '1' if --all
my $do_no_attributes  = 0; # set to '1' if --none
my $do_de_attributes  = 0; # set to '1' if --desc
my $version = undef;       # defined if --version used
my $extra = undef;         # defined if --extra used
my $do_hidedesc = 0;       # set to 1 if --hidedesc used
my $opt_source = undef;    # set to <s> if --source <s> used

&GetOptions( "T=s"       => \$minscore,
             "E=s"       => \$maxevalue,
             "cmscan"    => \$do_cmscan,
             "source=s"  => \$opt_source,
             "fmt2"      => \$do_fmt2,
             "all"       => \$do_all_attributes,
             "none"      => \$do_no_attributes,
             "desc"      => \$do_de_attributes,
             "version=s" => \$version, 
             "extra=s"   => \$extra,
             "hidedesc"  => \$do_hidedesc);

if((scalar(@ARGV) != 1) && (-t STDIN)) { die $usage; }
my ($tblout_file) = @ARGV;

if(defined $minscore)  { $do_minscore  = 1; }
if(defined $maxevalue) { $do_maxevalue = 1; }
if($do_minscore && $do_maxevalue) { 
  die "ERROR, -T and -E cannot be used in combination. Pick one.";
}
if(($do_all_attributes) && ($do_no_attributes)) { 
  die "ERROR, --all and --none cannot be used in combination. Pick one.";
}
if(($do_all_attributes) && ($do_de_attributes)) { 
  die "ERROR, --all and --desc cannot be used in combination. Pick one.";
}
if(($do_no_attributes) && ($do_de_attributes)) { 
  die "ERROR, --none and --desc cannot be used in combination. Pick one.";
}
if(($do_fmt2) && (! $do_cmscan)) { 
  die "ERROR, --fmt2 only makes sense in combination with --cmscan"; 
}
if((defined $opt_source) && (defined $version)) { 
  die "ERROR, --source and --version are incompatible";
}

if(-t STDIN){
  if(! -e $tblout_file) { die "ERROR tblout file $tblout_file does not exist"; }
  if(! -s $tblout_file) { die "ERROR tblout file $tblout_file is empty"; }
}

my $source = ($do_cmscan) ? "cmscan" : "cmsearch";
if(defined $version)    { $source .= "-" . $version; }
if(defined $opt_source) { $source = $opt_source; }


open IN,"$Bin/rfam_class_type.txt" or die "$! $Bin/rfam_class_type.txt";
my %rfam_type=();
my %rfam_subtype=();
while(my $line=<IN>){
  chomp $line;
  next if $line=~/^#/;
  my @tmp=split(/\t/,$line);
  $rfam_subtype{$tmp[0]}=$tmp[-1];
  $rfam_type{$tmp[0]}=$tmp[-2];
}

close(IN);

if(-t STDIN){
  open(IN, $tblout_file) || die "ERROR unable to open $tblout_file for reading"; 
}else{
  open(IN, "<&=STDIN") || die "ERROR unable to open STDIN for reading"; 
}
my $line;
my $i;




while($line = <IN>) { 
  if($line !~ m/^\#/) { 
    chomp $line;
    my @el_A = split(/\s+/, $line);
    my $nfields = scalar(@el_A);
    if((! $do_fmt2) && ($nfields < 18)) { 
      die "ERROR expected at least 18 space delimited fields in tblout line (fmt 1, default) but got $nfields on line:\n$line\n"; 
    }
    if(($do_fmt2) && ($nfields < 27)) { 
      die "ERROR expected at least 27 space delimited fields in tblout line (fmt 2, --fmt2) but got $nfields on line:\n$line\n"; 
    }
    # ref Infernal 1.1.2 user guide, pages 59-61
    my $idx     = undef;
    my $seqname = undef;
    my $seqaccn = undef;
    my $mdlname = undef;
    my $mdlaccn = undef;
    my $clan    = undef;
    my $mdl     = undef;
    my $mdlfrom = undef;
    my $mdlto   = undef;
    my $seqfrom = undef;
    my $seqto   = undef;
    my $strand  = undef;
    my $trunc   = undef;
    my $pass    = undef;
    my $gc      = undef;
    my $bias    = undef;
    my $score   = undef;
    my $evalue  = undef;
    my $inc     = undef;
    my $olp     = undef;
    my $anyidx  = undef;
    my $anyfrct1= undef;
    my $anyfrct2= undef;
    my $winidx  = undef;
    my $winfrct1= undef;
    my $winfrct2= undef;
    my $desc    = undef;

    if($do_fmt2) { # 27 fields
      $idx     = $el_A[0];
      $seqname = ($do_cmscan) ? $el_A[3] : $el_A[1];
      $seqaccn = ($do_cmscan) ? $el_A[4] : $el_A[2];
      $mdlname = ($do_cmscan) ? $el_A[1] : $el_A[3];
      $mdlaccn = ($do_cmscan) ? $el_A[2] : $el_A[4];
      $clan    = $el_A[5];
      $mdl     = $el_A[6];
      $mdlfrom = $el_A[7];
      $mdlto   = $el_A[8];
      $seqfrom = $el_A[9];
      $seqto   = $el_A[10];
      $strand  = $el_A[11];
      $trunc   = $el_A[12];
      $pass    = $el_A[13];
      $gc      = $el_A[14];
      $bias    = $el_A[15];
      $score   = $el_A[16];
      $evalue  = $el_A[17];
      $inc     = $el_A[18];
      $olp     = $el_A[19];
      $anyidx  = $el_A[20];
      $anyfrct1= $el_A[21];
      $anyfrct2= $el_A[22];
      $winidx  = $el_A[23];
      $winfrct1= $el_A[24];
      $winfrct2= $el_A[25];
      $desc    = $el_A[26]; 
      for($i = 27; $i < $nfields; $i++) { $desc .= "_" . $el_A[$i]; }
    }
    else { # fmt 1, default
      $seqname = ($do_cmscan) ? $el_A[2] : $el_A[0];
      $seqaccn = ($do_cmscan) ? $el_A[3] : $el_A[1];
      $mdlname = ($do_cmscan) ? $el_A[0] : $el_A[2];
      $mdlaccn = ($do_cmscan) ? $el_A[1] : $el_A[3];
      $mdl     = $el_A[4];
      $mdlfrom = $el_A[5];
      $mdlto   = $el_A[6];
      $seqfrom = $el_A[7];
      $seqto   = $el_A[8];
      $strand  = $el_A[9];
      $trunc   = $el_A[10];
      $pass    = $el_A[11];
      $gc      = $el_A[12];
      $bias    = $el_A[13];
      $score   = $el_A[14];
      $evalue  = $el_A[15];
      $inc     = $el_A[16];
      $desc    = $el_A[17]; 
      for($i = 18; $i < $nfields; $i++) { $desc .= "_" . $el_A[$i]; }
    }
    
      #只输出 sRNA snoRNA miRNA rRNA  lncRNA tRNA snRNA
      next unless exists $rfam_type{$mdlaccn};
    
    # one sanity check, strand should make sense
    if(($strand ne "+") && ($strand ne "-")) { 
      if(($do_fmt2) && (($seqfrom eq "+") || ($seqfrom eq "-"))) { 
        die "ERROR problem parsing, you specified --fmt2 but tblout file appears to have NOT been created with --fmt 2, retry without --fmt2\nproblematic line:\n$line\n"; 
      }
      if((! $do_fmt2) && (($pass eq "+") || ($pass eq "-"))) { 
        die "ERROR problem parsing, you did not specify --fmt2 but tblout file appears to have been created with --fmt 2, retry with --fmt2\nproblematic line:\n$line\n"; 
      }
      die "ERROR unable to parse, problematic line:\n$line\n";
    }
    if(($do_minscore) && ($score < $minscore)) { 
      ; # skip
    }
    elsif(($do_maxevalue) && ($evalue > $maxevalue)) { 
      ; # skip
    }
    else { 
      my $attributes = "evalue=" . $evalue; # default to just evalue
      if($do_all_attributes) { 
        if($do_fmt2) { 
          #$attributes .= sprintf(";idx=$idx;seqaccn=$seqaccn;mdlaccn=$mdlaccn;clan=$clan;mdl=$mdl;mdlfrom=$mdlfrom;mdlto=$mdlto;trunc=$trunc;pass=$pass;gc=$gc;bias=$bias;inc=$inc;olp=$olp;anyidx=$anyidx;anyfrct1=$anyfrct1;anyfrct2=$anyfrct2;winidx=$winidx;winfrct1=$winfrct1;winfrct2=$winfrct2;%s$desc", ($do_hidedesc ? "" : "desc="));
          $attributes .= sprintf(";subtype=$rfam_subtype{$mdlaccn};mdlaccn=$mdlaccn;clan=$clan;%s$desc", ($do_hidedesc ? "" : "desc="));

          
        }
        else { 
          $attributes .= sprintf(";seqaccn=$seqaccn;mdlaccn=$mdlaccn;mdl=$mdl;mdlfrom=$mdlfrom;mdlto=$mdlto;trunc=$trunc;pass=$pass;gc=$gc;bias=$bias;inc=$inc;%s$desc", ($do_hidedesc ? "" : "desc="));
        }
      }
      elsif($do_no_attributes) { 
        $attributes = "-";
      }
      elsif($do_de_attributes) { 
        $attributes = $desc;
      }
      if(defined $extra) { 
        if($attributes eq "-")       { $attributes = ""; }
        elsif($attributes !~ m/\;$/) { $attributes .= ";"; }
        $attributes .= $extra . ";";
      }
      

      
      $attributes="ID=ncRNA-$rfam_type{$mdlaccn}-${seqname}-".sprintf( "%06d",$idx).";".$attributes;
      
      printf("%s\t%s\t%s\t%d\t%d\t%.1f\t%s\t%s\t%s\n", 
             $seqname,                             # token 1: 'sequence' (sequence name)
             $source,                              # token 2: 'source'
             #$mdlname,                           # token 3: 'feature' (model name) you may want to change this to 'ncRNA'
             $rfam_type{$mdlaccn},
             ($strand eq "+") ? $seqfrom : $seqto, # token 4: 'start' in coordinate space [1..seqlen], must be <= 'end'
             ($strand eq "+") ? $seqto : $seqfrom, # token 5: 'end' in coordinate space [1..seqlen], must be >= 'start'
             $score,                               # token 6: 'score' bit score
             $strand,                              # token 7: 'strand' ('+' or '-')
             ".",                                  # token 8: 'phase' irrelevant for noncoding RNAs
             $attributes);                         # token 9: attributes, currently only E-value, unless --all, --none or --desc
    }
  }
}