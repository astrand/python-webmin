VERSION=0.1

.PHONY: dist rpm

dist: 
	(cd ..; tar zcvf python-webmin-${VERSION}.tgz \
	python-webmin/webmin.py\
	python-webmin/python-webmin.spec)

../python-webmin-${VERSION}.tgz: dist

rpm: ../python-webmin-${VERSION}.tgz
	(cd ..; rpm -ta python-webmin-${VERSION}.tgz)

