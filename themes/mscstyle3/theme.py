
#
# Python implementation of the mscstyle3 theme
#

# theme_prebody - called just before the main body of every page, so
# it can print any HTML it likes.
#
# theme_postbody - called just after the main body of every page.
#
# theme_header - called instead of the normal header function, with
# the same parameters. You could use this to re-write the header
# function in your own style with help and index links whereever you
# want them.
#
# theme_footer - called instead of the footer function with the same
# parameters.
#
# theme_error - called instead of the error function, with the same parameters.


def theme_header(title, image=None, help=None, config=None, nomodule=None, nowebmin=None,
                 rightside="", header=None, body=None, below=None):
    available = ["webmin", "system", "servers", "cluster", "hardware", "", "net", "kororaweb"]
    acl = read_acl()
    
    print "<!doctype html public \"-//W3C//DTD HTML 3.2 Final//EN\">"
    print "<html>"

    if gconfig.has_key("real_os_type"):
        os_type = gconfig["real_os_type"]
    else:
        os_type = gconfig["os_type"]

    if gconfig.has_key("real_os_version"):
        os_version = gconfig["real_os_version"]
    else:
        os_version = gconfig["os_version"]

    print "<head>"
    print "<link rel='icon' href='images/webmin_icon.png' type='image/png'>"

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

    risk = gconfig.get("risk_" + base_remote_user)
    for minfo in get_all_module_infos():
        if not check_os_support(minfo): continue
        if risk:
            # Check module risk level
            if risk != "high" and minfo.get("risk") and (minfo.get("risk").find(risk) == -1):
                continue
            else:
                # Check specific ACL
                pass
#                next if (!$acl{$base_remote_user,$minfo->{'dir'}} &&
#                         !$acl{$base_remote_user,"*"});
#                }
#        push(@msc_modules, $minfo);
#        }
#@msc_modules = sort { $a->{'desc'} cmp $b->{'desc'} } @msc_modules;
#
#if ($theme_no_table) {
#        print '<body bgcolor=#6696bc link=#000000 vlink=#000000 text=#000000 leftmargin="0" topmargin="0" marginwidth="0" marginheight="0" '.$_[8].'>';
#        }
#else {
#        print '<body bgcolor=#6696bc link=#000000 vlink=#000000 text=#000000 leftmargin="0" topmargin="0" marginwidth="0" marginheight="0" '.$_[8].'>';
#        }
#
#if ($remote_user && @_ > 1) {
#        # Show basic header with webmin.com link and logout button
#        local $logout = $main::session_id ? "/session_login.cgi?logout=1"
#                                          : "/switch_user.cgi";
#        print qq~<table width="100%" border="0" cellspacing="0" cellpadding="0" background="/images/top_bar/bg.jpg" height="32">
#          <tr>
#            <td width="4" nowrap><img src="/images/top_bar/left.jpg" width="4" height="32"></td>
#            <td width="100%" nowrap><a href="http://www.webmin.com"><img src="/images/top_bar/webmin_logo.jpg" width="99" height="32" border="0" alt="Webmin home page"></a></td>
#            <td><a href='/feedback_form.cgi?module=$module_name'><img src=/images/top_bar/feedback.jpg alt="$text{'main_feedback'}" border=0></a></td>
#            <td><img src=/images/top_bar/top_sep.jpg></td>
#            <td width="84" nowrap><a href='$logout'><img src="/images/top_bar/logout.jpg" width="84" height="31" border="0" alt="$text{'main_logout'}"></a></td>
#            <td width="3" nowrap>
#              <div align="right"><img src="/images/top_bar/right.jpg" width="3" height="32"></div>
#            </td>
#          </tr>
#        </table>~;
#        }
#
#local $one = @{$uacl{$base_remote_user}} == 1 && $gconfig{'gotoone'};
#if (@_ > 1 && !$one && $remote_user) {
#    # Display module categories
#    print qq~<table width="100%" border="0" cellspacing="0" cellpadding="0" height="7">
#  <tr>
#    <td background="/images/top_bar/shadow_bg.jpg" nowrap><img src="/images/top_bar/shadow.jpg" width="8" height="7"></td>
#  </tr>
#</table>~;
#
#    &read_file("$config_directory/webmin.catnames", \%catnames);
#    foreach $m (@msc_modules) {
#        $c = $m->{'category'};
#        next if ($cats{$c});
#        if (defined($catnames{$c})) {
#            $cats{$c} = $catnames{$c};
#            }
#        elsif ($text{"category_$c"}) {
#            $cats{$c} = $text{"category_$c"};
#            }
#        else {
#            # try to get category name from module ..
#            local %mtext = &load_language($m->{'dir'});
#            if ($mtext{"category_$c"}) {
#                $cats{$c} = $mtext{"category_$c"};
#                }
#            else {
#                $c = $m->{'category'} = "";
#                $cats{$c} = $text{"category_$c"};
#                }
#            }
#        }
#    @cats = sort { $b cmp $a } keys %cats;
#    $cats = @cats;
#    $per = $cats ? 100.0 / $cats : 100;
#
#    if ($theme_index_page) {
#            if (!defined($in{'cat'})) {
#               
#                # Use default category
#                if (defined($gconfig{'deftab'}) &&
#                    &indexof($gconfig{'deftab'}, @cats) >= 0) {
#                    $in{'cat'} = $gconfig{'deftab'};
#                    }
#                else {
#                    $in{'cat'} = $cats[0];
#                    }
#                }
#            elsif (!$cats{$in{'cat'}}) {
#                $in{'cat'} = "";
#                }
#    }
#
######Navigation Bar START#####
#    print qq~<table width="100%" border="0" cellspacing="0" cellpadding="0" height="57" background="/images/nav/bg.jpg">
#  <tr background="/images/nav/bg.jpg">
#    <td width="6" nowrap><img src="/images/nav/left.jpg" width="3" height="57"></td>~;
#
#    foreach $c (@cats) {
#        $t = $cats{$c};
#           $inlist    = "false";
#           foreach $testet (@available) {
#               if ($testet eq $c) {
#                $inlist = "true";
#               } 
#            }
#        if ($in{'cat'} eq $c && $theme_index_page) {
#           if ($inlist eq "true") {
#
#              if ($c eq "") {
#                print qq~<td nowrap><center><img src="/images/cats_over/others.jpg" width="43" height="44"><br>~;
#            &chop_font;
#
#                          print qq~</center></td>
#    <td width="17" nowrap><img src="/images/nav/sep.jpg" width="17" height="57"></td>~; 
#              } elsif ($c eq "webmin") {
#               if (@_ > 1) {
#               print qq~<td nowrap><center><a href=/?cat=$c><img src="/images/cats_over/$c.jpg" width="43" height="44" border=0><br>~;
#            &chop_font;
#                          print qq~</a></center></td>
#    <td width="17" nowrap><img src="/images/nav/sep.jpg" width="17" height="57"></td>~;
#                } else {
#               print qq~<td nowrap><center><img src="/images/cats_over/$c.jpg" width="43" height="44" border=0><br>~;            &chop_font;
#                          print qq~</center></td>
#    <td width="17" nowrap><img src="/images/nav/sep.jpg" width="17" height="57"></td>~;
#                }
#               } else {
#               print qq~<td nowrap><center><img src="/images/cats_over/$c.jpg" width="43" height="44"><br>~;
#
#            &chop_font;
#
#               print qq~</center></td>
#    <td width="17" nowrap><img src="/images/nav/sep.jpg" width="17" height="57"></td>~;
#              }
#
#        } else {
#            print qq~<td nowrap><center><img src="/images/cats_over/unknown.jpg" width="43" height="44"><br>~;
#
#            &chop_font;
#
#            print qq~</center></td>
#    <td width="17" nowrap><img src="/images/nav/sep.jpg" width="17" height="57"></td>~;
#           }
#        }
#        else {
#            if ($inlist eq "true") {
#              if ($c eq "") {
#                print qq~<td nowrap><center><a href=/?cat=$c><img src="/images/cats/others.jpg" width="43" height="44" border=0 alt=$c><br>~;
#
#            &chop_font;
#
#                print qq~</a></center></td>
#    <td width="17" nowrap><img src="/images/nav/sep.jpg" width="17" height="57"></td>~; 
#              } else {
#               print qq~<td nowrap><a href=/?cat=$c><center><img src="/images/cats/$c.jpg" width="43" height="44" border=0 alt=$c><br>~;
#
#            &chop_font;
#
#               print qq~</a></center></td>
#    <td width="17" nowrap><img src="/images/nav/sep.jpg" width="17" height="57"></td>~;
#              }
#        } else {
#            print qq~<td nowrap><center><a href=/?cat=$c><img src="/images/cats/unknown.jpg" width="43" height="44" border=0 alt=$c><br>~;
#
#            &chop_font;
#
#            print qq~</a></center></td>
#    <td width="17" nowrap><img src="/images/nav/sep.jpg" width="17" height="57"></td>~;
#        }
#           
#            }
#        }
#
#    print qq~<td width="100%" nowrap>&nbsp;</td>
#    <td nowrap>&nbsp;</td>
#  </tr>
#</table>~;
#    print qq~<table width="100%" border="0" cellspacing="0" cellpadding="0" background="/images/nav/bottom_bg.jpg" height="4">
#  <tr>
#    <td width="100%"><img src="/images/nav/bottom_left.jpg" width="3" height="4"></td>
#  </tr>
#</table>~;
#   }
#
#if (@_ > 1 && (!$_[5] || $ENV{'HTTP_WEBMIN_SERVERS'})) {
#   # Show tabs under module categories
#   print qq~<table width="100%" border="0" cellspacing="0" cellpadding="0" background="/images/nav/bottom_shadow2.jpg"> <tr background="/images/nav/bottom_shadow2.jpg">~;
#
#   if ($ENV{'HTTP_WEBMIN_SERVERS'}) {
#        &tab_start();
#        print "<a href='$ENV{'HTTP_WEBMIN_SERVERS'}'>",
#              "$text{'header_servers'}</a><br>"
#        &tab_end();
#        }
#        if (!$_[4]) { &tab_start; print "<a href=\"/$module_name/\">",
#                            "$text{'header_module'}</a>"; &tab_end;}
#        if (ref($_[2]) eq "ARRAY") {
#                &tab_start; print &hlink($text{'header_help'}, $_[2]->[0], $_[2]->[1]); &tab_end;
#                }
#        elsif (defined($_[2])) {
#                &tab_start; print &hlink($text{'header_help'}, $_[2]); &tab_end;
#                }
#        if ($_[3]) {
#                local %access = &get_module_acl();
#                if (!$access{'noconfig'}) {
#                        &tab_start; print "<a href=\"/config.cgi?$module_name\">",
#                              $text{'header_config'},"</a>"; &tab_end;
#                        }
#                }
#
#    foreach $t (split(/<br>/, $_[6])) {
#      if ($t =~ /\S/) {
#              &tab_start; print $t; &tab_end;
#      }
#    }
#
#print qq~
#    <td nowrap width="100%" background="/images/nav/bottom_shadow2.jpg" valign="top">
#
#      <table width="100%" border="0" cellspacing="0" cellpadding="0" background="/images/nav/bottom_shadow2.jpg">
#        <tr>
#          <td><img src="/images/nav/bottom_shadow.jpg" width="43" height="9"></td>
#        </tr>
#      </table>
#
#
#    </td>
#  </tr>
#</table>~;
#
#    if (!$_[5]) {
#            # Show page title in tab
#            local $title = $_[0];
#            $title =~ s/&auml;/ä/g;
#            $title =~ s/&ouml;/ö/g;
#            $title =~ s/&uuml;/ü/g;
#            $title =~ s/&nbsp;/ /g;
#
#            print "<p><table border=0 cellpadding=0 cellspacing=0 width=95% align=center><tr><td><table border=0 cellpadding=0 cellspacing=0 height=20><tr>"
#            print "<td bgcolor=#bae3ff>",
#              "<img src=/images/tabs/blue_left.jpg alt=\"\">","</td>"
#            print "<td bgcolor=#bae3ff>&nbsp;<b>$title</b>&nbsp;</td>"
#            print "<td bgcolor=#bae3ff>",
#              "<img src=/images/tabs/blue_right.jpg alt=\"\">","</td>"
#            if ($_[9]) {
#                print "</tr></table></td> <td align=right><table border=0 cellpadding=0 cellspacing=0 height=20><tr>"
#                print "<td bgcolor=#bae3ff>",
#                      "<img src=/images/tabs/blue_left.jpg alt=\"\">","</td>"
#                print "<td bgcolor=#bae3ff>&nbsp;<b>$_[9]</b>&nbsp;</td>"
#                print "<td bgcolor=#bae3ff>",
#                      "<img src=/images/tabs/blue_right.jpg alt=\"\">","</td>"
#                }
#            print "</tr></table></td></tr></table>"; 
#
#             &theme_prebody;
#        }
#    } elsif (@_ > 1) {
#            print qq~<table width="100%" border="0" cellspacing="0" cellpadding="0" background="/images/nav/bottom_shadow.jpg">
#          <tr>
#            <td width="100%" nowrap><img src="/images/nav/bottom_shadow.jpg" width="43" height="9"></td>
#          </tr>
#        </table><br>~;
#    }
#@header_arguments = @_;
#}
