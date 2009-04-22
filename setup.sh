#!/bin/sh

last_working=""

# Create .pth files
for binary in python2 python2.2 python2.3 python2.4 python2.5 python2.6 python _python_preferred_; do
    if ${binary} -c "" 2>/dev/null; then
        last_working=${binary}
        ${binary} - <<EOF
from distutils import sysconfig
filename = sysconfig.get_python_lib() + "/python-webmin.pth"
open(filename, "w").write("/opt/python-webmin\n")
print "Created", filename
EOF
    fi
done
