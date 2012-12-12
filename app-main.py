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


def recommender(jaccard=1, pearson=0):
	"""
		generic code for similarity-metric-based recommendation
		endpoints;
		returns json array comprised of user ids & similarity
		score based on pair-wise calc w/ client user id;
		pass in user id
	"""
	if  not 'user_id' in request.args:
		return "no valid user id supplied"
	else:
		if jaccard:
			from jaccard import recommender
		else:
			from pearson import recommender
		num_recs = 10
		user_id = request.args['user_id']
		fnx = lambda q: NP.array( list(q), dtype=int )
		vec1 = fnx(g.db.get(user_id))
		all_vecs = [ [fnx(g.db.get(k)), int(k)] for k in g.db.keys('*') ]
		ji = sorted([[recommender(vec1, row[0]), row[1]] for row in all_vecs],
				reverse=True)[::100]
		r = FK.jsonify(recs=ji)
		r.status_code = 200
		return r


@app.route('/jaccard')
def api_jaccard():
	if  not 'user_id' in request.args:
		return "no valid user id supplied"
	else:
		num_recs = 10
		user_id = request.args['user_id']
		fnx = lambda q: NP.array( list(q), dtype=int )
		vec1 = fnx(g.db.get(user_id))
		all_vecs = [ [fnx(g.db.get(k)), int(k)] for k in g.db.keys('*') ]
		ji = sorted([[recommender(vec1, row[0]), row[1]] for row in all_vecs],
				reverse=True)[::100]
		r = FK.jsonify(recs=ji)
		r.status_code = 200
		return r


@app.route('/pearson')
def api_pearson():
	if  not 'user_id' in request.args:
		return "no valid user id supplied"
	else:
		num_recs = 10
		user_id = request.args['user_id']
		fnx = lambda q: NP.array( list(q), dtype=float )
		vec1 = fnx(g.db.get(user_id))
		all_vecs = [ [fnx(g.db.get(k)), int(k)] for k in g.db.keys('*') ]
		ji = sorted([[recommender(vec1, row[0]), row[1]] for row in all_vecs],
				reverse=True)[::100]
		r = FK.jsonify(recs=ji)
		r.status_code = 200
		return r



if __name__ == '__main__':
	app.debug = True
	app.run()
