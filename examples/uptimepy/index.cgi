#!/usr/bin/env python2
# -*-Python-*-

print "Content-type: text/html\n"

import sys
sys.path.append("..")
sys.stderr = sys.stdout
import webmin
import uptimelib

webmin.header("Uptime demo (Python)", config=1, nomodule=1)

#print "Content-type: text/html\n"
#print "XXXXXXXXXXXXXXX"

#uptimelib.somefunction()

webmin.footer([("/", "index")])

print "done"
