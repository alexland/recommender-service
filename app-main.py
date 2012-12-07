#!/usr/local/bin/python
# encoding: utf-8

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


# @app.teardown_request
# def teardown_request(exception):
# 	g.db.close()


def jaccard_prep(bitstr):
	return NP.array( list(bitstr), dtype=int )


def jaccard(vec1, vec2) :
    """
        returns Jaccard Index for 2 bit-wise vectors;
        pass in 2 x NumPy 1D arrays (type is int/float/boolean, 
		if former 2;
        values of 0, 1 only ) of *equal* size
    """
    vec1, vec2 = NP.squeeze(vec1), NP.squeeze(vec2)
    fnx = lambda v : NP.array(v, dtype=bool)
    vec1, vec2 = fnx(vec1), fnx(vec2)
    try :
        numer = NP.sum(vec1 == vec2)
    except ValueError :
        print("check that the two vectors are of equal length")
    denom = float(vec1.size)
    return numer / denom


def recommendations(user_id, num_recs=10):
	vec1 = jaccard_prep(g.db.get(user_id))
	all_vecs = [ [jaccard_prep(g.db.get(k)), int(k)] for k in g.db.keys('*') ]
	return sorted([[jaccard(vec1, row[0]), row[1]] for row in all_vecs],
		reverse=True)[1:][:num_recs]


@app.route('/jaccard')
def api_jaccard():
	if  not 'user_id' in request.args:
		return "no valid user id supplied"
	else:	 
		k1 = request.args['user_id']
		ji = recommendations(k1)
		r = FK.jsonify(recs=ji)
		r.status_code = 200
		return r

		
	



if __name__ == '__main__':
	app.debug = True
	app.run()
