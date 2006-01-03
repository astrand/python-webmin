# -*- coding: iso-8859-1 -*-
#
# webmin.py
# Python implementation of web-lib.pl
#
# Written by Peter Åstrand <peter@cendio.se>
# Copyright (C) 2002 Cendio Systems AB (http://www.cendio.se)
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License. 
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

#
# Coding style: Max linewidth 120 chars
#

import socket
import os
import sys
import re
import types
import cgi
import time
import cgi
# added for use in create_user_config_dirs()
import pwd,os.path
 
#
# Global variables
#
# Make sure to define these as global in funtions, if you want to change them. 
#
# main:: variables
session_id         = None
read_file_cache    = None
tempfilecount      = 0
done_webmin_header = 0
whatfailed         = None

# A dictionary with lists, like: {"john": ["webmin", "bsdexports"]}
acl_array_cache    = {}

# NOTE: I cannot understand what acl_hash_cache is good for in webmin.py. Therefore,
# I'm not using it at all. 
done_foreign_require = None
foreign_args         = None
no_acl_check         = None
no_referers_check    = None
locked_file_list     = None
locked_file_data     = None
locked_file_type     = None
locked_file_diff     = None
action_id_count      = None
done_seed_random     = None

# Miscellaneous
text                     = {}
tconfig                  = {} 
config                   = {}
gconfig                  = {}
userconfig               = {}
module_name              = None
module_config_directory  = None

# In web-lib.pl, tb is either "" or "bgcolor=#something".  I think this
# is ugly and it makes it hard to use HTMLgen.  In webmin.py, tb is
# either None or the color string like "#9999ff".  Same goes for cb. 
tb  = None
cb  = None

scriptname                    = None
remote_user                   = None
remote_user_info              = None
base_remote_user              = None
root_directory                = None
module_root_directory         = None
module_categories             = {}
current_lang                  = "en"
default_lang                  = "en"
list_languages_cache          = []
force_charset                 = None
user_module_config_directory  = None
pragma_no_cache               = None
loaded_theme_library          = None
module_info                   = None
indata                        = None
theme_no_table                = 0
anonymous_user                = 0
webmin_module                 = globals()



# ----------------------------------------------------------------
#                             Themes
#


# A string with the current theme name
current_theme = None

# ----------------------------------------------------------------
#                 Perl compatibility functions
#


def die(msg):
    print >> sys.stderr, msg
    sys.exit(1)



# Configuration and spool directories
try:
    config_directory = os.environ["WEBMIN_CONFIG"]
except KeyError:
    die("WEBMIN_CONFIG not set")

try:
    var_directory = os.environ["WEBMIN_VAR"]
except KeyError:
    die("WEBMIN_VAR not set")

try:
    session_id = os.environ["SESSION_ID"]
    del os.environ["SESSION_ID"]
except KeyError:
    pass


def read_file(file, dict=None):
    """Return a dictionary with name=value pairs from a file
    If an existing dictionary is given, it will be updated
    Note: Currently there is not way to check if the read failed or not.
    This function should probably raise an exception on error. 
    """
    if dict == None:
        dict = {}
    
    try:
        f = open(file)
    except:
        return dict

    for line in f:
        # Get rid of \n
        line = line.rstrip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        try:
            (name, value) = line.split("=")
        except ValueError:
            # We fail silently here, because that's the the Perl module does. 
            continue
        name = name.strip()
        value = value.strip()
        dict[name] = value

    return dict


def read_file_cached(file, dict=None):
    """Like read_file, but reads from a cache if the file has already been read
    """
    # FIXME
    if dict == None:
        dict = {}

    return read_file(file, dict)
        

def write_file(file, newdict):
    """Write out the contents of an associative array as name=value lines"""
    # FIXME: Maybe preserve order, some day.
    dict = read_file(file)
    dict.update(newdict)
    f = open(file, "w")
    for key in dict.keys():
        print >> f, "%s=%s" % (key, dict[key])

    # FIXME
    #if read_file_cached: update...


def html_escape(s):
    """Convert &, < and > codes in text to HTML entities"""
    return cgi.escape(s)


## tempname([filename])

def tempname():
    raise NotImplementedError

## Returns a mostly random temporary file name
#sub tempname
#{
#local $tmp_dir = -d $remote_user_info[7] ? "$remote_user_info[7]/.tmp" :
#                 @remote_user_info ? "/tmp/.webmin-$remote_user" :
#                                     "/tmp/.webmin";
#while(1) {
#        local @st = lstat($tmp_dir);
#        last if ($st[4] == $< && $st[5] == $( && $st[2] & 0x4000 &&
#                 ($st[2] & 0777) == 0755);
#        if (@st) {
#                unlink($tmp_dir) || rmdir($tmp_dir) ||
#                        system("/bin/rm -rf \"$tmp_dir\"");
#                }
#        mkdir($tmp_dir, 0755) || next;
#        chown($<, $(, $tmp_dir);
#        chmod(0755, $tmp_dir);
#        }
#if (defined($_[0]) && $_[0] !~ /\.\./) {
#        return "$tmp_dir/$_[0]";
#        }
#else {
#        $main::tempfilecount++;
#        &seed_random();
#        return $tmp_dir."/".int(rand(1000000))."_".
#               $main::tempfilecount."_".$scriptname;
#        }
#}
#
## trunc
def trunc():
    raise NotImplementedError
## Truncation a string to the shortest whole word less than or equal to
## the given width
#sub trunc {
#  local($str,$c);
#  if (length($_[0]) <= $_[1])
#    { return $_[0]; }
#  $str = substr($_[0],0,$_[1]);
#  do {
#    $c = chop($str);
#    } while($c !~ /\S/);
#  $str =~ s/\s+$//;
#  return $str;
#}
#
## indexof

def indexof():
    raise NotImplementedError
## Returns the index of some value in an array, or -1
#sub indexof {
#  local($i);
#  for($i=1; $i <= $#_; $i++) {
#    if ($_[$i] eq $_[0]) { return $i - 1; }
#    }
#  return -1;
#  }
#
## unique
def unique():
    raise NotImplementedError
## Returns the unique elements of some array
#sub unique
#{
#local(%found, @rv, $e);
#foreach $e (@_) {
#        if (!$found{$e}++) { push(@rv, $e); }
#        }
#return @rv;
#}
#
## sysprint(handle, [string]+)
def sysprint():
    raise NotImplementedError
#sub sysprint
#{
#local($str, $fh);
#$str = join('', @_[1..$#_]);
#$fh = $_[0];
#syswrite $fh, $str, length($str);
#}
#
## check_ipaddress(ip)

def check_ipaddress(ip):
    raise NotImplementedError
## Check if some IP address is properly formatted
#sub check_ipaddress
#{
#return $_[0] =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/ &&
#        $1 >= 0 && $1 <= 255 &&
#        $2 >= 0 && $2 <= 255 &&
#        $3 >= 0 && $3 <= 255 &&
#        $4 >= 0 && $4 <= 255;
#}
#

def generate_icon(image, title, link=None):
    if link:
        print "<table border><tr><td>"
        print "<a href='%s'><img src='%s' alt='' border=0 " % (link, image),
        print "width=48 height=48></a></td></tr></table>"
        print "<a href='%s'>%s</a>" % (link, title)
    else:
        print "<table border><tr><td>"
        print "<img src='%s' alt='' border=0 width=48 height=48>" % image,
        print "</td></tr></table>"
        print title


## urlize

def urlize():
    raise NotImplementedError
## Convert a string to a form ok for putting in a URL
#sub urlize {
#  local $rv = $_[0];
#  $rv =~ s/([^A-Za-z0-9])/sprintf("%%%2.2X", ord($1))/ge;
#  return $rv;
#
##  local($tmp, $tmp2, $c);
##  $tmp = $_[0];
##  $tmp2 = "";
##  while(($c = chop($tmp)) ne "") {
##	if ($c !~ /[A-z0-9]/) {
##		$c = sprintf("%%%2.2X", ord($c));
##		}
##	$tmp2 = $c . $tmp2;
##	}
##  return $tmp2;
#}
#
## un_urlize(string)
def un_urlize():
    raise NotImplementedError
## Converts a URL-encoded string to the original
#sub un_urlize
#{
#local $rv = $_[0];
#$rv =~ s/\+/ /g;
#$rv =~ s/%(..)/pack("c",hex($1))/ge;
#return $rv;
#}
#


def include(file):
    """Read and output the named file"""
    print open(file).read()


## copydata

def copydata():
    raise NotImplementedError
## Read from one file handle and write to another
#sub copydata
#{
#local($line, $out, $in);
#$out = $_[1];
#$in = $_[0];
#while($line = <$in>) {
#        print $out $line;
#        }
#}
#

def ReadParseMime():
    raise NotImplementedError
    # ReadParseMime
# Read data submitted via a POST request using the multipart/form-data coding
#sub ReadParseMime
#{
#local ($boundary, $line, $foo, $name);
#$ENV{CONTENT_TYPE} =~ /boundary=(.*)$/;
#$boundary = $1;
#<STDIN>;	# skip first boundary
#while(1) {
#        $name = "";
#        # Read section headers
#        local $lastheader;
#        while(1) {
#                $line = <STDIN>;
#                $line =~ s/\r|\n//g;
#                last if (!$line);
#                if ($line =~ /^(\S+):\s*(.*)$/) {
#                        $header{$lastheader = lc($1)} = $2;
#                        }
#                elsif ($line =~ /^\s+(.*)$/) {
#                        $header{$lastheader} .= $line;
#                        }
#                }
#
#        # Parse out filename and type
#        if ($header{'content-disposition'} =~ /^form-data(.*)/) {
#                $rest = $1;
#                while ($rest =~ /([a-zA-Z]*)=\"([^\"]*)\"(.*)/) {
#                        if ($1 eq 'name') {
#                                $name = $2;
#                                }
#                        else {
#                                $foo = $name . "_$1";
#                                $in{$foo} = $2;
#                                }
#                        $rest = $3;
#                        }
#                }
#        else {
#                &error("Missing Content-Disposition header");
#                }
#        if ($header{'content-type'} =~ /^([^\s;]+)/) {
#                $foo = $name . "_content_type";
#                $in{$foo} = $1;
#                }
#
#        # Read data
#        $in{$name} .= "\0" if (defined($in{$name}));
#        while(1) {
#                $line = <STDIN>;
#                if (!$line) { return; }
#                if (index($line, $boundary) != -1) { last; }
#                $in{$name} .= $line;
#                }
#        chop($in{$name}); chop($in{$name});
#        if (index($line,"$boundary--") != -1) { last; }
#        }
#}
#    

def ReadParse():
    global indata
    indata = cgi.FieldStorage()


def _PrintHeader(charset=None):
    """Outputs the HTTP header for HTML"""
    if pragma_no_cache and config.get("pragma_no_cache"):
        print "Pragma: no-cache"

    # FIXME: As far as I know, we should print \r as well. 
    if charset:
        print "Content-type: text/html; Charset=%s\n" % charset
    else:
        print "Content-type: text/html\n"

    # Flush
    sys.stdout.flush()
    sys.stderr.flush()

    # Make sure further errors are visible.
    sys.stderr = sys.stdout


def header(title, image=None, help=None, config=None, nomodule=None, nowebmin=None,
           rightside="", header=None, body="", below=None):
    """Output a page header with some title and image. The header may also
    include a link to help, and a link to the config page.
    The header will also have a link to to webmin index, and a link to the
    module menu if there is no config link.
    """
    if done_webmin_header: return
    for l in list_languages():
        if l["lang"] == current_lang:
            lang = l

    if force_charset:
        charset = force_charset
    elif lang.has_key("charset"):
        charset = lang["charset"]
    else:
        charset = "iso-8859-1"

    _PrintHeader(charset)
    _load_theme_library()
    if webmin_module.has_key("theme_header"):
        theme_header(title, image, help, config, nomodule, nowebmin,
                     rightside, header, body, below)
        return

    print "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\"\n\"http://www.w3.org/TR/REC-html40/loose.dtd\">"

    if gconfig.has_key("real_os_type"):
        os_type = gconfig["real_os_type"]
    else:
        os_type = gconfig["os_type"]

    if gconfig.has_key("real_os_version"):
        os_version = gconfig["real_os_version"]
    else:
        os_version = gconfig["os_version"]

    print "<html>\n<head>"
    if (charset):
        print "<meta http-equiv=\"Content-Type\" "\
              "content=\"text/html; charset=%s\">" % charset
    print "<link rel='icon' href='/images/webmin_icon.png' type='image/png'>"

    if gconfig.get("sysinfo") == 1:
        print "<title>%s : %s on %s (%s %s)</title>" % \
              (title, remote_user, get_system_hostname(), os_type, os_version)
    else:
        print "<title>%s</title>" % title

    if header:
        print header

    if gconfig.get("sysinfo") == 0 and remote_user:
        print "<SCRIPT LANGUAGE=\"JavaScript\">"
        if os.environ.has_key("SSL_USER"):
            userstring = " (SSL certified)"
        elif os.environ.has_key("LOCAL_USER"):
            userstring = " (Local user)"
        else:
            userstring = ""
        
        print "defaultStatus=\"%s%s logged into %s %s on %s (%s %s)\";" % \
              (remote_user, userstring, text["programname"], get_webmin_version(), 
               get_system_hostname(), os_type, os_version)
        print "</SCRIPT>"

    print tconfig.get("headhtml", ""),
    if tconfig.has_key("headinclude"):
        print open(os.path.join(root_directory, current_theme, tconfig["headinclude"])).read()

    print "</head>"

    bgcolor = tconfig.get("cs_page")
    if not bgcolor:
        bgcolor = gconfig.get("cs_page")
    if not bgcolor:
        bgcolor = "ffffff"
    
    link = tconfig.get("cs_link")
    if not link:
        link = gconfig.get("cs_link")
    if not link:
        link = "0000ee"

    text_color = tconfig.get("cs_text")
    if not text_color:
        text_color = gconfig.get("cs_text")
    if not text_color:
        text_color = "000000"

    if tconfig.has_key("bgimage"):
        bgimage = "background=" + tconfig["bgimage"]
    else:
        bgimage = ""

    inbody = tconfig.get("inbody", "")
    print "<body bgcolor=#%(bgcolor)s link=#%(link)s vlink=#%(link)s text=#%(text_color)s " \
          "%(bgimage)s %(inbody)s %(body)s>" % locals()

    hostname = get_system_hostname()
    version = get_webmin_version()
    prebody = tconfig.get("prebody", "")
    if prebody:
        prebody.replace("%HOSTNAME%", hostname)
        prebody.replace("%VERSION%", version)
        prebody.replace("%USER%", remote_user)
        prebody.replace("%OS%", os_type + os_version)
        print prebody

    if tconfig.get("prebodyinclude"):
        print open(os.path.join(root_directory, current_theme, tconfig["prebodyinclude"])).read()

    if webmin_module.has_key("theme_prebody"):
        theme_prebody(title, image, help, config, nomodule, nowebmin,
                      rightside, header, body, below)
    
    print "<table width=100%><tr>"
    if gconfig.get("sysinfo") == 2 and remote_user:
        print "<td colspan=3 align=center>"
        print "<tt>%s</tt>%s logged into %s %s on <tt>%s</tt> (%s %s)</td>" % \
              (remote_user, userstring, text["programname"], version, os_type, os_version)
        print "</tr> <tr>\n";

    print "<td width=15% valign=top align=left>"
    if os.environ.has_key("HTTP_WEBMIN_SERVERS"):
        print "<a href='%s'>" % os.environ["HTTP_WEBMIN_SERVERS"]
        print "%s</a><br>" % text["header_servers"]

    if not nowebmin and not tconfig.has_key("noindex"):
        acl = read_acl()
        mc = acl.has_key(base_remote_user)
        if gconfig.get("gotoone") and session_id and mc == 1:
            print "<a href='%s/session_login.cgi?logout=1'> %s</a><br>" % \
                  (gconfig.get("webprefix", ""), text["main_logout"])
        elif gconfig.get("gotoone") and mc == 1:
            print "<a href='%s/switch_user.cgi'> %s</a><br>" % \
                  (gconfig.get("webprefix", ""), text["main_switch"])
        else:
            print "<a href='%s/?cat=%s'> %s </a><br>" % \
                  (gconfig.get("webprefix", ""), module_info.get("category"), text["header_webmin"])

    if not nomodule:
        print "<a href='%s/%s'> %s </a><br>" % \
              (gconfig.get("webprefix", ""), module_name, text["header_module"])

    if type(help) == types.ListType:
        print hlink(text["header_help"], help[0], help[1]), "<br>"
    elif help:
        print hlink(text["header_help"], help), "<br>\n"

    if config:
        access = get_module_acl();
        if not access.get("noconfig"):
            if user_module_config_directory:
                cprog = "uconfig.cgi"
            else:
                cprog = "config.cgi"

            print "<a href='%s/%s?%s'> %s </a><br>" % \
                  (gconfig.get("webprefix", ""), cprog, module_name, text["header_config"])
            
    print "</td>"

    title.replace("&auml", "ä")
    title.replace("&ouml", "ö")
    title.replace("&aring", "å")
    title.replace("&uuml", "ü")
    title.replace("&nbsp;", " ")

    if image:
        print "<td align=center width=70%> <img alt='%s' src='%s'></td>" % \
              (image, image)
    elif lang["titles"] and not gconfig.get("texttitles") and not tconfig.get("texttitles"):
        print "<td align=center width=70%>"
        for char in title:
            charnum = ord(char)
            if charnum > 127 and lang.get("charset"):
                print "<img src='%s/images/letters/%d.%s.gif' alt='%s' align=bottom>" % \
                      (gconfig.get("webprefix", ""), charnum, lang["charset"], char)
            elif char == "":
                print "<img src='%s/images/letters/%d.gif' alt='&nbsp;' align=bottom>" % \
                      (gconfig.get("webprefix", ""), charnum)
            else:
                print "<img src='%s/images/letters/%d.gif' alt='%s' align=bottom>" % \
                      (gconfig.get("webprefix", ""), charnum, char)
        if below:
            print "<br>", below

        print "</td>"
    else:
        print "<td align=center width=70%%><h1>%s</h1></td>" % title

    print "<td width=15% valign=top align=right>"
    print rightside
    print "</td></tr></table>"


def footer(links=[], noendbody=None):
    """Output a footer for returning to some page
    The links parameter is a list of two-tuples, containing url and name, like:
    [('', 'module index'), ('list.cgi', 'users list')]
    
    """
    _load_theme_library()
    if webmin_module.has_key("theme_footer"):
        theme_footer(links, noendbody)
        return

    for i in range(len(links)):
        (url, name) = links[i]
        if url != "/" or not tconfig.get("noindex"):
            if url == "/":
                url = "/?cat=" + module_info["category"]
            elif url == "" and module_name:
                url = "/%s/" % module_name
            elif url.startswith("?") and module_name:
                url = "/%s/" + url
            if url.startswith("/"):
                url = gconfig.get("webprefix", "") + url
            if i == 0:
                print "<a href='%s'><img alg='<-' align=middle border=0 "\
                      "src='%s/images/left.gif'></a>" % (url, gconfig.get("webprefix", ""))
            else:
                print "&nbsp;|"
            print "&nbsp;<a href='%s'> %s</a>" % (url, textsub("main_return", name))
            
    print "<br>\n";
    if not noendbody:
        postbody = tconfig.get("postbody")
        if postbody:
            hostname = get_system_hostname()
            version = get_webmin_version()
            os_type = gconfig.get("real_os_type")
            if not os_type:
                os_type = gconfig.get("os_type")
            os_version = gconfig.get("real_os_version")
            if not os_version:
                os_version = gconfig.get("os_version")

            postbody.replace("%HOSTNAME%", hostname)
            postbody.replace("%VERSION%", version)
            postbody.replace("%USER%", remote_user)
            postbody.replace("%OS%", os_type + os_version)
            print postbody

        if tconfig.get("postbodyinclude"):
            f = open(os.path.join(root_directory, current_theme, tconfig.get("postbodyinclude")))
            print f.read()

        if webmin_module.has_key("theme_postbody"):
            theme_postbody(links, noendbody)

        print "</body></html>"


def _load_theme_library():
    """Load theme library"""
    if not current_theme or not tconfig.get("functions") or loaded_theme_library:
        return
    filename = tconfig["functions"]

    # HACK!
    if filename.endswith(".pl"):
        filename = filename[:-3] + ".py"

    themefile = os.path.join(root_directory, current_theme, filename)
    if not os.path.exists(themefile):
        themefile = os.path.join(os.path.split(__file__)[0],
                                 current_theme,
                                 filename)
    try:
        execfile(themefile, webmin_module, webmin_module)
    except IOError:
        pass

def redirect(url=""):
    """Output headers to redirect the browser to some page"""
    if url==None: url=""
    server_port=os.environ.get("SERVER_PORT","")
    https=os.environ.get("HTTPS","").upper()
    script_name=os.environ.get("SCRIPT_NAME","")
    if server_port == "443" and https == "ON":
        port=""
    elif server_port == "80" and https != "ON":
        port=""
    else:
        port=":"+server_port
    prot="http"
    if https == "ON":
        prot="https"
    if gconfig.has_key("webprefixnoredir"):
        wp=gconfig["webprefixnoredir"]
    else:
        wp=gconfig.get("webprefix","")
    if re.compile("^(http|https|ftp|gopher):").search(url):
        url=url
    elif url.startswith("/"):
        url="%s://%s%s%s%s" %(prot,os.environ.get("SERVER_NAME",""),port,wp,url)
    elif re.compile("^(.*)\/[^\/]*$").search(script_name):
        url="%s://%s%s%s/%s%s" %(prot,os.environ.get("SERVER_NAME",""),port,re.compile("^(.*)\/[^\/]*$").search(script_name).group(1),wp,url)
    else:
        url="%s://%s%s/%s%s" %(prot,os.environ.get("SERVER_NAME",""),port,wp,url)

    print "Location: %s\n\n" % url



## kill_byname(name, signal)

def kill_byname(name, signal):
    raise NotImplementedError
## Use the command defined in the global config to find and send a signal
## to a process matching some name
#sub kill_byname
#{
#local(@pids);
#@pids = &find_byname($_[0]);
#if (@pids) { kill($_[1], @pids); return scalar(@pids); }
#else { return 0; }
#}
#
## kill_byname_logged(name, signal)

def kill_byname_logged(name, signal):
    raise NotImplementedError

## Like kill_byname, but also logs the killing
#sub kill_byname_logged
#{
#local(@pids);
#@pids = &find_byname($_[0]);
#if (@pids) { &kill_logged($_[1], @pids); return scalar(@pids); }
#else { return 0; }
#}
#
## find_byname(name)

def find_byname(name):
    raise NotImplementedError
## Finds a process by name, and returns a list of matching PIDs
#sub find_byname
#{
#local($cmd, @pids);
#$cmd = $gconfig{'find_pid_command'};
#$cmd =~ s/NAME/"$_[0]"/g;
#@pids = split(/\n/, `($cmd) </dev/null 2>/dev/null`);
#@pids = grep { $_ != $$ } @pids;
#return @pids;
#}
#

def error(*message):
    """Display an error message and exit. The global variable whatfailed
    must be set to the name of the operation that failed."""
    _load_theme_library()
    if not os.environ.has_key("REQUEST_METHOD"):
        # Show text-only error
        print >> sys.stderr, text["error"]
        print >> sys.stderr, "-----"
        if whatfailed:
            print >> sys.stderr, whatfailed, " : "
        else:
            for msg in message:
                print >> sys.stderr, msg
        print >> sys.stderr, "-----"
    elif webmin_module.has_key("theme_error"):
        theme_error(*message)
    else:
        header(text['error'], "");
        print "<hr>"
        if whatfailed:
            print >> sys.stderr, whatfailed, " : "
        else:
            for msg in message:
                print >> sys.stderr, msg
        print "<hr>"
        footer()


def _error_setup():
    # Note: this is probably a public function, although it is not lised on http://www.webmin.com/modules.html
    raise NotImplementedError

## error_setup(message)
## Register a message to be prepended to all error strings
#sub error_setup
#{
#$main::whatfailed = $_[0];
#}
#
## wait_for(handle, regexp, regexp, ...)

def wait_for():
    raise NotImplementedError
## Read from the input stream until one of the regexps matches..
#sub wait_for
#{
#local($hit, $c, $i, $sw, $rv, $ha); undef($wait_for_input);
##print STDERR "wait_for(",join(",", @_),")\n";
#$ha = $_[0];
#$codes =
#"undef(\$hit);\n".
#"while(1) {\n".
#" if ((\$c = getc($ha)) eq \"\") { return -1; }\n".
#" \$wait_for_input .= \$c;\n";
##" \$wait_for_input .= \$c;\nprint STDERR \$wait_for_input,\"\\n\";";
#for($i=1; $i<@_; $i++) {
#        $sw = $i>1 ? "elsif" : "if";
#        $codes .= " $sw (\$wait_for_input =~ /$_[$i]/i) { \$hit = $i-1; }\n";
#        }
#$codes .=
#" if (defined(\$hit)) {\n".
#"  \@matches = (-1, \$1, \$2, \$3, \$4, \$5, \$6, \$7, \$8, \$9);\n".
#"  return \$hit;\n".
#"  }\n".
#" }\n";
#$rv = eval $codes;
#if ($@) { &error("wait_for error : $@\n"); }
#return $rv;
#}
#
## fast_wait_for(handle, string, string, ...)
def fast_wait_for():
    raise NotImplementedError
#sub fast_wait_for
#{
#local($inp, $maxlen, $ha, $i, $c, $inpl);
#for($i=1; $i<@_; $i++) {
#        $maxlen = length($_[$i]) > $maxlen ? length($_[$i]) : $maxlen;
#        }
#$ha = $_[0];
#while(1) {
#        if (($c = getc($ha)) eq "") {
#                &error("fast_wait_for read error : $!");
#                }
#        $inp .= $c;
#        if (length($inp) > $maxlen) {
#                $inp = substr($inp, length($inp)-$maxlen);
#                }
#        $inpl = length($inp);
#        for($i=1; $i<@_; $i++) {
#                if ($_[$i] eq substr($inp, $inpl-length($_[$i]))) {
#                        return $i-1;
#                        }
#                }
#        }
#}
#


def has_command(command):
    """Returns the full path if some command is in the path, None if not"""
    for path_dir in os.environ["PATH"].split(os.pathsep):
        fullpath = os.path.join(path_dir, command)
        if os.path.exists(fullpath):
            fstat = os.stat(fullpath)
            if fstat[stat.ST_UID] == os.getuid():
                # We own this file
                if fstat[stat.ST_MODE] & stat.S_IXUSR:
                    return fullpath
                else: continue
            elif fstat[stat.ST_GID] == os.getgid():
                # Our group
                if fstat[stat.ST_MODE] & stat.S_IXGRP:
                    return fullpath
                else: continue
            else:
                # Other
                if fstat[stat.ST_MODE] & stat.S_IXOTH:
                    return fullpath
                else: continue
    return None


def make_date(seconds):
    """Converts a Unix date/time in seconds to a human-readable form """
    # FIXME: Translation support. Make sure we use same format as web-lib.pl.
    return time.ctime(seconds)
    
def file_chooser_button(input, choosetype, form=0, chroot="/", addmode=0,
                        ashtml=1):
    """Return HTML for a file chooser button, if the browser supports
    Javascript.

    @input: The name of the input field in which the filename/directory choosen
            in the chooser should appear.

    @choosetype: 0 if both file and directories should be selectable. 1 for
                 directories only.

    @form: The form index for the form in which the input field in @input
           exists.

    @chroot: The path the chooser should begin with.

    @addmode: I don't know what this is, but the parameter exists in the
              perl implementation, so it's implemented here as well.

    @ashtml: If this is set as 0, a hash suitable as argument to a
             Input element in HTMLgen will be returned instead of a
             string.
    """
    
    ret = {'type':'button'}
    ret['onClick'] = "ifield = document.forms[%d].%s; chooser = window.open('%s/chooser.cgi?add=%d&type=%s&chroot=%s&file='+ifield.value, 'chooser', 'toolbar=no,menubar=no,scrollbar=no,width=400,heigh=300'); chooser.ifield = ifield; window.ifield = ifield" % (form, input, gconfig.get('webprefix', ''), addmode, choosetype, chroot)
    ret['value'] = '...'

    if ashtml:
        return "<input type=\"%(type)s\" onClick=%(onClick)s value=%(value)s>\n" % ret
    else:
        return ret

def read_acl():
    """Reads the acl file and return dictionary"""
    global acl_array_cache
    if not acl_array_cache:
        for line in open(_acl_filename()):
            # Get rid of \n
            line = line.rstrip()
            if not line: continue
            match = re.search("^(\S+):\s*(.*)", line)
            if match:
                user = match.group(1)
                modules = match.group(2).split()
                acl_array_cache[user] = modules
    
    # Available as global variables, but return anyway...
    return acl_array_cache


def _acl_filename():
    """Returns the file containing the webmin ACL"""
    return os.path.join(config_directory, "webmin.acl");


## get_miniserv_config(&array)
def _get_miniserv_config():
    raise NotImplementedError
## Store miniserv configuration into the given array
#sub get_miniserv_config
#{
#return &read_file($ENV{'MINISERV_CONFIG'}, $_[0]);
#}
#
## put_miniserv_config(&array)
def _put_miniserv_config():
    raise NotImplementedError
## Store miniserv configuration from the given array
#sub put_miniserv_config
#{
#&write_file($ENV{'MINISERV_CONFIG'}, $_[0]);
#}
#
## restart_miniserv()
## Send a HUP signal to miniserv
def _restart_miniserv():
    raise NotImplementedError
#sub restart_miniserv
#{
#local($pid, %miniserv, $addr, $i);
#&get_miniserv_config(\%miniserv) || return;
#$miniserv{'inetd'} && return;
#open(PID, $miniserv{'pidfile'}) || &error("Failed to open pid file");
#chop($pid = <PID>);
#close(PID);
#if (!$pid) { &error("Invalid pid file"); }
#&kill_logged('HUP', $pid);
#
## wait for miniserv to come back up
#$addr = inet_aton($miniserv{'bind'} ? $miniserv{'bind'} : "127.0.0.1");
#for($i=0; $i<20; $i++) {
#        sleep(1);
#        socket(STEST, PF_INET, SOCK_STREAM, getprotobyname("tcp"));
#        $rv = connect(STEST, sockaddr_in($miniserv{'port'}, $addr));
#        close(STEST);
#        if ($rv) { last; }
#        }
#if ($i == 20) { &error("Failed to restart Webmin server!"); }
#}
#

def check_os_support(minfo):
    oss = minfo.get("os_support")
    if not oss or oss == "*":
        # No problem
        return

    os = ver = codes = None

    while 1:
        match = re.search("^([^\/\s]+)\/([^\{\s]+)\{([^\}]*)\}\s*(.*)$", oss)
        if match:
            os = match.group(1)
            ver = match.group(2)
            codes = match.group(3)
            oss = match.group(4)
        else:
            match = re.search("^([^\/\s]+)\/([^\/\s]+)\s*(.*)$", oss)
            if match:
                os = match.group(1)
                ver = match.group(2)
                oss = match.group(3)
            else:
                match = re.search("^([^\{\s]+)\{([^\}]*)\}\s*(.*)$", oss)
                if match:
                    os = match.group(1)
                    codes = match.group(2)
                    oss = match.group(3)
                else:
                    match = re.search("^\{([^\}]*)\}\s*(.*)$", oss)
                    if match:
                        codes = match.group(1)
                        oss = match.group(2)
                    else:
                        match = re.search("^(\S+)\s*(.*)$", oss)
                        if match:
                            os = match.group(1)
                            oss = match.group(2)
                        else:
                            # Couldn't parse
                            return 0

        if os and os != gconfig.get("os_type"):
            continue
        if ver and ver != gconfig.get("os_version"):
            continue
        if codes:
            # FIXME: Do something like below, but check quoting. 
            #os.system("""perl -e 'exit(%s);'""")
            continue
        # No problem
        return 1



## http_download(host, port, page, destfile, [&error], [&callback])

def http_download():
    raise NotImplementedError
## Download data from a HTTP url to a local file
#sub http_download
#{
#$SIG{ALRM} = "download_timeout";
#alarm(60);
#local $h = &make_http_connection($_[0], $_[1], 0, "GET", $_[2]);
#if (!ref($h)) {
#        if ($_[4]) { ${$_[4]} = $h; return; }
#        else { &error($h); }
#        }
#alarm(0);
#&write_http_connection($h, "Host: $_[0]\r\n");
#&write_http_connection($h, "User-agent: Webmin\r\n");
#&write_http_connection($h, "\r\n");
#&complete_http_download($h, $_[3], $_[4], $_[5]);
#}
#
## complete_http_download(handle, destfile, [&error], [&callback])
## Do a HTTP download, after the headers have been sent
def _complete_http_download():
    raise NotImplementedError
#sub complete_http_download
#{
#local($line, %header, $s);
#local $cbfunc = $_[3];
#
## read headers
#alarm(60);
#($line = &read_http_connection($_[0])) =~ s/\r|\n//g;
#if ($line !~ /^HTTP\/1\..\s+(200|302|301)\s+/) {
#        if ($_[2]) { ${$_[2]} = $line; return; }
#        else { &error("Download failed : $line"); }
#        }
#local $rcode = $1;
#&$cbfunc(1, $rcode == 302 || $rcode == 301 ? 1 : 0) if ($cbfunc);
#while(($line = &read_http_connection($_[0])) =~ /^(\S+):\s+(.*)$/) {
#        $header{lc($1)} = $2;
#        }
#alarm(0);
#&$cbfunc(2, $header{'content-length'}) if ($cbfunc);
#if ($rcode == 302 || $rcode == 301) {
#        # follow the redirect
#        &$cbfunc(5, $header{'location'}) if ($cbfunc);
#        local ($host, $port, $page);
#        if ($header{'location'} =~ /^http:\/\/([^:]+):(\d+)(\/.*)$/) {
#                $host = $1; $port = $2; $page = $3;
#                }
#        elsif ($header{'location'} =~ /^http:\/\/([^:\/]+)(\/.*)$/) {
#                $host = $1; $port = 80; $page = $2;
#                }
#        else {
#                if ($_[2]) { ${$_[2]} = "Missing Location header"; return; }
#                else { &error("Missing Location header"); }
#                }
#        &http_download($host, $port, $page, $_[1], $_[2], $cbfunc);
#        }
#else {
#        # read data
#        if (ref($_[1])) {
#                # Append to a variable
#                while(defined($buf = &read_http_connection($_[0], 1024))) {
#                        ${$_[1]} .= $buf;
#                        &$cbfunc(3, length(${$_[1]})) if ($cbfunc);
#                        }
#                }
#        else {
#                # Write to a file
#                local $got = 0;
#                open(PFILE, "> $_[1]");
#                while(defined($buf = &read_http_connection($_[0], 1024))) {
#                        print PFILE $buf;
#                        $got += length($buf);
#                        &$cbfunc(3, $got) if ($cbfunc);
#                        }
#                close(PFILE);
#                }
#        &$cbfunc(4) if ($cbfunc);
#        }
#&close_http_connection($_[0]);
#}
#
#
## ftp_download(host, file, destfile, [&error], [&callback])
def ftp_download():
    raise NotImplementedError
## Download data from an FTP site to a local file
#sub ftp_download
#{
#local($buf, @n);
#local $cbfunc = $_[4];
#
#$SIG{ALRM} = "download_timeout";
#alarm(60);
#if ($gconfig{'ftp_proxy'} =~ /^http:\/\/(\S+):(\d+)/ && !&no_proxy($_[0])) {
#        # download through http-style proxy
#        &open_socket($1, $2, "SOCK", $_[3]) || return 0;
#        print SOCK "GET ftp://$_[0]$_[1] HTTP/1.0\r\n";
#        print SOCK "User-agent: Webmin\r\n";
#        print SOCK "\r\n";
#        &complete_http_download({ 'fh' => "SOCK" }, $_[2], $_[3], $_[4]);
#        }
#else {
#        # connect to host and login
#        &open_socket($_[0], 21, "SOCK", $_[3]) || return 0;
#        alarm(0);
#        &ftp_command("", 2, $_[3]) || return 0;
#        &ftp_command("user anonymous", 3, $_[3]) || return 0;
#        &ftp_command("pass root\@".&get_system_hostname(), 2, $_[3]) || return 0;
#        &$cbfunc(1, 0) if ($cbfunc);
#
#        if ($cbfunc) {
#                # get the file size
#                local $size = &ftp_command("size $_[1]", 2, $_[3]);
#                defined($size) || return 0;
#                &$cbfunc(2, int($size));
#                }
#
#        # request the file
#        &ftp_command("type i", 2, $_[3]) || return 0;
#        local $pasv = &ftp_command("pasv", 2, $_[3]);
#        defined($pasv) || return 0;
#        $pasv =~ /\(([0-9,]+)\)/;
#        @n = split(/,/ , $1);
#        &open_socket("$n[0].$n[1].$n[2].$n[3]", $n[4]*256 + $n[5], "CON", $_[3]) || return 0;
#        &ftp_command("retr $_[1]", 1, $_[3]) || return 0;
#
#        # transfer data
#        local $got = 0;
#        open(PFILE, "> $_[2]");
#        while(read(CON, $buf, 1024) > 0) {
#                print PFILE $buf;
#                $got += length($buf);
#                &$cbfunc(3, $got) if ($cbfunc);
#                }
#        close(PFILE);
#        close(CON);
#        &$cbfunc(4) if ($cbfunc);
#
#        # finish off..
#        &ftp_command("", 2, $_[3]) || return 0;
#        &ftp_command("quit", 2, $_[3]) || return 0;
#        close(SOCK);
#        }
#return 1;
#}
#
## no_proxy(host)
## Checks if some host is on the no proxy list
def _no_proxy():
    raise NotImplementedError
#sub no_proxy
#{
#foreach $n (split(/\s+/, $gconfig{'noproxy'})) {
#        if ($_[0] =~ /$n/) { return 1; }
#        }
#return 0;
#}
#
## open_socket(host, port, handle, [&error])
def _open_socket():
    raise NotImplementedError
#sub open_socket
#{
#local($addr, $h); $h = $_[2];
#if (!socket($h, PF_INET, SOCK_STREAM, getprotobyname("tcp"))) {
#        if ($_[3]) { ${$_[3]} = "Failed to create socket : $!"; return 0; }
#        else { &error("Failed to create socket : $!"); }
#        }
#if (!($addr = inet_aton($_[0]))) {
#        if ($_[3]) { ${$_[3]} = "Failed to lookup IP address for $_[0]"; return 0; }
#        else { &error("Failed to lookup IP address for $_[0]"); }
#        }
#if (!connect($h, sockaddr_in($_[1], $addr))) {
#        if ($_[3]) { ${$_[3]} = "Failed to connect to $_[0]:$_[1] : $!"; return 0; }
#        else { &error("Failed to connect to $_[0]:$_[1] : $!"); }
#        }
#select($h); $| =1; select(STDOUT);
#return 1;
#}
#
#
## download_timeout()
## Called when a download times out
def _download_timeout():
    raise NotImplementedError
#sub download_timeout
#{
#&error("Timeout downloading $in{url}");
#}
#
#
## ftp_command(command, expected, [&error])
## Send an FTP command, and die if the reply is not what was expected
def _ftp_command():
    raise NotImplementedError
#sub ftp_command
#{
#local($line, $rcode, $reply);
#$what = $_[0] ne "" ? "<i>$_[0]</i>" : "initial connection";
#if ($_[0] ne "") {
#        print SOCK "$_[0]\r\n";
#        }
#alarm(60);
#if (!($line = <SOCK>)) {
#        if ($_[2]) { ${$_[2]} = "Failed to read reply to $what"; return undef; }
#        else { &error("Failed to read reply to $what"); }
#        }
#$line =~ /^(...)(.)(.*)$/;
#if (int($1/100) != $_[1]) {
#        if ($_[2]) { ${$_[2]} = "$what failed : $3"; return undef; }
#        else { &error("$what failed : $3"); }
#        }
#$rcode = $1; $reply = $3;
#if ($2 eq "-") {
#        # Need to skip extra stuff..
#        while(1) {
#                if (!($line = <SOCK>)) {
#                        if ($_[2]) { ${$_[2]} = "Failed to read reply to $what";
#                                     return undef; }
#                        else { &error("Failed to read reply to $what"); }
#                        }
#                $line =~ /^(....)(.*)$/; $reply .= $2;
#                if ($1 eq "$rcode ") { last; }
#                }
#        }
#alarm(0);
#return $reply;
#}
#
## to_ipaddress(hostname)
def to_ipaddress():
    raise NotImplementedError
## Converts a hostname to an a.b.c.d format IP address
#sub to_ipaddress
#{
#if (&check_ipaddress($_[0])) {
#        return $_[0];
#        }
#else {
#        local(@ip);
#        @ip = unpack("CCCC", gethostbyname($_[0]));
#        if (@ip) { return join("." , @ip); }
#        else { return undef; }
#        }
#}


def icons_table(iconlist, columns=None):
    """Renders a 4-column table of icons
    The argument is a list of tuples (link, title, icon). 
    """
    if not columns:
        columns = min(4, len(iconlist))

    per = int(100.0 / columns)
    print "<table width=100% cellpadding=5> <tr>"
    for i in range(0, len(iconlist)):
        (link, title, icon) = iconlist[i]
        print "<td width=%d%% align=center valign=top>" % per
        generate_icon(icon, title, link)
        print "</td>"
        if i % columns == columns - 1:
            print "</tr>"

    while i % columns:
        i += 1
        print "<td width=%d%%></td>" % per
    
    print "</table><p>"


## replace_file_line(file, line, [newline]*)
def replace_file_line():
    raise NotImplementedError
## Replaces one line in some file with 0 or more new lines
#sub replace_file_line
#{
#local(@lines);
#open(FILE, $_[0]);
#@lines = <FILE>;
#close(FILE);
#if (@_ > 2) { splice(@lines, $_[1], 1, @_[2..$#_]); }
#else { splice(@lines, $_[1], 1); }
#open(FILE, "> $_[0]");
#print FILE @lines;
#close(FILE);
#}
#
## read_file_lines(file)
def read_file_lines():
    raise NotImplementedError
## Returns a reference to an array containing the lines from some file. This
## array can be modified, and will be written out when flush_file_lines()
## is called.
#sub read_file_lines
#{
#if (!$file_cache{$_[0]}) {
#        local(@lines, $_);
#        open(READFILE, $_[0]);
#        while(<READFILE>) {
#                s/\r|\n//g;
#                push(@lines, $_);
#                }
#        close(READFILE);
#        $file_cache{$_[0]} = \@lines;
#        }
#return $file_cache{$_[0]};
#}
#
## flush_file_lines()
def flush_file_lines():
    raise NotImplementedError
#sub flush_file_lines
#{
#foreach $f (keys %file_cache) {
#        open(FLUSHFILE, "> $f");
#        foreach $line (@{$file_cache{$f}}) {
#                print FLUSHFILE $line,"\n";
#                }
#        close(FLUSHFILE);               
#        }                               
#undef(%file_cache);
#}                                       
#
## unix_user_input(fieldname, user)
## Returns HTML for an input to select a Unix user
def _unix_user_input():
    raise NotImplementedError
#sub unix_user_input
#{
#return "<input name=$_[0] size=8 value=\"$_[1]\"> ".
#       &user_chooser_button($_[0], 0)."\n";
#}
#
## unix_group_input(fieldname, user)
## Returns HTML for an input to select a Unix group
def _unix_group_input():
    raise NotImplementedError
#sub unix_group_input
#{
#return "<input name=$_[0] size=8 value=\"$_[1]\"> ".
#       &group_chooser_button($_[0], 0)."\n";
#}
#

def hlink(text, page, module=None):
    """Returns HTML for a link to a help page"""
    if not module:
        mod = module_name
    else:
        mod = module
    return "<a onClick='window.open(\""+gconfig.get("webprefix","")+"/help.cgi/"+mod+"/"+page+"\", \"help\", \"toolbar=no,menubar=no,scrollbars=yes,width=400,height=300,resizable=yes\"); return false' href=\""+gconfig.get("webprefix","")+"/help.cgi/"+mod+"/"+page+"\">"+text+"</a>"
    
#sub hlink
#{
#local $mod = $_[2] ? $_[2] : $module_name;
#return "<a onClick='window.open(\"$gconfig{'webprefix'}/help.cgi/$mod/$_[1]\", \"help\", \"toolbar=no,menubar=no,scrollbars=yes,width=400,height=300,resizable=yes\"); return false' href=\"$gconfig{'webprefix'}/help.cgi/$mod/$_[1]\">$_[0]</a>";
#}
#
## user_chooser_button(field, multiple, [form])

def user_chooser_button():
    raise NotImplementedError
## Returns HTML for a javascript button for choosing a Unix user or users
#sub user_chooser_button
#{
#local $form = @_ > 2 ? $_[2] : 0;
#local $w = $_[1] ? 500 : 300;
#return "<input type=button onClick='ifield = document.forms[$form].$_[0]; chooser = window.open(\"$gconfig{'webprefix'}/user_chooser.cgi?multi=$_[1]&user=\"+escape(ifield.value), \"chooser\", \"toolbar=no,menubar=no,scrollbars=yes,width=$w,height=200\"); chooser.ifield = ifield' value=\"...\">\n";
#}
#
## group_chooser_button(field, multiple, [form])
def group_chooser_button():
    raise NotImplementedError
## Returns HTML for a javascript button for choosing a Unix group or groups
#sub group_chooser_button
#{
#local $form = @_ > 2 ? $_[2] : 0;
#local $w = $_[1] ? 500 : 300;
#return "<input type=button onClick='ifield = document.forms[$form].$_[0]; chooser = window.open(\"$gconfig{'webprefix'}/group_chooser.cgi?multi=$_[1]&group=\"+escape(ifield.value), \"chooser\", \"toolbar=no,menubar=no,scrollbars=yes,width=$w,height=200\"); chooser.ifield = ifield' value=\"...\">\n";
#}
#
## foreign_check(module)

def foreign_check():
    raise NotImplementedError
## Checks if some other module exists and is supported on this OS
#sub foreign_check
#{
#local %minfo;
#&read_file_cached("$root_directory/$_[0]/module.info", \%minfo) || return 0;
#return &check_os_support(\%minfo);
#}
#
## foreign_require(module, file)

def foreign_require(module, file):
    raise NotImplementedError
## Brings in functions from another module
#sub foreign_require
#{
#return 1 if ($main::done_foreign_require{$_[0],$_[1]}++);
#local $pkg = $_[0] ? $_[0] : "global";
#local @OLDINC = @INC;
#@INC = &unique("$root_directory/$_[0]", @INC);
#chdir("$root_directory/$_[0]") if (!$module_name && $_[0]);
#eval <<EOF;
#package $pkg;
#\$ENV{'FOREIGN_MODULE_NAME'} = '$_[0]';
#\$ENV{'FOREIGN_ROOT_DIRECTORY'} = '$root_directory';
#do "$root_directory/$_[0]/$_[1]";
#EOF
#@OLDINC = @INC;
#if ($@) { &error("require $_[0]/$_[1] failed : $@"); }
#return 1;
#}
#
## foreign_call(module, function, [arg]*)

def foreign_call():
    raise NotImplementedError
## Call a function in another module
#sub foreign_call
#{
#local $pkg = $_[0] ? $_[0] : "global";
#local @args = @_[2 .. @_-1];
#$main::foreign_args = \@args;
#local @rv = eval <<EOF;
#package $pkg;
#&$_[1](\@{\$main::foreign_args});
#EOF
#if ($@) { &error("$_[0]::$_[1] failed : $@"); }
#return wantarray ? @rv : $rv[0];
#}
#
## foreign_config(module)

def foreign_config():
    raise NotImplementedError
## Get the configuration from another module
#sub foreign_config
#{
#local %fconfig;
#&read_file_cached("$config_directory/$_[0]/config", \%fconfig);
#return %fconfig;
#}
#
## get_system_hostname()

def get_system_hostname():
    """Returns the hostname of this system"""
    return socket.gethostname()


def get_webmin_version():
    """Returns the version of Webmin currently being run"""
    line = open(os.path.join(root_directory, "version")).readline()
    return line.strip()

def get_module_acl(user=None, module=None):
    """Returns an array containing access control options for the given user"""
    if user:
        u = user
    else:
        u = base_remote_user

    if module:
        m = module
    else:
        m = module_name

        rv = read_file_cached(os.path.join(root_directory, m, "defaultacl"))
        if gconfig.has_key("risk_" + u) and m:
            rf = gconfig.get("risk_" + u) + ".risk"
            rv = read_file_cached(os.path.join(root_directory, m, rf), rv)
            sf = gconfig.get("skill_" + u) + ".skill"
            rv = read_file_cached(os.path.join(root_directory, m, sf), rv)
        else:
            rv = read_file_cached(os.path.join(config_directory, m, u + ".acl"), rv)
            if remote_user != base_remote_user and not user:
                rv = read_file_cached(os.path.join(config_directory, m, remote_user + ".acl"), rv)

    return rv

## save_module_acl(&acl, [user], [module])

def save_module_acl():
    raise NotImplementedError
## Updates the acl hash for some user and module (or the current one)
#sub save_module_acl
#{
#local $u = $_[1] ? $_[1] : $base_remote_user;
#local $m = $_[2] ? $_[2] : $module_name;
#&write_file("$config_directory/$m/$u.acl", $_[0]);
#}
#

# Note: I think this function is too long. The reason why I'm not splitting it is
# that I want to stay as close to web-lib.pl as possible. 
def init_config():
    """Sets the following global (for the webmin module) variables
    %config - Per-module configuration
    %gconfig - Global configuration
    $tb - Background for table headers
    $cb - Background for table bodies
    $scriptname - Base name of the current perl script
    $module_name - The name of the current module
    $module_config_directory - The config directory for this module
    $webmin_logfile - The detailed logfile for webmin
    $remote_user - The actual username used to login to webmin
    $base_remote_user - The username whose permissions are in effect
    $current_theme - The theme currently in use
    $root_directory - The root directory of this webmin install
    """
    global config, gconfig, module_name, module_config_directory, tb, cb, \
           scriptname, remote_user, base_remote_user, current_theme, \
           root_directory, module_root_directory, module_info
    global no_acl_check, no_referers_check, current_lang, text

    # Read the webmin global config file. This contains the OS type and version,
    # OS specific configuration and global options such as proxy servers
    read_file_cached(os.path.join(config_directory, "config"),
                     gconfig)

    # Set PATH and LD_LIBRARY_PATH
    if gconfig.has_key("path"): os.environ["PATH"] = gconfig["path"]
    if gconfig.has_key("ld_env"): os.environ[gconfig["ld_env"]] = gconfig.get("ld_path", "")

    if os.environ.has_key("FOREIGN_MODULE_NAME"):
        # In a foreign call - use the module name given
        root_directory = os.environ["FOREIGN_ROOT_DIRECTORY"]
        module_name = os.environ["FOREIGN_MODULE_NAME"]
    elif os.environ.has_key("SCRIPT_NAME"):
        sn = os.environ["SCRIPT_NAME"]
        if gconfig.has_key("webprefix"):
            sn = sn.replace(gconfig.get("webprefix", ""), "")
        match = re.search("^\/([^\/]+)\/", sn)
        if match:
            module_name = match.group(1)

        if os.environ.has_key("SERVER_ROOT"):
            root_directory = os.environ["SERVER_ROOT"]
        elif os.environ.has_key("SCRIPT_FILENAME"):
            root_directory = os.environ["SCRIPT_FILENAME"]
            root_directory = root_directory.replace(sn, "")
    else:
        if re.search("^(.*)\/([^\/]+)\/[^\/]+$", sys.argv[0]):
            root_directory = sys.argv[1]
            module_name = sys.argv[2]

    if (module_name):
        module_config_directory = os.path.join(config_directory, module_name)
        config = read_file_cached(os.path.join(module_config_directory, "config"))
        module_info = get_module_info(module_name, noclone=1)
        module_root_directory = os.path.join(root_directory, module_name)

    # Get the username
    if os.environ.has_key("BASE_REMOTE_USER"):
        u = os.environ["BASE_REMOTE_USER"]
    else:
        u = os.environ["REMOTE_USER"]

    base_remote_user = u
    remote_user = os.environ["REMOTE_USER"]
        
    # Set some useful variables
    # FIXME: Themes disabled, because no themes are ported yet. 
    if not current_theme:
        current_theme = gconfig.get("theme_" + base_remote_user)
    if not current_theme:
        current_theme = gconfig.get("theme", "")

    if current_theme:
        read_file_cached(os.path.join(root_directory,
                                      current_theme, "config"),
                         tconfig)

    tmpdict = {"cs_header" : "#9999ff"}
    tmpdict.update(gconfig)
    tmpdict.update(tconfig)
    tb = tmpdict["cs_header"]

    tmpdict = {"cs_table" : "#cccccc"}
    tmpdict.update(gconfig)
    tmpdict.update(tconfig)
    cb = tmpdict["cs_table"]

    if tconfig.has_key("tb"):
        tb = tconfig["tb"]
    if tconfig.has_key("cb"):
        cb = tconfig["cb"]

    # We assume argv[0] does not end with a slash. 
    scriptname = re.search("([^\/]+)$", sys.argv[0]).group(1)
    if gconfig.has_key("webmin_log"):
        webmin_logfile = gconfig["webmin_log"]
    else:
        webmin_logfile = os.path.join(os.environ["WEBMIN_VAR"], "webmin.log")
        
    # Load language strings into %text
    current_lang = gconfig.get("lang_" + remote_user)
    if not current_lang:
        current_lang = gconfig.get("lang_" + base_remote_user)
    if not current_lang:
        current_lang = gconfig.get("lang")
    if not current_lang:
        current_lang = default_lang

    text = load_language(module_name)
    if not text:
        error("Failed to determine Webmin root from SERVER_ROOT or SCRIPT_FILENAME")


    # Check if the HTTP user can access this module
    if (module_name and not no_acl_check and not
        os.environ.has_key("FOREIGN_MODULE_NAME")):
        acl = read_acl()
        risk = gconfig.get("risk_" + u)
        if risk:
            # Dummy loop, so we can break out
            for dummy in [0]:
                if risk == "high":
                    break
                if not module_info.get("risk"):
                    break
                if module_info["risk"].find(risk) != -1:
                    # Found
                    break
                error(textsub('emodule', "<i>%s</i>" % u,
                              "<i>%s</i>" % module_info["desc"]))
        else:
            allowed_modules = acl.get(u, [])
            if not (module_name in allowed_modules) and \
                   not ('*' in allowed_modules):
                error(textsub('emodule', "<i>%s</i>" % u,
                              "<i>%s</i>" % module_info.get("desc")))
            
        no_acl_check = 1

    # Check the Referer: header for nasty redirects
    referers = gconfig.get("referers", "").split()
    http_referer = os.environ.get("HTTP_REFERER", "")
    match = re.search("^(http|https|ftp):\/\/([^:]+:[^@]+@)?([^\/:@]+)", http_referer)
    if match:
        referer_site = match.group(3)
    else:
        referer_site = None

    http_host = os.environ.get("HTTP_HOST", "")
    http_host = re.sub(":\d+$", "", http_host)

    if (sys.argv[0] and
        not re.search("^\/(index.cgi)?$", os.environ.get("SCRIPT_NAME")) and
        not re.search("referer_save.cgi$", sys.argv[0]) and
        not re.search("session_login.cgi$", sys.argv[0]) and
        not gconfig.has_key("referer") and
        os.environ.has_key("MINISERV_CONFIG") and
        not no_referers_check and
        not re.search("Webmin",  os.environ.get("HTTP_USER_AGENT", ""), re.I) and
        # Referer site
        (referer_site and (referer_site != http_host) and
         not referer_site in referers and
         gconfig["referers_none"] and not trust_unknown_referers)):
        # Looks like a link from elsewhere ..
        header("referer_title", "", None, 0, 1, 1)
        print "<hr><center>\n"
        print "<form action=/referer_save.cgi>\n"
        ReadParse()
        for k in indata.keys():
            # FIXME: This is probably not correct. 
            for kk in indata[k].split("\0"):
                print "<input type=hidden name=%s value='%s'>" % (k, kk)
        
        print "<input type=hidden name=referer_original " \
              "value='%s'>" % os.environ["REQUEST_URI"]

        if os.environ.get("HTTPS", "").lower() == "on":
            prot = "https"
        else:
            prot = "http"

        url = "<tt>%s://%s%s</tt>" % (prot, os.environ.get("HTTP_HOST"),
                                      os.environ.get("REQUEST_URI"))

        if (referer_site):
            print textsub('referer_warn', "<tt>%s</tt>" %
                          os.environ.get("HTTP_REFERER"), url), "<p>"
            
        else:
            print "<p>", textsub('referer_warn_unknown', url), "<p>"
        print "<input type=submit value='%s'><br>" % text["referer_ok"]
        print "<input type=checkbox name=referer_again value=1> ", \
              text["referer_again"], "<p>"
        print "</form></center><hr>"
        footer("/", text['index'])
        return

    no_referers_check = 1
    return 1


#$main::no_referers_check++;
#
#return 1;
#}
#
#$default_lang = "en";
#

def load_language(module=None):
    """Returns a hashtable mapping text codes to strings in the appropriate language"""
    root = root_directory
    ol = gconfig.get("overlang", "")

    # Read global lang files
    local_text = read_file_cached(os.path.join(root, "lang", default_lang))
    
    if not local_text:
        return {}
    if default_lang != current_lang:
        read_file_cached(os.path.join(root, "lang", current_lang),
                         local_text)
    if ol:
        read_file_cached(os.path.join(root, ol, default_lang),
                         local_text)

        if default_lang != current_lang:
            read_file_cached(os.path.join(root, ol, current_lang),
                             local_text)
                                      
    read_file_cached(os.path.join(config_directory, "custom-lang"),
                     local_text)

    if module:
        # Read module's lang files
        read_file_cached(os.path.join(root, module, "lang", default_lang),
                         local_text)
        if default_lang != current_lang:
            read_file_cached(os.path.join(root, module, "lang", current_lang),
                             local_text)
        if ol:
            read_file_cached(os.path.join(root, module, ol, default_lang),
                             local_text)
            if default_lang != current_lang:
                read_file_cached(os.path.join(root, module, ol, current_lang),
                                 local_text)
        read_file_cached(os.path.join(config_directory, module, "custom-lang"),
                         local_text)
        
    for key in local_text.keys():
        match = re.search("\$([A-Za-z0-9\.\-\_]+)", local_text[key])
        # FIXME
        #local_text = re.sub("\$([A-Za-z0-9\.\-\_]+)",
        #                    lambda match: text_subs(match.group(1), local_text))

    return local_text


def _text_subs(s, dict):
    if dict.has_key(s):
        return dict[s]
    else:
        return "$" + s
    
def textsub(message, *substitute):
    rv = text.get(message, "")
    for i in range (0, len(substitute)):
        # The translation string variables began at $1, thus the +1
        rv = re.sub("\$%d" % (i + 1), substitute[i], rv)
    return rv

# This function seems to be unused. Defined anyway. 
def terror(*params):
    error(textsub(*params))
    
def encode_base64(s):
    """Encodes a string into base64 format"""
    return base64.encodestring(s)


def decode_base64(s):
    """Converts a base64 string into plain text"""
    return base64.decodestring(s)


# FIXME: This function is called from init_config(), but before the current_lang
# variable has been initalized. Strange...
def get_module_info(module, noclone=None):
    """Returns a hash containg a module name, desc and os_support"""
    if module.startswith("."): return {}
    rv = read_file_cached(os.path.join(root_directory, module, "module.info"))
    
    if not rv:
        return {}

    clone = os.path.islink(os.path.join(root_directory, module))
    if rv.has_key("desc_" + current_lang):
        rv["desc"] = rv["desc_" + current_lang]

    if clone and not noclone and config_directory:
        rv["clone"] = rv.get("desc", "")
        rv = read_file(os.path.join(config_directory, module, "clone"))

    rv["dir"] = module
    global module_categories
    if not module_categories and config_directory:
        module_categories = read_file_cached(os.path.join(config_directory, "webmin.cats"))

    rv["realcategory"] = rv.get("category", "")
    if module_categories.has_key(module):
        rv["category"] = module_categories[module]

    return rv


def get_all_module_infos(nocache=None):
    """Returns a vector contains the information on all modules in this webmin
    install, including clones, like:
    [{"name": "mysql", "desc_sv": "MySQL-databasserver"}]
    """
    # Dict with dicts. Key is "modulename variable".
    cache_dict = {}
    # Dict with dicts with minfos. Key is "modulename".
    all_modules_dict = {}
    
    cache_file = os.path.join(config_directory, "module.infos.cache")
    cache_dict = read_file_cached(cache_file)
    st = os.stat(root_directory)
    if not nocache and cache_dict.get("lang") == current_lang and \
           cache_dict.get("mtime") == str(st.st_mtime):
        # Can use existing module.info cache
        for k in cache_dict.keys():
            try:
                # Try to split this key. 
                (module, variable) = k.split(None, 1)
            except ValueError:
                # Malformed line (or mtime=) or something like that
                continue
            value = cache_dict[k]
            try:
                modinfo = all_modules_dict[module]
            except KeyError:
                all_modules_dict[module] = modinfo = {}

            modinfo[variable] = value

    else:
        # Need to rebuild cache
        # Dictionary of dictionaries, during cache read
        for entry in os.listdir(root_directory):
            # Only deal with directories
            if not os.path.isdir(os.path.join(root_directory, entry)): continue
            modinfo = get_module_info(entry)
            if not modinfo: continue
            for variable in modinfo.keys():
                cache_dict["%s %s" % (entry, variable)] = modinfo[variable]
            all_modules_dict[entry] = modinfo

        cache_dict["lang"] = current_lang
        cache_dict["mtime"] = str(st.st_mtime)
        if not nocache:
            write_file(cache_file, cache_dict)
            
    # Return list of module info dictionaries
    return all_modules_dict.values()


## get_theme_info(theme)
def get_theme_info():
    raise NotImplementedError
## Returns a hash containing a theme's details
#sub get_theme_info
#{
#return () if ($_[0] =~ /^\./);
#local %rv;
#&read_file("$root_directory/$_[0]/theme.info", \%rv) || return ();
#$rv{"desc"} = $rv{"desc_$current_lang"} if ($rv{"desc_$current_lang"});
#$rv{"dir"} = $_[0];
#return %rv;
#}
#


def list_languages():
    """Returns a list of dictionaries with supported languages, like:
    
    [{'lang': 'en', 'titles': '1', 'desc': 'English'},
    {'lang': 'de', 'titles': '1', 'desc': 'German'}]

    The list is sorted on 'desc'. 
    
    """
    global list_languages_cache
    if not list_languages_cache:
        for line in open(os.path.join(root_directory, "lang_list.txt")):
            # Get rid of \n
            line = line.rstrip()
            # Separate line in two chunks
            try:
                (infostring, desc) = line.split(None, 1)
            except ValueError:
                # Malformed line
                continue
            lang = {"desc": desc}
            for nameval in infostring.split(","):
                # nameval is something like "titles=0"
                try:
                    (name, val) = nameval.split("=")
                    lang[name] = val
                except ValueError:
                    # Its a bit strange that we should continue in this case,
                    # but web-lib does it, so...
                    continue
            # The line below is from web-lib.pl. I have no idea what it does...
            #$l->{'index'} = scalar(@rv);
            list_languages_cache.append(lang)

        # Done with file. Sort.
        list_languages_cache.sort(lambda x,y: x["desc"] < y["desc"])

        
    return list_languages_cache


## read_env_file(file, &array)
def read_env_file():
    raise NotImplementedError
#sub read_env_file
#{
#open(FILE, $_[0]) || return 0;
#while(<FILE>) {
#        s/#.*$//g;
#        if (/([A-z0-9_\.]+)\s*=\s*"(.*)"/ ||
#            /([A-z0-9_\.]+)\s*=\s*'(.*)'/ ||
#            /([A-z0-9_\.]+)\s*=\s*(.*)/) {
#                $_[1]->{$1} = $2;
#                }
#        }
#close(FILE);
#return 1;
#}
#
## write_env_file(file, &array, export)
def write_env_file():
    raise NotImplementedError
#sub write_env_file
#{
#local $k;
#local $exp = $_[2] ? "export " : "";
#open(FILE, ">$_[0]");
#foreach $k (keys %{$_[1]}) {
#        local $v = $_[1]->{$k};
#        if ($v =~ /^\S+$/) {
#                print FILE "$exp$k=$v\n";
#                }
#        else {
#                print FILE "$exp$k=\"$v\"\n";
#                }
#        }
#close(FILE);
#}
#
## lock_file(filename, [readonly], [forcefile])
def lock_file():
    raise NotImplementedError
## Lock a file for exclusive access. If the file is already locked, spin
## until it is freed. This version uses a .lock file, which is not very reliable.
#sub lock_file
#{
#return if (!$_[0] || defined($main::locked_file_list{$_[0]}));
#local $lock_tries_count = 0;
#while(1) {
#        local $pid;
#        if (open(LOCKING, "$_[0].lock")) {
#                chop($pid = <LOCKING>);
#                close(LOCKING);
#                }
#        if (!$pid || !kill(0, $pid) || $pid == $$) {
#                # got the lock!
#                open(LOCKING, ">$_[0].lock");
#                print LOCKING $$,"\n";
#                close(LOCKING);
#                $main::locked_file_list{$_[0]} = int($_[1]);
#                if ($gconfig{'logfiles'} && !$_[1]) {
#                        # Grab a copy of this file for later diffing
#                        local $lnk;
#                        $main::locked_file_data{$_[0]} = undef;
#                        if (-d $_[0]) {
#                                $main::locked_file_type{$_[0]} = 1;
#                                $main::locked_file_data{$_[0]} = '';
#                                }
#                        elsif (!$_[2] && ($lnk = readlink($_[0]))) {
#                                $main::locked_file_type{$_[0]} = 2;
#                                $main::locked_file_data{$_[0]} = $lnk;
#                                }
#                        elsif (open(ORIGFILE, $_[0])) {
#                                $main::locked_file_type{$_[0]} = 0;
#                                $main::locked_file_data{$_[0]} = '';
#                                while(<ORIGFILE>) {
#                                        $main::locked_file_data{$_[0]} .= $_;
#                                        }
#                                close(ORIGFILE);
#                                }
#                        }
#                last;
#                }
#        sleep(1);
#        if ($lock_tries_count++ > 5*60) {
#                # Give up after 5 minutes
#                &error(textsub('elock_tries', "<tt>$_[0]</tt>", 5));
#                }
#        }
#}
#
## unlock_file(filename)
## Release a lock on a file. When unlocking a file that was locked in
## read mode, optionally save the update in RCS
def unlock_file():
    raise NotImplementedError
#sub unlock_file
#{
#return if (!$_[0] || !defined($main::locked_file_list{$_[0]}));
#unlink("$_[0].lock");
#delete($main::locked_file_list{$_[0]});
#if (exists($main::locked_file_data{$_[0]})) {
#        # Diff the new file with the old
#        stat($_[0]);
#        local $lnk = readlink($_[0]);
#        local $type = -d _ ? 1 : $lnk ? 2 : 0;
#        local $oldtype = $main::locked_file_type{$_[0]};
#        local $new = !defined($main::locked_file_data{$_[0]});
#        if ($new && !-e _) {
#                # file doesn't exist, and never did! do nothing ..
#                }
#        elsif ($new && $type == 1 || !$new && $oldtype == 1) {
#                # is (or was) a directory ..
#                if (-d _ && !defined($main::locked_file_data{$_[0]})) {
#                        push(@main::locked_file_diff,
#                             { 'type' => 'mkdir', 'object' => $_[0] });
#                        }
#                elsif (!-d _ && defined($main::locked_file_data{$_[0]})) {
#                        push(@main::locked_file_diff,
#                             { 'type' => 'rmdir', 'object' => $_[0] });
#                        }
#                }
#        elsif ($new && $type == 2 || !$new && $oldtype == 2) {
#                # is (or was) a symlink ..
#                if ($lnk && !defined($main::locked_file_data{$_[0]})) {
#                        push(@main::locked_file_diff,
#                             { 'type' => 'symlink', 'object' => $_[0],
#                               'data' => $lnk });
#                        }
#                elsif (!$lnk && defined($main::locked_file_data{$_[0]})) {
#                        push(@main::locked_file_diff,
#                             { 'type' => 'unsymlink', 'object' => $_[0],
#                               'data' => $main::locked_file_data{$_[0]} });
#                        }
#                elsif ($lnk ne $main::locked_file_data{$_[0]}) {
#                        push(@main::locked_file_diff,
#                             { 'type' => 'resymlink', 'object' => $_[0],
#                               'data' => $lnk });
#                        }
#                }
#        else {
#                # is a file, or has changed type?!
#                local ($diff, $delete_file);
#                local $type = "modify";
#                if (!-r _) {
#                        open(NEWFILE, ">$_[0]");
#                        close(NEWFILE);
#                        $delete_file++;
#                        $type = "delete";
#                        }
#                if (!defined($main::locked_file_data{$_[0]})) {
#                        $type = "create";
#                        }
#                open(ORIGFILE, ">$_[0].webminorig");
#                print ORIGFILE $main::locked_file_data{$_[0]};
#                close(ORIGFILE);
#                $diff = `diff "$_[0].webminorig" "$_[0]"`;
#                push(@main::locked_file_diff,
#                     { 'type' => $type, 'object' => $_[0],
#                       'data' => $diff } ) if ($diff);
#                unlink("$_[0].webminorig");
#                unlink($_[0]) if ($delete_file);
#                }
#        delete($main::locked_file_data{$_[0]});
#        delete($main::locked_file_type{$_[0]});
#        }
#}
#
## unlock_all_files()
def unlock_all_files():
    raise NotImplementedError
## Unlocks all files locked by this program
#sub unlock_all_files
#{
#foreach $f (keys %main::locked_file_list) {
#        &unlock_file($f);
#        }
#}
#
## webmin_log(action, type, object, &params, [module])
def webmin_log():
    raise NotImplementedError
## Log some action taken by a user
#sub webmin_log
#{
#return if (!$gconfig{'log'});
#local $m = $_[4] ? $_[4] : $module_name;
#
#if ($gconfig{'logclear'}) {
#        # check if it is time to clear the log
#        local @st = stat("$webmin_logfile.time");
#        local $write_logtime = 0;
#        if (@st) {
#                if ($st[9]+$gconfig{'logtime'}*60*60 < time()) {
#                        # clear logfile and all diff files
#                        system("rm -f $ENV{'WEBMIN_VAR'}/diffs/* 2>/dev/null");
#                        unlink($webmin_logfile);
#                        $write_logtime = 1;
#                        }
#                }
#        else { $write_logtime = 1; }
#        if ($write_logtime) {
#                open(LOGTIME, ">$webmin_logfile.time");
#                print LOGTIME time(),"\n";
#                close(LOGTIME);
#                }
#        }
#
## should logging be done at all?
#return if ($gconfig{'logusers'} && &indexof($base_remote_user,
#           split(/\s+/, $gconfig{'logusers'})) < 0);
#return if ($gconfig{'logmodules'} && &indexof($m,
#           split(/\s+/, $gconfig{'logmodules'})) < 0);
#
## log the action
#local $now = time();
#local @tm = localtime($now);
#local $script_name = $0 =~ /([^\/]+)$/ ? $1 : '-';
#local $id = sprintf "%d.%d.%d",
#                $now, $$, $main::action_id_count;
#$main::action_id_count++;
#local $line = sprintf "%s [%2.2d/%s/%4.4d %2.2d:%2.2d:%2.2d] %s %s %s %s %s \"%s\" \"%s\" \"%s\"",
#        $id, $tm[3], $text{"smonth_".($tm[4]+1)}, $tm[5]+1900,
#        $tm[2], $tm[1], $tm[0],
#        $remote_user, $main::session_id ? $main::session_id : '-',
#        $ENV{'REMOTE_HOST'},
#        $m, $script_name,
#        $_[0], $_[1] ne '' ? $_[1] : '-', $_[2] ne '' ? $_[2] : '-';
#foreach $k (sort { $a cmp $b } keys %{$_[3]}) {
#        local $v = $_[3]->{$k};
#        if ($v eq '') {
#                $line .= " $k=''";
#                }
#        elsif (ref($v) eq 'ARRAY') {
#                foreach $vv (@$v) {
#                        next if (ref($vv));
#                        $vv =~ s/(['"\\\r\n\t\%])/sprintf("%%%2.2X",ord($1))/ge;
#                        $line .= " $k='$vv'";
#                        }
#                }
#        elsif (!ref($v)) {
#                foreach $vv (split(/\0/, $v)) {
#                        $vv =~ s/(['"\\\r\n\t\%])/sprintf("%%%2.2X",ord($1))/ge;
#                        $line .= " $k='$vv'";
#                        }
#                }
#        }
#open(WEBMINLOG, ">>$webmin_logfile");
#print WEBMINLOG $line,"\n";
#close(WEBMINLOG);
#
#if ($gconfig{'logfiles'}) {
#        # Find and record the changes made to any locked files
#        local $i = 0;
#        mkdir("$ENV{'WEBMIN_VAR'}/diffs", 0700);
#        foreach $d (@main::locked_file_diff) {
#                open(DIFFLOG, ">$ENV{'WEBMIN_VAR'}/diffs/$id.$i");
#                print DIFFLOG "$d->{'type'} $d->{'object'}\n";
#                print DIFFLOG $d->{'data'};
#                close(DIFFLOG);
#                $i++;
#                }
#        @main::locked_file_diff = undef;
#        }
#}
#
## additional_log(type, object, data)
## Records additional log data for an upcoming call to webmin_log, such
## as command that was run or SQL that was executed.
def additional_log():
    raise NotImplementedError
#sub additional_log
#{
#if ($gconfig{'logfiles'}) {
#        push(@main::locked_file_diff,
#             { 'type' => $_[0], 'object' => $_[1], 'data' => $_[2] } );
#        }
#}
#
## system_logged(command)
def system_logged():
    raise NotImplementedError
## Just calls the system() function, but also logs the command
#sub system_logged
#{
#local $cmd = join(" ", @_);
#local $and;
#if ($cmd =~ s/(\s*&\s*)$//) {
#        $and = $1;
#        }
#while($cmd =~ s/(\d*)(<|>)((\/\S+)|&\d+)\s*$//) { }
#$cmd =~ s/^\((.*)\)\s*$/$1/;
#$cmd .= $and;
#&additional_log('exec', undef, $cmd);
#return system(@_);
#}
#
## backquote_logged(command)
def backquote_logged():
    raise NotImplementedError
## Executes a command and returns the output (like `cmd`), but also logs it
#sub backquote_logged
#{
#local $cmd = $_[0];
#local $amd;
#if ($cmd =~ s/(\s*&\s*)$//) {
#        $and = $1;
#        }
#while($cmd =~ s/(\d*)(<|>)((\/\S+)|&\d+)\s*$//) { }
#$cmd =~ s/^\((.*)\)\s*$/$1/;
#$cmd .= $and;
#&additional_log('exec', undef, $cmd);
#return `$_[0]`;
#}
#
## kill_logged(signal, pid, ...)
def kill_logged():
    raise NotImplementedError
#sub kill_logged
#{
#&additional_log('kill', $_[0], join(" ", @_[1..@_-1])) if (@_ > 1);
#return kill(@_);
#}
#
## rename_logged(old, new)
def rename_logged():
    raise NotImplementedError
#sub rename_logged
#{
#&additional_log('rename', $_[0], $_[1]) if ($_[0] ne $_[1]);
#return rename($_[0], $_[1]);
#}
#
## remote_foreign_require(server, module, file)
def remote_foreign_require():
    raise NotImplementedError
## Connect to rpc.cgi on a remote webmin server and have it open a session
## to a process that will actually do the require and run functions.
#sub remote_foreign_require
#{
#local $call = { 'action' => 'require',
#                'module' => $_[1],
#                'file' => $_[2] };
#if ($remote_session{$_[0]}) {
#        $call->{'session'} = $remote_session{$_[0]};
#        }
#else {
#        $call->{'newsession'} = 1;
#        }
#local $rv = &remote_rpc_call($_[0], $call);
#$remote_session{$_[0]} = $rv->{'session'} if ($rv->{'session'});
#}
#
## remote_foreign_call(server, module, function, [arg]*)
def remote_foreign_call():
    raise NotImplementedError
## Call a function on a remote server. Must have been setup first with
## remote_foreign_require for the same server and module
#sub remote_foreign_call
#{
#return &remote_rpc_call($_[0], { 'action' => 'call',
#                                 'module' => $_[1],
#                                 'func' => $_[2],
#                                 'session' => $remote_session{$_[0]},
#                                 'args' => [ @_[3 .. $#_] ] } );
#}
#
## remote_foreign_check(server, module)
def remote_foreign_check():
    raise NotImplementedError
## Checks if some module is installed and supported on a remote server
#sub remote_foreign_check
#{
#return &remote_rpc_call($_[0], { 'action' => 'check',
#                                 'module' => $_[1] });
#}
#
## remote_foreign_config(server, module)
def remote_foreign_config():
    raise NotImplementedError
## Gets the configuration for some module from a remote server
#sub remote_foreign_config
#{
#return &remote_rpc_call($_[0], { 'action' => 'config',
#                                 'module' => $_[1] });
#}
#
## remote_eval(server, module, code)
def remote_eval():
    raise NotImplementedError
## Eval some perl code in the context of a module on a remote webmin server
#sub remote_eval
#{
#return &remote_rpc_call($_[0], { 'action' => 'eval',
#                                 'module' => $_[1],
#                                 'code' => $_[2],
#                                 'session' => $remote_session{$_[0]} });
#}
#
## remote_write(server, localfile, [remotefile])
def remote_write():
    raise NotImplementedError
#sub remote_write
#{
#local ($data, $got);
#if ($remote_server_version{$_[0]} >= 0.966) {
#        # Copy data over TCP connection
#        local $rv = &remote_rpc_call($_[0],
#                        { 'action' => 'tcpwrite', 'file' => $_[2] } );
#        local $error;
#        &open_socket($_[0], $rv->[1], TWRITE, \$error);
#        return &$remote_error_handler("Failed to transfer file : $error")
#                if ($error);
#        open(FILE, $_[1]);
#        while(read(FILE, $got, 1024) > 0) {
#                print TWRITE $got;
#                }
#        close(FILE);
#        close(TWRITE);
#        return $rv->[0];
#        }
#else {
#        # Just pass file contents as parameters
#        open(FILE, $_[1]);
#        while(read(FILE, $got, 1024) > 0) {
#                $data .= $got;
#                }
#        close(FILE);
#        return &remote_rpc_call($_[0], { 'action' => 'write',
#                                         'data' => $data,
#                                         'file' => $_[2],
#                                         'session' => $remote_session{$_[0]} });
#        }
#}
#
## remote_read(server, localfile, remotefile)
def remote_read():
    raise NotImplementedError
#sub remote_read
#{
#if ($remote_server_version{$_[0]} >= 0.966) {
#        # Copy data over TCP connection
#        local $rv = &remote_rpc_call($_[0],
#                        { 'action' => 'tcpread', 'file' => $_[2] } );
#        local $error;
#        &open_socket($_[0], $rv->[1], TREAD, \$error);
#        return &$remote_error_handler("Failed to transfer file : $error")
#                if ($error);
#        local $got;
#        open(FILE, ">$_[1]");
#        while(read(TREAD, $got, 1024) > 0) {
#                print FILE $got;
#                }
#        close(FILE);
#        close(TREAD);
#        }
#else {
#        # Just get data as return value
#        local $d = &remote_rpc_call($_[0], { 'action' => 'read',
#                                     'file' => $_[2],
#                                     'session' => $remote_session{$_[0]} });
#        open(FILE, ">$_[1]");
#        print FILE $d;
#        close(FILE);
#        }
#}
#
## remote_finished()
def remote_finished():
    raise NotImplementedError
## Close all remote sessions. This happens automatically after a while
## anyway, but this function should be called to clean things up faster.
#sub remote_finished
#{
#foreach $h (keys %remote_session) {
#        &remote_rpc_call($h, { 'action' => 'quit',
#                               'session' => $remote_session{$h} } );
#        }
#foreach $fh (keys %fast_fh_cache) {
#        close($fh);
#        }
#}
#
## remote_error_setup(&function)
def remote_error_setup():
    raise NotImplementedError
## Sets a function to be called instead of &error when a remote RPC fails
#sub remote_error_setup
#{
#$remote_error_handler = $_[0];
#}
#
## remote_rpc_call(server, structure)
## Calls rpc.cgi on some server and passes it a perl structure (hash,array,etc)
## and then reads back a reply structure
#sub remote_rpc_call
def _remote_rpc_call():
    raise NotImplementedError
#{
#local $serv;
#if ($_[0]) {
#        # lookup the server in the webmin servers module if needed
#        if (!defined(%remote_servers_cache)) {
#                &foreign_require("servers", "servers-lib.pl");
#                foreach $s (&foreign_call("servers", "list_servers")) {
#                        $remote_servers_cache{$s->{'host'}} = $s;
#                        }
#                }
#        $serv = $remote_servers_cache{$_[0]};
#        $serv || return &$remote_error_handler("No Webmin Servers entry for $_[0]");
#        }
#if ($serv->{'fast'} || !$_[0]) {
#        # Make TCP connection call to fastrpc.cgi
#        if (!$fast_fh_cache{$_[0]} && $_[0]) {
#                # Need to open the connection
#                local $con = &make_http_connection(
#                        $serv->{'host'}, $serv->{'port'}, $serv->{'ssl'},
#                        "POST", "/fastrpc.cgi");
#                return &$remote_error_handler(
#                    "Failed to connect to $serv->{'host'} : $con")
#                        if (!ref($con));
#                &write_http_connection($con, "Host: $serv->{'host'}\r\n");
#                &write_http_connection($con, "User-agent: Webmin\r\n");
#                local $auth = &encode_base64("$serv->{'user'}:$serv->{'pass'}");
#                $auth =~ s/\n//g;
#                &write_http_connection($con, "Authorization: basic $auth\r\n");
#                &write_http_connection($con, "Content-length: ",
#                                             length($tostr),"\r\n");
#                &write_http_connection($con, "\r\n");
#                &write_http_connection($con, $tostr);
#
#                # read back the response
#                local $line = &read_http_connection($con);
#                $line =~ s/\r|\n//g;
#                if ($line =~ /^HTTP\/1\..\s+401\s+/) {
#                        return &$remote_error_handler("Login to RPC server as $serv->{'user'} rejected");
#                        }
#                $line =~ /^HTTP\/1\..\s+200\s+/ || return &$remote_error_handler("HTTP error : $line");
#                do {
#                        $line = &read_http_connection($con);
#                        $line =~ s/\r|\n//g;
#                        } while($line);
#                $line = &read_http_connection($con);
#                if ($line =~ /^0\s+(.*)/) {
#                        return &$remote_error_handler("RPC error : $1");
#                        }
#                elsif ($line =~ /^1\s+(\S+)\s+(\S+)\s+(\S+)/ ||
#                       $line =~ /^1\s+(\S+)\s+(\S+)/) {
#                        # Started ok .. connect and save SID
#                        &close_http_connection($con);
#                        local ($port = $1, $sid = $2, $version = $3, $error);
#                        &open_socket($serv->{'host'}, $port, $sid, \$error);
#                        return &$remote_error_handler("Failed to connect to fastrpc.cgi : $error")
#                                if ($error);
#                        $fast_fh_cache{$_[0]} = $sid;
#                        $remote_server_version{$_[0]} = $version;
#                        }
#                else {
#                        while($stuff = &read_http_connection($con)) {
#                                $line .= $stuff;
#                                }
#                        return &$remote_error_handler("Bad response from fastrpc.cgi : $line");
#                        }
#                }
#        elsif (!$fast_fh_cache{$_[0]}) {
#                # Open the connection by running fastrpc.cgi locally
#                pipe(RPCOUTr, RPCOUTw);
#                if (!fork()) {
#                        untie(*STDIN);
#                        untie(*STDOUT);
#                        open(STDOUT, ">&RPCOUTw");
#                        close(STDIN);
#                        close(RPCOUTr);
#                        $| = 1;
#                        $ENV{'REQUEST_METHOD'} = 'GET';
#                        $ENV{'SCRIPT_NAME'} = '/fastrpc.cgi';
#                        local %acl;
#                        if ($base_remote_user ne 'root' &&
#                            $base_remote_user ne 'admin') {
#                                # Need to fake up a login for the CGI!
#                                &read_acl(undef, \%acl);
#                                $ENV{'BASE_REMOTE_USER'} =
#                                        $ENV{'REMOTE_USER'} =
#                                                $acl{'root'} ? 'root' : 'admin';
#                                }
#                        delete($ENV{'FOREIGN_MODULE_NAME'});
#                        delete($ENV{'FOREIGN_ROOT_DIRECTORY'});
#                        chdir($root_directory);
#                        exec("./fastrpc.cgi");
#                        print "exec failed : $!\n";
#                        exit 1;
#                        }
#                close(RPCOUTw);
#                local $line;
#                do {
#                        ($line = <RPCOUTr>) =~ s/\r|\n//g;
#                        } while($line);
#                $line = <RPCOUTr>;
#                #close(RPCOUTr);
#                if ($line =~ /^0\s+(.*)/) {
#                        return &$remote_error_handler("RPC error : $2");
#                        }
#                elsif ($line =~ /^1\s+(\S+)\s+(\S+)/) {
#                        # Started ok .. connect and save SID
#                        close(SOCK);
#                        local ($port = $1, $sid = $2, $error);
#                        &open_socket("localhost", $port, $sid, \$error);
#                        return &$remote_error_handler("Failed to connect to fastrpc.cgi : $error") if ($error);
#                        $fast_fh_cache{$_[0]} = $sid;
#                        }
#                else {
#                        &error("Bad line from fastrpc.cgi : $line");
#                        }
#                }
#        # Got a connection .. send off the request
#        local $fh = $fast_fh_cache{$_[0]};
#        local $tostr = &serialise_variable($_[1]);
#        print $fh length($tostr)," $fh\n";
#        print $fh $tostr;
#        local $rlen = int(<$fh>);
#        local ($fromstr, $got);
#        while(length($fromstr) < $rlen) {
#                return &$remote_error_handler("Failed to read from fastrpc.cgi")
#                        if (read($fh, $got, $rlen - length($fromstr)) <= 0);
#                $fromstr .= $got;
#                }
#        local $from = &unserialise_variable($fromstr);
#        if (defined($from->{'arv'})) {
#                return @{$from->{'arv'}};
#                }
#        else {
#                return $from->{'rv'};
#                }
#        }
#else {
#        # Call rpc.cgi on remote server
#        local $tostr = &serialise_variable($_[1]);
#        local $error = 0;
#        local $con = &make_http_connection($serv->{'host'}, $serv->{'port'},
#                                           $serv->{'ssl'}, "POST", "/rpc.cgi");
#        return &$remote_error_handler("Failed to connect to $serv->{'host'} : $con") if (!ref($con));
#
#        &write_http_connection($con, "Host: $serv->{'host'}\r\n");
#        &write_http_connection($con, "User-agent: Webmin\r\n");
#        local $auth = &encode_base64("$serv->{'user'}:$serv->{'pass'}");
#        $auth =~ s/\n//g;
#        &write_http_connection($con, "Authorization: basic $auth\r\n");
#        &write_http_connection($con, "Content-length: ",length($tostr),"\r\n");
#        &write_http_connection($con, "\r\n");
#        &write_http_connection($con, $tostr);
#
#        # read back the response
#        local $line = &read_http_connection($con);
#        $line =~ s/\r|\n//g;
#        if ($line =~ /^HTTP\/1\..\s+401\s+/) {
#                return &$remote_error_handler("Login to RPC server as $serv->{'user'} rejected");
#                }
#        $line =~ /^HTTP\/1\..\s+200\s+/ || return &$remote_error_handler("RPC HTTP error : $line");
#        do {
#                $line = &read_http_connection($con);
#                $line =~ s/\r|\n//g;
#                } while($line);
#        local $fromstr;
#        while($line = &read_http_connection($con)) {
#                $fromstr .= $line;
#                }
#        close(SOCK);
#        local $from = &unserialise_variable($fromstr);
#        return &$remote_error_handler("Invalid RPC login to $_[0]") if (!$from->{'status'});
#        if (defined($from->{'arv'})) {
#                return @{$from->{'arv'}};
#                }
#        else {
#                return $from->{'rv'};
#                }
#        }
#}
#
## serialise_variable(variable)
## Converts some variable (maybe a scalar, hash ref, array ref or scalar ref)
## into a url-encoded string
def _serialize_variable():
    raise NotImplementedError
#sub serialise_variable
#{
#if (!defined($_[0])) {
#        return 'UNDEF';
#        }
#local $r = ref($_[0]);
#local $rv;
#if (!$r) {
#        $rv = &urlize($_[0]);
#        }
#elsif ($r eq 'SCALAR') {
#        $rv = &urlize(${$_[0]});
#        }
#elsif ($r eq 'ARRAY') {
#        $rv = join(",", map { &urlize(&serialise_variable($_)) } @{$_[0]});
#        }
#elsif ($r eq 'HASH') {
#        $rv = join(",", map { &urlize(&serialise_variable($_)).",".
#                              &urlize(&serialise_variable($_[0]->{$_})) }
#                            keys %{$_[0]});
#        }
#elsif ($r eq 'REF') {
#        $rv = &serialise_variable(${$_[0]});
#        }
#return ($r ? $r : 'VAL').",".$rv;
#}
#
## unserialise_variable(string)
## Converts a string created by serialise_variable() back into the original
## scalar, hash ref, array ref or scalar ref.
def _unserialise_variable():
    raise NotImplementedError
#sub unserialise_variable
#{
#local @v = split(/,/, $_[0]);
#local ($rv, $i);
#if ($v[0] eq 'VAL') {
#        $rv = &un_urlize($v[1]);
#        }
#elsif ($v[0] eq 'SCALAR') {
#        local $r = &un_urlize($v[1]);
#        $rv = \$r;
#        }
#elsif ($v[0] eq 'ARRAY') {
#        $rv = [ ];
#        for($i=1; $i<@v; $i++) {
#                push(@$rv, &unserialise_variable(&un_urlize($v[$i])));
#                }
#        }
#elsif ($v[0] eq 'HASH') {
#        $rv = { };
#        for($i=1; $i<@v; $i+=2) {
#                $rv->{&unserialise_variable(&un_urlize($v[$i]))} =
#                        &unserialise_variable(&un_urlize($v[$i+1]));
#                }
#        }
#elsif ($v[0] eq 'REF') {
#        local $r = &unserialise_variable($v[1]);
#        $rv = \$r;
#        }
#elsif ($v[0] eq 'UNDEF') {
#        $rv = undef;
#        }
#return $rv;
#}

def other_groups(user):
    # FIXME check speed compared to perl function    
    """Returns a list of secondary groups a user is a member of
    unlike in perl, it doesn't us the webmin function "indexof"   
    """    
    usergrps=list()
    # as in perl, return nothing, when user is missing (may be exception/error would the better response)
    if not user:
        return usergrps
    import grp
    allgroups=grp.getgrall()    
    for g in allgroups:
        if user in g[3]:
            usergrps.append(g[2])
    return usergrps

def date_chooser_button(dayfield, monthfield, yearfield, formno=0):
    """Returns HTML for a date-chooser button"""
    if not dayfield or not monthfield or not yearfield:
        return ""
    return '<input type=button onClick=\'window.dfield = document.forms[%s].%s; window.mfield = document.forms[%s].%s;'\
        ' window.yfield = document.forms[%s].%s; window.open("%s/date_chooser.cgi?day="+escape(dfield.value)+"&month='\
        '"+escape(mfield.selectedIndex)+"&year="+yfield.value, "chooser",'\
        ' "toolbar=no,menubar=no,scrollbars=yes,width=250,height=225")\' value="...">\n' % \
            (formno,dayfield,formno,monthfield,formno,yearfield,gconfig.get('webprefix',''))
  
## help_file(module, file)
def _help_file():
    raise NotImplementedError
## Returns the path to a module's help file
#sub help_file
#{
#local $dir = "$root_directory/$_[0]/help";
#local $lang = "$dir/$_[1].$current_lang.html";
#local $def = "$dir/$_[1].html";
#return -r $lang ? $lang : $def;
#}
#
## seed_random()
def seed_random():
    raise NotImplementedError
## Seeds the random number generator, if needed
#sub seed_random
#{
#if (!$main::done_seed_random) {
#        if (open(RANDOM, "/dev/urandom")) {
#                local $buf;
#                read(RANDOM, $buf, 4);
#                close(RANDOM);
#                srand(time() ^ $$ ^ $buf);
#                }
#        else {
#                srand(time() ^ $$);
#                }
#        $main::done_seed_random = 1;
#        }
#}
#
## disk_usage_kb(directory)
def disk_usage_kb():
    raise NotImplementedError
## Returns the number of kb used by some directory and all subdirs
#sub disk_usage_kb
#{
#local $out = `du -sk \"$_[0]\"`;
#if ($?) {
#        $out = `du -s \"$_[0]\"`;
#        }
#return $out =~ /^([0-9]+)/ ? $1 : "???";
#}
#
## help_search_link(term, [ section, ... ] )
def help_search_link():
    raise NotImplementedError
## Returns HTML for a link to the man module for searching local and online
## docs for various search terms
#sub help_search_link
#{
#local %acl;
#&read_acl(\%acl, undef);
#if ($acl{$base_remote_user,'man'} || $acl{$base_remote_user,'*'}) {
#        local $for = &urlize(shift(@_));
#        return "<a href='$gconfig{'webprefix'}/man/search.cgi?".
#               join("&", map { "section=$_" } @_)."&".
#               "for=$for&exact=1&check=$module_name'>".
#               $text{'helpsearch'}."</a>\n";
#        }
#else {
#        return "";
#        }
#}
#
## make_http_connection(host, port, ssl, method, page)
def make_http_connection():
    raise NotImplementedError
## Opens a connection to some HTTP server, maybe through a proxy, and returns
## a handle object. The handle can then be used to send additional headers
## and read back a response. If anything goes wrong, returns an error string.
#sub make_http_connection
#{
#local $rv = { 'fh' => time().$$ };
#local $error;
#if ($_[2]) {
#        # Connect using SSL
#        eval "use Net::SSLeay";
#        $@ && &error($text{'link_essl'});
#        eval "Net::SSLeay::SSLeay_add_ssl_algorithms()";
#        eval "Net::SSLeay::load_error_strings()";
#        $rv->{'ssl_ctx'} = Net::SSLeay::CTX_new() ||
#                return "Failed to create SSL context";
#        $rv->{'ssl_con'} = Net::SSLeay::new($rv->{'ssl_ctx'}) ||
#                return "Failed to create SSL connection";
#        if ($gconfig{'http_proxy'} =~ /^http:\/\/(\S+):(\d+)/ &&
#            !&no_proxy($_[0])) {
#                &open_socket($1, $2, $rv->{'fh'}, \$error);
#                return $error if ($error);
#                local $fh = $rv->{'fh'};
#                print $fh "CONNECT $_[0]:$_[1] HTTP/1.0\r\n";
#                if ($gconfig{'proxy_user'}) {
#                        local $auth = &encode_base64(
#                           "$gconfig{'proxy_user'}:$gconfig{'proxy_pass'}");
#                        $auth =~ s/\r|\n//g;
#                        print $fh "Proxy-Authorization: Basic $auth\r\n";
#                        }
#                print $fh "\r\n";
#                local $line = <$fh>;
#                if ($line =~ /^HTTP(\S+)\s+(\d+)\s+(.*)/) {
#                        return "Proxy error : $3" if ($2 != 200);
#                        }
#                else {
#                        return "Proxy error : $line";
#                        }
#                $line = <$fh>;
#                }
#        else {
#                &open_socket($_[0], $_[1], $rv->{'fh'}, \$error);
#                return $error if ($error);
#                }
#        Net::SSLeay::set_fd($rv->{'ssl_con'}, fileno($rv->{'fh'}));
#        Net::SSLeay::connect($rv->{'ssl_con'}) ||
#                return "SSL connect() failed";
#        Net::SSLeay::write($rv->{'ssl_con'}, "$_[3] $_[4] HTTP/1.0\r\n");
#        }
#else {
#        # Plain HTTP request
#        local $error;
#        if ($gconfig{'http_proxy'} =~ /^http:\/\/(\S+):(\d+)/ &&
#            !&no_proxy($_[0])) {
#                &open_socket($1, $2, $rv->{'fh'}, \$error);
#                return $error if ($error);
#                local $fh = $rv->{'fh'};
#                print $fh "$_[3] http://$_[0]:$_[1]$_[4] HTTP/1.0\r\n";
#                if ($gconfig{'proxy_user'}) {
#                        local $auth = &encode_base64(
#                           "$gconfig{'proxy_user'}:$gconfig{'proxy_pass'}");
#                        $auth =~ s/\r|\n//g;
#                        print $fh "Proxy-Authorization: Basic $auth\r\n";
#                        }
#                }
#        else {
#                &open_socket($_[0], $_[1], $rv->{'fh'}, \$error);
#                return $error if ($error);
#                local $fh = $rv->{'fh'};
#                print $fh "$_[3] $_[4] HTTP/1.0\r\n";
#                }
#        }
#return $rv;
#}
#
## read_http_connection(handle, [amount])
def read_http_connection():
    raise NotImplementedError
## Reads either one line or up to the specified amount of data from the handle
#sub read_http_connection
#{
#local $h = $_[0];
#local $rv;
#if ($h->{'ssl_con'}) {
#        if (!$_[1]) {
#                local ($idx, $more);
#                while(($idx = index($h->{'buffer'}, "\n")) < 0) {
#                        # need to read more..
#                        if (!($more = Net::SSLeay::read($h->{'ssl_con'}))) {
#                                # end of the data
#                                $rv = $h->{'buffer'};
#                                delete($h->{'buffer'});
#                                return $rv;
#                                }
#                        $h->{'buffer'} .= $more;
#                        }
#                $rv = substr($h->{'buffer'}, 0, $idx+1);
#                $h->{'buffer'} = substr($h->{'buffer'}, $idx+1);
#                }
#        else {
#                if (length($h->{'buffer'})) {
#                        $rv = $h->{'buffer'};
#                        delete($h->{'buffer'});
#                        }
#                else {
#                        $rv = Net::SSLeay::read($h->{'ssl_con'}, $_[1]);
#                        }
#                }
#        }
#else {
#        if ($_[1]) {
#                read($h->{'fh'}, $rv, $_[1]) > 0 || return undef;
#                }
#        else {
#                local $fh = $h->{'fh'};
#                $rv = <$fh>;
#                }
#        }
#return $rv;
#}
#
## write_http_connection(handle, [data+])
def write_http_connection():
    raise NotImplementedError
## Writes the given data to the handle
#sub write_http_connection
#{
#local $h = shift(@_);
#local $fh = $h->{'fh'};
#if ($h->{'ssl_ctx'}) {
#        foreach (@_) {
#                Net::SSLeay::write($h->{'ssl_con'}, $_);
#                }
#        }
#else {
#        print $fh @_;
#        }
#}
#
## close_http_connection(handle)
def close_http_connection():
    raise NotImplementedError
#sub close_http_connection
#{
#close($h->{'fh'});
#}
#

UNCLEAN_ENV = os.environ.copy()

def clean_environment():
    """Deletes any environment variables inherited from miniserv so that they
    won't be passed to programs started by webmin."""
    
    for key in os.environ.keys():
        if key[0:5] == "HTTP_":
            del os.environ[key]

    for key in ['WEBMIN_CONFIG', 'SERVER_NAME', 'CONTENT_TYPE', 'REQUEST_URI',
                'PATH_INFO', 'WEBMIN_VAR', 'REQUEST_METHOD', 'GATEWAY_INTERFACE',
                'QUERY_STRING', 'REMOTE_USER', 'SERVER_SOFTWARE', 'SERVER_PROTOCOL',
                'REMOTE_HOST', 'SERVER_PORT', 'DOCUMENT_ROOT', 'SERVER_ROOT',
                'MINISERV_CONFIG', 'SCRIPT_NAME', 'SERVER_ADMIN', 'CONTENT_LENGTH',
                'HTTPS']:
        if (os.environ.has_key(key)):
            del os.environ[key]


## reset_environment()
def reset_environment():
    """Puts the environment back how it was before clean_environment()"""
    
    os.environ = UNCLEAN_ENV.copy()


webmin_feedback_address = "feedback\@webmin.com"

## progress_callback()
## Never called directly, but useful for passing to &http_download
#sub progress_callback
#{
#if ($_[0] == 2) {
#        # Got size
#        print $progress_callback_prefix;
#        if ($_[1]) {
#                $progress_size = $_[1];
#                $progress_step = int($_[1] / 10);
#                print textsub('progress_size', $progress_callback_url,
#                            $progress_size),"<br>\n";
#                }
#        else {
#                print textsub('progress_nosize', $progress_callback_url),"<br>\n";
#                }
#        }
#elsif ($_[0] == 3) {
#        # Got data update
#        local $sp = $progress_callback_prefix.("&nbsp;" x 5);
#        if ($progress_size) {
#                local $st = int(($_[1] * 10) / $progress_size);
#                print $sp,textsub('progress_data', $_[1], int($_[1]*100/$progress_size)),"<br>\n" if ($st != $progress_step);
#                $progress_step = $st;
#                }
#        else {
#                print $sp,textsub('progress_data2', $_[1]),"<br>\n";
#                }
#        }
#elsif ($_[0] == 4) {
#        # All done downloading
#        print $progress_callback_prefix,textsub('progress_done'),"<br>\n";
#        }
#elsif ($_[0] == 5) {
#        # Got new location after redirect
#        $progress_callback_url = $_[1];
#        }
#}
#

def switch_to_remote_user():
    """Changes the user and group of the current process to that of the unix user
    with the same name as the current webmin login, or fails if there is none.
    """
    global remote_user_info
    try:
        remote_user_info = pwd.getpwnam(remote_user)	
    except KeyError:
        error(" switch to user "+remote_user+" failed")
    if os.getuid()==0 and  remote_user_info:
        other_ugroups=other_groups(remote_user_info[0])
        other_ugroups.insert(0,remote_user_info[3])
        os.setgroups(other_ugroups)
        # Set real and effective user and group ids
        # in perl: ($>, $<) = ( $remote_user_info[2], $remote_user_info[2] );
        os.setregid(remote_user_info[3],remote_user_info[3])
        os.setreuid(remote_user_info[2],remote_user_info[2])
        
        os.environ['USER'] = remote_user
        os.environ['LOGNAME'] = remote_user 
        os.environ['HOME'] = remote_user_info[5]

def create_user_config_dirs():
    """ Creates per-user config directories and sets $user_config_directory and
    $user_module_config_directory to them. 
    Also reads per-user module configs into %userconfig
    Note: if switch_to_remote_user() is not called before this function
    nonexisting directories will be created with root ownership!
    -> they are then not writeable by usermin's uconfig.cgi
    """
    global user_config_directory,user_module_config_directory,userconfig
    
    if not gconfig.has_key('userconfig'): return
    if not remote_user_info:
        uinfo = pwd.getpwnam(remote_user)	
    else:
        uinfo = remote_user_info
    
    if not uinfo or not uinfo[5]: return
    
    user_config_directory = os.path.join(uinfo[5],gconfig['userconfig'])
    if not os.path.exists(user_config_directory):
        os.mkdir(user_config_directory,0755)
    if module_name:
        user_module_config_directory = os.path.join(user_config_directory,module_name)	
        if not os.path.exists(user_module_config_directory):
            os.mkdir(user_module_config_directory,0755)
        userconfig={}	
        read_file_cached(module_root_directory+os.sep+'defaultuconfig',userconfig)
        read_file_cached(module_config_directory+os.sep+'uconfig',userconfig)
        read_file_cached(user_module_config_directory+os.sep+'config',userconfig)

## filter_javascript(text)
def filter_javascript():
    raise NotImplementedError
## Disables all javascript <script>, onClick= and so on tags in the given HTML
#sub filter_javascript
#{
#local $rv = $_[0];
#$rv =~ s/<\s*script[^>]*>([\000-\377]*?)<\s*\/script\s*>//g;
#$rv =~ s/(on(Abort|Blur|Change|Click|DblClick|DragDrop|Error|Focus|KeyDown|KeyPress|KeyUp|Load|MouseDown|MouseMove|MouseOut|MouseOver|MouseUp|Move|Reset|Resize|Select|Submit|Unload)=)/x$1/g;
#return $rv;
#}
#
## resolve_links(path)
def resolve_links():
    raise NotImplementedError
## Given a path that may contain symbolic links, returns the real path
#sub resolve_links
#{
#local $path = $_[0];
#$path =~ s/\/+/\//g;
#$path =~ s/\/$// if ($path ne "/");
#local @p = split(/\/+/, $path);
#shift(@p);
#for($i=0; $i<@p; $i++) {
#        local $sofar = "/".join("/", @p[0..$i]);
#        local $lnk = readlink($sofar);
#        if ($lnk =~ /^\//) {
#                # Link is absolute..
#                return &resolve_links($lnk."/".join("/", @p[$i+1 .. $#p]));
#                }
#        elsif ($lnk) {
#                # Link is relative
#                return &resolve_links("/".join("/", @p[0..$i-1])."/".$lnk."/".join("/", @p[$i+1 .. $#p]));
#                }
#        }
#return $path;
#}
#
## same_file(file1, file2)
def same_file():
    raise NotImplementedError
## Returns 1 if two files are actually the same
#sub same_file
#{
#return 1 if ($_[0] eq $_[1]);
#return 0 if ($_[0] !~ /^\// || $_[1] !~ /^\//);
#local @stat1 = $stat_cache{$_[0]} ? @{$stat_cache{$_[0]}}
#                                  : (@{$stat_cache{$_[0]}} = stat($_[0]));
#local @stat2 = $stat_cache{$_[1]} ? @{$stat_cache{$_[1]}}
#                                  : (@{$stat_cache{$_[1]}} = stat($_[1]));
#return 0 if (!@stat1 || !@stat2);
#return $stat1[0] == $stat2[0] && $stat1[1] == $stat2[1];
#}
#
#1;  # return true?
#
