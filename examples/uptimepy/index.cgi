#!/usr/bin/env python2
# -*-Python-*-

import sys
sys.path.append("..")
sys.stderr = sys.stdout # Send errors to browser
import webmin
import uptimelib

webmin.header("Uptime demo (Python)", config=1, nomodule=1)
print "<hr>"

print "<h3>System uptime</h3>"
uptimelib.print_uptime()
print "<br><br>"

webmin.footer([("/", "index")])

