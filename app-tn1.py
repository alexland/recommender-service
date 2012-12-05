#!/usr/local/bin/python2.7
# encoding: utf-8


import tornado.ioloop
import tornado.web

from tapioca import TornadoRESTful, ResourceHandler

class HelloResource(ResourceHandler):

    def get_collection(self, callback):
        callback("Hello, world!")

api = TornadoRESTful(discovery=True)
api.add_resource('hello', HelloResource)
application = tornado.web.Application(
    api.get_url_mapping()
)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
	
	