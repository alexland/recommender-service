#!/usr/local/bin/python
# encoding: utf-8

import sys
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

sys.path.append("/Users/doug/Projects/recommender-service/")
from appred1 import app


http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
IOLoop.instance().start()