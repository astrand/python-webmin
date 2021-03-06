#!/bin/sh

last_working=""

# Create .pth files
for binary in python2 python2.2 python2.3 python2.4 python2.5 python2.6 python _python_preferred_; do
    if ${binary} -c "" 2>/dev/null; then
        last_working=${binary}
        ${binary} - <<EOF
pthfile="python-webmin.pth"
mod_dir="/opt/python-webmin"
import sys, os
sitedirs = filter(lambda s: s.endswith("site-packages") or s.endswith("dist-packages"), sys.path)
if len(sitedirs) < 1:
    sys.exit("Unable to find a site packages directory in sys.path")
filename = sitedirs[0] + "/" + pthfile
want = mod_dir + "\n"
if not os.path.exists(filename) or open(filename, "r").read() != want:
    open(filename, "w").write(want)
    print "Created", filename
EOF
    fi
done
