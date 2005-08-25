
PATH=$PATH:/usr/local/bin
for binary in python python2 python2.0 python2.1 python2.2 python2.3 python2.4 python2.5; do
    if $binary -c "" ; then
        $binary - <<EOF
import sys
sitedir = sys.prefix + "/lib/python" + sys.version[:3] + "/site-packages"
filename = sitedir + "/python-webmin.pth"
open(filename, "w").write("/opt/python-webmin\n")
print "Created", filename
EOF
    fi
done
