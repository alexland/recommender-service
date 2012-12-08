#!/usr/local/bin/python
# encoding: utf-8

"""
to use, just curl against one of the endpoints, like so:

url http://127.0.0.1:5000/jaccard?user_id=12896 

to get the headers, pass in '-i'

to redirect the output to a file:

url http://127.0.0.1:5000/jaccard?user_id=12896 | cat > t1.json

"""

from __future__ import absolute_import
import os
import sys
import flask as FK
from flask import g
from flask import url_for
from flask import request
from contextlib import closing
from redis import StrictRedis as redis
import numpy as NP
import jaccard as REC

DATABASE = 0
DEBUG = True
SECRET_KEY = '!Erew9reQir549&3d394W*'
USERNAME = None
PASSWORD = None 
REDIS_HOST = 'localhost'
PORT = 6379

app = FK.Flask(__name__)
app.config.from_object(__name__)


def connect_db():
	return redis(db=DATABASE, host=REDIS_HOST, port=PORT)


@app.before_request
def before_request():
	g.db = connect_db()

# @app.teardown_request
# def teardown_request(exception):
# 	g.db.close()


@app.route('/jaccard')
def api_jaccard():
	if  not 'user_id' in request.args:
		return "no valid user id supplied"
	else:	 
		k1 = request.args['user_id']
		ji = REC.recommendations(k1)
		r = FK.jsonify(recs=ji)
		r.status_code = 200
		return r

		
	



if __name__ == '__main__':
	app.debug = True
	app.run()
