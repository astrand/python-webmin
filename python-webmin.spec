Summary: A Python implementation of the Webmin API
Name: python-webmin
Version: 0.3pre
Release: 2
Requires: webmin
Copyright: GPL
Group: System/Tools
Source: python-webmin-0.3pre.tgz
URL: http://www.cendio.se/~peter/python-webmin/
Packager: Peter �strand <astrand@lysator.liu.se>
BuildRoot: %{_tmppath}/%{name}-root
BuildArchitectures: noarch


%description
python-webmin is an implementation of the Webmin API. By using
python-webmin, you can write Webmin modules in Python instead of Perl.

%prep
%setup -n python-webmin

%build
#python -O -c 'from compileall import *; compile_dir(".")'

%install
rm -rf $RPM_BUILD_ROOT
make install ROOTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/opt/python-webmin/webmin.py
/opt/python-webmin/mscstyle3/theme.py

%post

for binary in python2 python2.0 python2.1 python2.2 python2.3; do
    if $binary -c "" &>/dev/null; then
        $binary - <<EOF
import sys
sitedir = sys.prefix + "/lib/python" + sys.version[:3] + "/site-packages"
filename = sitedir + "/python-webmin.pth"
open(filename, "w").write("/opt/python-webmin\n")
print "Created", filename
EOF
    fi
done
