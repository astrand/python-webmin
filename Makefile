VERSION=0.7
ROOTDIR=/
WEBMINDIR=$(ROOTDIR)/opt/python-webmin
USERMINDIR=$(ROOTDIR)/opt/python-webmin

.PHONY: dist rpm

all:

install:
# API module
	mkdir -p $(WEBMINDIR)
	mkdir -p $(WEBMINDIR)/mscstyle3
	install setup.sh $(WEBMINDIR)
# FIXME: Compile 
	install webmin.py $(WEBMINDIR)
	install themes/mscstyle3/theme.py $(WEBMINDIR)/mscstyle3/

install-usermin:
# API module
	mkdir -p $(USERMINDIR)
	mkdir -p $(USERMINDIR)/mscstyle3
# FIXME: Compile 
	install webmin.py $(USERMINDIR)
	install themes/mscstyle3/theme.py $(USERMINDIR)/mscstyle3/


install-examples:
# Python example module
	mkdir -p $(WEBMINDIR)/uptimepy
	install -m 644 examples/uptimepy/config $(WEBMINDIR)/uptimepy
	install -m 644 examples/uptimepy/module.info $(WEBMINDIR)/uptimepy
	install -m 644 examples/uptimepy/uptimelib.py $(WEBMINDIR)/uptimepy
	install examples/uptimepy/index.cgi $(WEBMINDIR)/uptimepy
	mkdir -p $(WEBMINDIR)/uptimepy/images
	install -m 644 examples/uptimepy/images/icon.gif $(WEBMINDIR)/uptimepy/images
# Perl example module
	mkdir -p $(WEBMINDIR)/uptimepl
	install -m 644 examples/uptimepl/config $(WEBMINDIR)/uptimepl
	install -m 644 examples/uptimepl/module.info $(WEBMINDIR)/uptimepl
	install -m 644 examples/uptimepl/uptime-lib.pl $(WEBMINDIR)/uptimepl
	install examples/uptimepl/index.cgi $(WEBMINDIR)/uptimepl
	mkdir -p $(WEBMINDIR)/uptimepl/images
	install -m 644 examples/uptimepl/images/icon.gif $(WEBMINDIR)/uptimepl/images

dist: 
	(cd ..; tar zcvf python-webmin/python-webmin-$(VERSION).tgz \
	python-webmin/setup.sh\
	python-webmin/Makefile\
	python-webmin/webmin.py\
	python-webmin/python-webmin.spec\
	python-webmin/themes/mscstyle3/theme.py \
	python-webmin/examples/uptimepl/index.cgi\
	python-webmin/examples/uptimepl/images/icon.gif\
	python-webmin/examples/uptimepl/config\
	python-webmin/examples/uptimepl/module.info\
	python-webmin/examples/uptimepl/uptime-lib.pl\
	python-webmin/examples/uptimepy/uptimelib.py\
	python-webmin/examples/uptimepy/images/icon.gif\
	python-webmin/examples/uptimepy/config\
	python-webmin/examples/uptimepy/index.cgi\
	python-webmin/examples/uptimepy/module.info)

python-webmin-$(VERSION).tgz: dist

rpm: python-webmin-$(VERSION).tgz
	rpmbuild -ta python-webmin-$(VERSION).tgz 
