Summary: A Python implementation of the Webmin API
Name: python-webmin
Version: 0.7
Release: 1
License: GPL
Group: System/Tools
Source: python-webmin-%{version}.tgz
URL: http://www.cendio.se/~peter/python-webmin/
Packager: Peter Åstrand <astrand@lysator.liu.se>
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
/opt/python-webmin/setup.sh
/opt/python-webmin/webmin.py
/opt/python-webmin/mscstyle3/theme.py

%post
/opt/python-webmin/setup.sh 2>/dev/null
