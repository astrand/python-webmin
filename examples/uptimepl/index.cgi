#!/usr/bin/env perl
# -*-Perl-*-

require './uptime-lib.pl';

&header("Uptime demo (Perl)", "", undef, 1, 1);
print "<hr>\n";

print "<h3>System uptime</h3>\n";
&print_uptime();
print "<br><br>\n";

&footer("/", "index");

