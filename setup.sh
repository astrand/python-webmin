#!/bin/sh

PATH=$PATH:/usr/local/bin
for binary in python python2 python2.0 python2.1 python2.2 python2.3 python2.4 python2.5; do
    if $binary -c "" ; then
        $binary - <<EOF
import sys
sitedirs = filter(lambda s: s.endswith("site-packages"), sys.path)
if len(sitedirs) < 1:
    sys.exit("Unable to find a site-packages directory in sys.path")
filename = sitedirs[0] + "/python-webmin.pth"
open(filename, "w").write("/opt/python-webmin\n")
print "Created", filename
EOF
    fi
done
