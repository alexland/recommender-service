#!/usr/local/bin/python
# encoding: utf-8


from flask import Flask
from flask.ext import restful
from flask import request, g
from flask.ext.restful import (reqparse, abort, fields, marshal_with,
                               marshal)
							   
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

sys.path.append("/Users/doug/Projects/recommender-service/")
from app2 import app

from redis import StrictRedis as redis
from contextlib import closing
import numpy as NP


class Trec(restful.Resource):
	
	def get(self, uid):
		tx = r0.get(uid)
		# return {'rec1': tx}
		return TODOS[uid]


class Trec2(restful.Resource):
	
	def get(self):
		return TODOS



# the resources (one resource = one class)
api.add_resource(Trec2, '/rec')
api.add_resource(Trec, '/todos/<string:uid>')

if __name__ == '__main__':
	app.run(debug=True)
	http_server = HTTPServer(WSGIContainer(app))
	http_server.listen(5000)
	IOLoop.instance().start()
