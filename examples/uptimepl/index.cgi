#!/usr/bin/env perl
# -*-Perl-*-

print "Content-type: text/html\n\n";

require './uptime-lib.pl';

&header("Uptime demo (Perl)", "", undef, 1, 1);
print "<hr>\n";

&print_uptime();

&footer("/", "index");

