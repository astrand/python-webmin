#!/bin/sh

last_working=""

# Create .pth files
for binary in python2 python2.0 python2.1 python2.2 python2.3 python2.4 python2.5 python _python_preferred_; do
    if ${binary} -c "" 2>/dev/null; then
        last_working=${binary}
        ${binary} - <<EOF
import sys
sitedirs = filter(lambda s: s[-len("site-packages"):] == "site-packages", sys.path)
if len(sitedirs) < 1:
    sys.exit("Unable to find a site-packages directory in sys.path")
filename = sitedirs[0] + "/python-webmin.pth"
open(filename, "w").write("/opt/python-webmin\n")
print "Created", filename
EOF
    fi
done
