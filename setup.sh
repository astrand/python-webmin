#!/bin/sh

last_working=""

# Create .pth files
for binary in python2 python2.2 python2.3 python2.4 python2.5 python2.6 python _python_preferred_; do
    if ${binary} -c "" 2>/dev/null; then
        last_working=${binary}
        ${binary} - <<EOF
pthfile="python-webmin.pth"
mod_dir="/opt/python-webmin"
from distutils import sysconfig
filename = sysconfig.get_python_lib() + "/" + pthfile
open(filename, "w").write(mod_dir + "\n")
print "Created", filename
EOF
    fi
done
