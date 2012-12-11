#!/usr/local/bin/python
# encoding: utf-8

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
from jaccard import recommender

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
		num_recs = 10
		user_id = request.args['user_id']
		fnx = lambda q: NP.array( list(q), dtype=int )
		vec1 = fnx(g.db.get(user_id))
		all_vecs = [ [fnx(g.db.get(k)), int(k)] for k in g.db.keys('*') ]
		ji = sorted([[recommender(vec1, row[0]), row[1]] for row in all_vecs],
				reverse=True)[1:][:num_recs]
		r = FK.jsonify(recs=ji)
		r.status_code = 200
		return r


# @app.route('/freq_itemsets')
# def api_freq_itemsets():


if __name__ == '__main__':
	app.debug = True
	app.run()
