# uptimelib.py
# Common functions for the uptime module

import webmin
import os
import sys

webmin.init_config()

def print_uptime():
    sys.stdout.flush()
    os.system("uptime")
    
