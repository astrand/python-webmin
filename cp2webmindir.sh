#!/bin/sh
cp -a examples/uptimepl/* /usr/libexec/webmin/uptimepl/

rm -f examples/uptimepy/*.pyc
rm -f examples/uptimepy/*.pyo
cp -a examples/uptimepy/* /usr/libexec/webmin/uptimepy/

