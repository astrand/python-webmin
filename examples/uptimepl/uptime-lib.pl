# uptime-lib.pl
# Common functions for the uptime module

do '../web-lib.pl';
&init_config();


sub print_uptime
{
    print `uptime`;
}

