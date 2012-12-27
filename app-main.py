#!/usr/local/bin/python
# encoding: utf-8

# TODO: create new redis DB for pearson

"""
to use, just curl against one of the endpoints, like so:
curl http://127.0.0.1:5000/jaccard?user_id=12896
to get the headers, pass in '-i'
to redirect the output to a file:
curl http://127.0.0.1:5000/jaccard?user_id=12896 | cat > t1.json
"""

from __future__ import absolute_import
import os
import sys
from math import floor
import flask as FK
from flask import g
from flask import url_for
from flask import request
from contextlib import closing
from redis import StrictRedis as redis
import numpy as NP

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


@app.route('/jaccard')
def api_jaccard():
	if  not 'user_id' in request.args:
		return "no valid user id supplied"
	else:
		from jaccard import recommender
		num_recs = 10
		user_id = request.args['user_id']
		fnx = lambda q: NP.array( list(q), dtype=int )
		v1 = fnx(g.db.get(user_id)[:25])
		all_vecs = [ [ fnx(g.db.get(k)[:25]), int(k) ] for k in g.db.keys('*') ]
		fnx = lambda v: round(v, 3)
		ji = [ [fnx(recommender(v1, row[0]) ), row[1]] for row in all_vecs ]
		ji = sorted(ji, reverse=True)[1::500]
		r = FK.jsonify(recs=ji)
		r.status_code = 200
		return r

@app.route('/')
def index():
	FK.template(index.hmtl)

@app.route('/pearson')
def api_pearson():
	if  not 'user_id' in request.args:
		return "no valid user id supplied"
	else:
		from pearson import recommender
		num_recs = 10
		user_id = request.args['user_id']
		v1 = map(float, g.db.get(user_id).split('X')[1].split('|'))
		all_vecs = [ [map(float, g.db.get(k).split('X')[1].split('|')),
			int(k)] for k in g.db.keys('*') ]
		fnx = lambda v: round(v, 3)
		ji = [[fnx(recommender(v1, row[0])), row[1]] for row in all_vecs]
		ji = sorted(ji, reverse=True)[1::500]
		r = FK.jsonify(recs=ji)
		r.status_code = 200
		return r



if __name__ == '__main__':
	app.debug = True
	app.run()
