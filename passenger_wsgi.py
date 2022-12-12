#!/usr/bin/python3

# Required to make it run on DreamHost

import os
import sys

INTERP = "/usr/bin/python3"
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.path.dirname(__file__))

import views.channel
import views.download
import views.index

from app import app as application
