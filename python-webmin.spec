Summary: A Python implementation of the Webmin API
Name: python-webmin
Version: 0.1
Release: 1
Requires: webmin
Copyright: GPL
Group: System/Tools
Source: python-webmin-0.1.tgz
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
python -O -c 'from compileall import *; compile_dir(".")'

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/libexec/webmin
cp webmin.py $RPM_BUILD_ROOT/usr/libexec/webmin

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/libexec/webmin/webmin.py
