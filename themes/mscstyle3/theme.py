# -*- coding: iso-8859-1 -*-
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

from HTMLgen import *

# Choose if you use Usermin or Webmin
# IsUsermin=0 for Webmin, IsUsermin=1 for Usermin
# or IsUsermin="auto" for autodetection (default)
IsUsermin="auto"

# --- no need to change anything below ---

# try autodetect
if IsUsermin=="auto":
    try:
        if module_info and  module_info.get('usermin'):
            IsUsermin = 1
    except:
        IsUsermin=0

if IsUsermin == 1:
     available = ["usermin", "mail", "login", "apps", ""]
     pytheme_logo = "/usermin_logo.gif"
     pytheme_logo_link ="http://www.usermin.com/"
     pytheme_logo_alt = "Usermin homepage"
     module_infos_access=1
     noprefs = config.get("noprefs")     
     if noprefs==0 or noprefs=="0":
        noprefs=None
else:
     available = ["webmin", "system", "servers", "cluster", "hardware", 
                  "", "net", "kororaweb"]
     pytheme_logo = "/images/top_bar/webmin_logo.jpg"
     pytheme_logo_link ="http://www.webmin.com/"
     pytheme_logo_alt = "Webmin homepage"
     module_infos_access=0
     noprefs = None

letter_sizes = {
	'100.gif': [ 10, 16 ],
	'101.gif': [ 11, 16 ],
	'102.gif' : [ 6, 16 ],
	'103.gif' : [ 10, 16 ],
	'104.gif' : [ 9, 16 ],
	'105.gif' : [ 4, 16 ],
	'106.gif' : [ 5, 16 ],
	'107.gif' : [ 9, 16 ],
	'108.gif' : [ 4, 16 ],
	'109.gif' : [ 14, 16 ],
	'110.gif' : [ 9, 16 ],
	'111.gif' : [ 11, 16 ],
	'112.gif' : [ 10, 16 ],
	'113.gif' : [ 10, 16 ],
	'114.gif' : [ 6, 16 ],
	'115.gif' : [ 8, 16 ],
	'116.gif' : [ 6, 16 ],
	'117.gif' : [ 9, 16 ],
	'118.gif' : [ 10, 16 ],
	'119.gif' : [ 13, 16 ],
	'120.gif' : [ 10, 16 ],
	'121.gif' : [ 10, 16 ],
	'122.gif' : [ 8, 16 ],
	'123.gif' : [ 7, 16 ],
	'124.gif' : [ 4, 16 ],
	'125.gif' : [ 7, 16 ],
	'126.gif' : [ 9, 16 ],
	'177.iso-8859-2.gif' : [ 10, 16 ],
	'179.iso-8859-2.gif' : [ 7, 16 ],
	'182.iso-8859-2.gif' : [ 9, 16 ],
	'188.iso-8859-2.gif' : [ 9, 16 ],
	'191.iso-8859-2.gif' : [ 9, 16 ],
	'192.gif' : [ 12, 16 ],
	'193.gif' : [ 12, 16 ],
	'194.gif' : [ 11, 16 ],
	'195.gif' : [ 12, 16 ],
	'196.gif' : [ 12, 16 ],
	'197.gif' : [ 12, 16 ],
	'198.gif' : [ 13, 16 ],
	'199.gif' : [ 12, 16 ],
	'200.gif' : [ 7, 16 ],
	'201.gif' : [ 8, 16 ],
	'202.gif' : [ 8, 16 ],
	'203.gif' : [ 7, 16 ],
	'204.gif' : [ 6, 16 ],
	'205.gif' : [ 5, 16 ],
	'206.gif' : [ 7, 16 ],
	'207.gif' : [ 7, 16 ],
	'208.gif' : [ 11, 16 ],
	'208.iso-8859-9.gif' : [ 13, 16 ],
	'209.gif' : [ 10, 16 ],
	'210.gif' : [ 13, 16 ],
	'211.gif' : [ 13, 16 ],
	'211.iso-8859-2.gif' : [ 13, 16 ],
	'212.gif' : [ 12, 16 ],
	'213.gif' : [ 13, 16 ],
	'214.gif' : [ 13, 16 ],
	'214.iso-8859-9.gif' : [ 13, 16 ],
	'215.gif' : [ 9, 16 ],
	'216.gif' : [ 13, 16 ],
	'217.gif' : [ 9, 16 ],
	'218.gif' : [ 9, 16 ],
	'219.gif' : [ 9, 16 ],
	'220.gif' : [ 9, 16 ],
	'220.iso-8859-9.gif' : [ 9, 16 ],
	'221.gif' : [ 11, 16 ],
	'221.iso-8859-9.gif' : [ 5, 16 ],
	'222.gif' : [ 9, 16 ],
	'222.iso-8859-9.gif' : [ 11, 16 ],
	'223.gif' : [ 9, 16 ],
	'224.gif' : [ 10, 16 ],
	'225.gif' : [ 10, 16 ],
	'226.gif' : [ 11, 16 ],
	'227.gif' : [ 10, 16 ],
	'228.gif' : [ 10, 16 ],
	'229.gif' : [ 11, 16 ],
	'230.gif' : [ 16, 16 ],
	'230.iso-8859-2.gif' : [ 9, 16 ],
	'231.gif' : [ 10, 16 ],
	'231.iso-8859-9.gif' : [ 10, 16 ],
	'231.iso.8859-9.gif' : [ 10, 16 ],
	'232.gif' : [ 11, 16 ],
	'233.gif' : [ 11, 16 ],
	'234.gif' : [ 11, 16 ],
	'234.iso-8859-2.gif' : [ 9, 16 ],
	'235.gif' : [ 11, 16 ],
	'236.gif' : [ 6, 16 ],
	'237.gif' : [ 6, 16 ],
	'238.gif' : [ 6, 16 ],
	'239.gif' : [ 7, 16 ],
	'240.gif' : [ 10, 16 ],
	'240.iso-8859-9.gif' : [ 10, 16 ],
	'241.gif' : [ 9, 16 ],
	'241.iso-8859-2.gif' : [ 9, 16 ],
	'242.gif' : [ 11, 16 ],
	'243.gif' : [ 11, 16 ],
	'243.iso-8859-2.gif' : [ 11, 16 ],
	'244.gif' : [ 11, 16 ],
	'245.gif' : [ 11, 16 ],
	'246.gif' : [ 11, 16 ],
	'246.iso-8859-9.gif' : [ 11, 16 ],
	'247.gif' : [ 9, 16 ],
	'248.gif' : [ 10, 16 ],
	'249.gif' : [ 9, 16 ],
	'250.gif' : [ 9, 16 ],
	'251.gif' : [ 9, 16 ],
	'252.gif' : [ 9, 16 ],
	'252.iso-8859-9.gif' : [ 9, 16 ],
	'253.gif' : [ 10, 16 ],
	'253.iso-8859-9.gif' : [ 5, 16 ],
	'254.gif' : [ 10, 16 ],
	'255.gif' : [ 9, 16 ],
	'32.gif' : [ 6, 16 ],
	'33.gif' : [ 4, 16 ],
	'34.gif' : [ 7, 16 ],
	'35.gif' : [ 9, 16 ],
	'36.gif' : [ 8, 16 ],
	'37.gif' : [ 13, 16 ],
	'38.gif' : [ 11, 16 ],
	'39.gif' : [ 3, 16 ],
	'40.gif' : [ 6, 16 ],
	'41.gif' : [ 6, 16 ],
	'42.gif' : [ 7, 16 ],
	'43.gif' : [ 9, 16 ],
	'44.gif' : [ 4, 16 ],
	'45.gif' : [ 6, 16 ],
	'46.gif' : [ 4, 16 ],
	'47.gif' : [ 7, 16 ],
	'48.gif' : [ 9, 16 ],
	'49.gif' : [ 6, 16 ],
	'50.gif' : [ 9, 16 ],
	'51.gif' : [ 9, 16 ],
	'52.gif' : [ 10, 16 ],
	'53.gif' : [ 9, 16 ],
	'54.gif' : [ 10, 16 ],
	'55.gif' : [ 8, 16 ],
	'56.gif' : [ 9, 16 ],
	'57.gif' : [ 10, 16 ],
	'58.gif' : [ 5, 16 ],
	'59.gif' : [ 4, 16 ],
	'60.gif' : [ 9, 16 ],
	'61.gif' : [ 10, 16 ],
	'62.gif' : [ 10, 16 ],
	'63.gif' : [ 9, 16 ],
	'64.gif' : [ 12, 16 ],
	'65.gif' : [ 12, 16 ],
	'66.gif' : [ 9, 16 ],
	'67.gif' : [ 12, 16 ],
	'68.gif' : [ 10, 16 ],
	'69.gif' : [ 7, 16 ],
	'70.gif' : [ 7, 16 ],
	'71.gif' : [ 13, 16 ],
	'72.gif' : [ 9, 16 ],
	'73.gif' : [ 5, 16 ],
	'74.gif' : [ 8, 16 ],
	'75.gif' : [ 9, 16 ],
	'76.gif' : [ 8, 16 ],
	'77.gif' : [ 12, 16 ],
	'78.gif' : [ 10, 16 ],
	'79.gif' : [ 12, 16 ],
	'80.gif' : [ 9, 16 ],
	'81.gif' : [ 13, 16 ],
	'82.gif' : [ 9, 16 ],
	'83.gif' : [ 9, 16 ],
	'84.gif' : [ 8, 16 ],
	'85.gif' : [ 9, 16 ],
	'86.gif' : [ 11, 16 ],
	'87.gif' : [ 14, 16 ],
	'88.gif' : [ 11, 16 ],
	'89.gif' : [ 11, 16 ],
	'90.gif' : [ 9, 16 ],
	'91.gif' : [ 5, 16 ],
	'93.gif' : [ 6, 16 ],
	'94.gif' : [ 9, 16 ],
	'95.gif' : [ 9, 16 ],
	'96.gif' : [ 6, 16 ],
	'97.gif' : [ 11, 16 ],
	'98.gif' : [ 10, 16 ],
	'99.gif' : [ 10, 16 ] }


def theme_header(title, image=None, help=None, config=None, nomodule=None, nowebmin=None,
                 rightside="", header=None, body=None, below=None):
    acl = read_acl()

    for l in list_languages():
        if l["lang"] == current_lang:
            lang = l    

    if force_charset:
        charset = force_charset
    elif lang.has_key("charset"):
        charset = lang["charset"]
    else:
        charset = "iso-8859-1"    

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
    
    print "<link rel='icon' href='images/webmin_icon.png' type='image/png'>"

    if gconfig.get("sysinfo") == 1:
        print "<title>%s : %s on %s (%s %s)</title>" % \
              (title, remote_user, get_system_hostname(), os_type, os_version)
    else:
        print "<title>%s</title>" % title

    if header:
        print header

    # Where does gconfig["sysinfo"] come from? 
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

    msc_modules = get_all_module_infos(module_infos_access)

    print "</head>"

    if theme_no_table:
        print '<body bgcolor="#6696bc" link="#000000" vlink="#000000" text="#000000" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0" ', body, '>'

    else:
        print '<body bgcolor="#6696bc" link="#000000" vlink="#000000" text="#000000" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0" ', body, '>'
        

    if None != session_id:
        logout = "/session_login.cgi?logout=1"
        loicon = "logout.jpg"
        lowidth = 84
        lotext = text["main_logout"]
    else:
        logout = "switch_user.cgi"
        loicon = "switch.jpg"
        lowidth = 27
        lotext = text["main_switch"]

    top_table = TableLite(width="100%", border="0", cellspacing="0",
                          cellpadding="0", background="/images/top_bar/bg.jpg",
                          height="32")
    t_body = TR()
    TDList = [TD(IMG("/images/top_bar/left.jpg", height=32),
                 width=4, nowrap="nowrap"),
              TD(Href(pytheme_logo_link,
                      IMG(pytheme_logo, width=99,
                          height=32,
                          border="0", alt=pytheme_logo_alt)),
                 width="100%", nowrap="nowrap")]

    if not os.environ.has_key("ANONYMOUS_USER"):
        # XXX: acl.get("feedback") might not be correct
        if gconfig.get("nofeedbackcc") != 2 and acl.get("feedback"):
            TDList.append(TD(Href("/feedback_form.cgi?module=%s" % module_name,
                                  IMG("/images/top_bar/feedback.jpg", width=97,
                                      height=32,
                                      border="0", alt=text["feedback"]))))
            TDList.append(TD(IMG("/images/top_bar/top_sep.jpg", width=12,
                                 height=32)))

        TDList.append(TD(Href(logout,
                              IMG("/images/top_bar/"+loicon, width=lowidth,
                                  height=32,
                                  alt=lotext, border="0"))))

    TDList.append(TD(Div(IMG("/images/top_bar/right.jpg", width=3, height=32)),
                     width="3"))

    
    top_table.append(t_body + TDList)

    print top_table

    cat_top_table = TableLite(width="100%", border="0", cellspacing="0",
                           cellpadding="0", height="7")

    
    cat_top_table.append(TR(TD(IMG("/images/top_bar/shadow.jpg",width=8, height=7),
                           background="/images/top_bar/shadow_bg.jpg",
                           nowrap="nowrap")))

    print cat_top_table


    catnames = read_file(os.path.join(config_directory, "webmin.catnames"))
    cats = {}

    for module in msc_modules:
        c = module.get("category", "")
        if cats.has_key(c):
            continue
        if catnames.has_key(c):
            cats[c] = catnames[c]
        elif text.has_key("category_%s" % c):
            cats[c] = text["category_%s" % c]
        else:
            mtext = load_language(module["dir"])
            if mtext.has_key("category_%s" % c):
                cats[c] = mtext["category_%s" % c]
            else:
                c = ""
                module["category"] = ""
                cats[c] = text["category_%s" % c]
    sorted_cats = cats.keys()
    sorted_cats.sort()
    sorted_cats.reverse()

    if 0 == len(cats):
        per = 100
    else:
        per = 100.0 / float(len(cats))

    ## Navigation Bar START ##

    nav_table = TableLite(width="100%", border="0", cellspacing="0",
                          cellpadding="0", height="57",
                          background="/images/nav/bg.jpg")

    nav_table_body = TR(background="/images/nav/bg.jpg")

    TDList = [TD(IMG("/images/nav/left.jpg", width=3, height=57),
                 width="6", nowrap="nowrap")]

    for cat in sorted_cats:
        uri = "/?cat=%s" % cat
        cont = Container()
        if cat in available:
            if "" == cat:
                cont.append(IMG("/images/cats/others.jpg", width=43, height=44,
                                        border="0", alt=cat))
            else:
                cont.append(IMG("/images/cats/%s.jpg" % cat, width=43, height=44,
                                border="0", alt=cat))

        else:
            cont.append(IMG("/images/cats/unknown.jpg", width=43, height=44,
                            border="0", alt=cat))

        cont.append(BR())
        cont.append(chop_font(cats[cat]))
                
        TDList.append(TD(Center(Href(uri, cont)), nowrap="nowrap"))
        TDList.append(TD(IMG("/images/nav/sep.jpg", width=17, height=57),
                         width=17))

    TDList.append(TD(Container('&nbsp;'), nowrap="nowrap", width="100%"))

    nav_table.append(nav_table_body + TDList)

    # UGLY!
    # The reason we replace all "\n" with "" is that Mozilla
    # won't render the menu correctly otherwise. GAAAAH!
    
    print str(nav_table).replace("\n", "")

    nav_under_table = TableLite(width="100%", border="0", cellspacing="0",
                                cellpadding="0",
                                background="/images/nav/bottom_bg.jpg",
                                height="4")

    nav_under_table.append(TR()+[TD(IMG("/images/nav/bottom_left.jpg",
                                        width=3, height=4), width="100%")])

    print nav_under_table

    tab_under_modcats = TableLite(width="100%", border="0",
                                  cellspacing="0", cellpadding="0",
                                  background="/images/nav/bottom_shadow2.jpg")

    # ---new/changed display (user) preference tab
    tab_under_modcats_prefs=None
    tab_under_modcats_help=None
    if help:        
        if type(help) == types.ListType:
            helplink =  hlink(text["header_help"], help[0], help[1])
        else:
            helplink = hlink(text["header_help"], help)
        tab_under_modcats_help = TableLite(border="0",cellspacing="0", cellpadding="0")
        tab_under_modcats_help.append(TR() + [TD(IMG("/images/tabs/left.jpg", width=12, height="21"),background="/images/tabs/bg.jpg")]+\
                                [TD(Code(helplink),background="/images/tabs/bg.jpg")]+\
                                [TD(IMG("/images/tabs/right.jpg", width=15, height="21"),background="/images/tabs/bg.jpg")])    
        tab_under_modcats_help.append(TR() + [TD(IMG("/images/tabs/right_bottom.jpg", width=12, height="4"))]+\
                                [TD(IMG("/images/tabs/bottom.jpg", width=17, height="4"),background="/images/tabs/bottom.jpg")]+\
                                [TD(IMG("/images/tabs/left_bottom.jpg", width=15, height="4"))])    


    
    if config:
        access = get_module_acl();
        if not access.get("noconfig") and not noprefs:
            if user_module_config_directory:
                cprog = "uconfig.cgi"
            else:
                cprog = "config.cgi"            
    
            uri='%s/%s?%s' % (gconfig.get("webprefix", ""), cprog, module_name)	    
            tab_under_modcats_prefs = TableLite(border="0",cellspacing="0", cellpadding="0")
            tab_under_modcats_prefs.append(TR() + [TD(IMG("/images/tabs/left.jpg", width=12, height="21"),background="/images/tabs/bg.jpg")]+\
                                    [TD(Href(uri,text["header_config"]),background="/images/tabs/bg.jpg")]+\
                                    [TD(IMG("/images/tabs/right.jpg", width=15, height="21"),background="/images/tabs/bg.jpg")])    
            tab_under_modcats_prefs.append(TR() + [TD(IMG("/images/tabs/right_bottom.jpg", width=12, height="4"))]+\
                                    [TD(IMG("/images/tabs/bottom.jpg", width=17, height="4"),background="/images/tabs/bottom.jpg")]+\
                                    [TD(IMG("/images/tabs/left_bottom.jpg", width=15, height="4"))])    

    tab_under_modcats_inner = TableLite(width="100%", border="0",
                                  cellspacing="0", cellpadding="0",
                                  background="/images/nav/bottom_shadow2.jpg")
    tab_under_modcats_inner.append(TR() + [TD(IMG("/images/nav/bottom_shadow.jpg", width=43, height="9"))])
    if tab_under_modcats_help or tab_under_modcats_prefs:
        tabTR = TR()
        if tab_under_modcats_help:
            tabTR = tabTR + [TD(tab_under_modcats_help)]
        if tab_under_modcats_prefs:
            tabTR = tabTR + [TD(tab_under_modcats_prefs)]
        tabTR = tabTR + [TD(tab_under_modcats_inner,background="/images/nav/bottom_shadow2.jpg",width="100%",nowrap="nowarp",valign="top")]
        tab_under_modcats(tabTR)
        # tab_under_modcats.append(TR() + [TD(tab_under_modcats_prefs)]+ [TD(tab_under_modcats_inner,background="/images/nav/bottom_shadow2.jpg",width="100%",nowrap="nowarp",valign="top")])	
    else:
        tab_under_modcats.append(TR() + [TD(IMG("/images/nav/bottom_shadow.jpg", width=43, height="9"))])    
    print tab_under_modcats

    print "<br>"
    # ----end new display (user) preference tab


    if not nowebmin:
        title = title.replace("&auml;", "ä")
        title = title.replace("&ouml;", "ö")
        title = title.replace("&uuml;", "ü")
        title = title.replace("&nbsp;", " ")

        title_table = TableLite(border=0, cellpadding=0, cellspacing=0,
                                width="95%", align="center")
        inr_tt = TableLite(border=0, cellpadding=0, cellspacing=0, height=20)
        inr_tt_body = TR()
        inr_tt_TDList = [TD(IMG("/images/tabs/blue_left.jpg", width=13,
                                height=22), bgcolor="#bae3ff"),
                         TD(Strong(title), bgcolor="#bae3ff"),
                         TD(IMG("/images/tabs/blue_right.jpg", width=13,
                                height=22), bgcolor="#bae3ff")]
        inr_tt.append(inr_tt_body + inr_tt_TDList)
        title_table.append(TR(TD(inr_tt)))

        print title_table

        theme_prebody()

def theme_prebody():
    print "<table border=0 width=\"95%\" align=\"center\" cellspacing=0 cellpadding=0><tr><td bgcolor=#ffffff>\n";
    print "<table border=0 width=\"95%\" align=\"center\" cellspacing=0 cellpadding=0><tr><td>\n";

def theme_footer(links, noendbody=None):
    print "</table></table>"

    foot_table = TableLite(border=0, width="100%", align="center",
                           cellspacing=0, cellpadding=0, bgcolor="#6696bc")
    cont = Container()

    for i in range(len(links)):
        uri, uritxt = links[i]
        if "/" == uri:
            uri = "/?cat=%s" % module_info["category"]
        elif "" == uri and module_name:
            uri = "/%s" % module_name
        elif "?" == uri[0] and module_name:
            uri = "/%s/%s" % (module_name, uri)
        if 0 == i:
            cont.append("&nbsp;",
                             Href(uri, IMG("/images/arrow.jpg",
                                           align="middle", border="0",
                                           alt="<-")))
        else:
            cont.append("&nbsp;")

        cont.append("&nbsp;", Href(uri, textsub("main_return", uritxt)))

    foot_table.append(TR(TD(cont)))

    print foot_table
                    


def chop_font(s):
    if gconfig.get("texttitles"):
        return s

    cont = Container()
    for char in s:
        ll = ord(char)
        gif = "%s.gif" % ll
        sz = letter_sizes.get(gif, [0, 0])
        alt=char
        if " " == char:
            alt = "&nbsp;"
        cont.append(IMG("/images/letters2/%s" % gif,
                        width=sz[0], height=sz[1], alt=char, border="0",
                        align="bottom"))

    return cont
