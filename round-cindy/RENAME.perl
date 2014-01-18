#! /usr/bin/perl -w
use strict;

open IN, "upload-mapping.wiki"
    || die "Unable to open upload-mapping.wiki\n";

while (defined (my $line = <IN>))
{
    chomp $line;
    if ($line =~ /^\| (.*) \|\| (.*)$/)
    {
        my $filename = $1;
        my $wikiname = $2;

        # Change wikiname to a filename, replace / with ., replace space with _

        $wikiname =~ s/\//./g;
        $wikiname =~ s/ /_/g;
        $wikiname = "${wikiname}.wiki";
        rename ($filename, $wikiname);
    }
}

close IN;
