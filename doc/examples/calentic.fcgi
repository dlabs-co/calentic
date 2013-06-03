#!/usr/bin/python
from flup.server.fcgi import WSGIServer
from calentic.server import APP
from werkzeug.contrib.fixers import LighttpdCGIRootFix
import os

if __name__ == '__main__':
    WSGIServer(LighttpdCGIRootFix(APP)).run()

