#!/usr/local/bin/python
# encoding: utf-8

from __future__ import absolute_import
import os
import sys
import flask as FK
from flask import url_for
from flask import request
from contextlib import closing
from redis import StrictRedis as redis
import numpy as NP

app = FK.Flask(__name__)
app.config.from_object(__name__)

REDIS_DB = 0
DEBUG = True
SECRET_KEY = '!Erew9reQir549&3d394W*'
USERNAME = None
PASSWORD = None 
REDIS_HOST = 'localhost'
PORT = 6379


def connect_db():
	return redis(db=REDIS_DB, host=REDIS_HOST, port=PORT)


@app.before_request
def before_request():
	FK.g.db = connect_db()


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
        print("check that the 2 vectors are of equal length")
    denom = float(vec1.size)
    return numer / denom



@app.route('/rec1')
def api_rec1():
	if 'user_id' in request.args:
		k1 = request.args['user_id']
		k2 = FK.g.db.randomkey()
		v12 = FK.g.db.mget([k1, k2])
		v12 = map(jaccard_prep, v12)
		score = jaccard(*v12)
		return "pair-wise score is: {0}".format(score)
	



if __name__ == '__main__':
	app.debug = True
	app.run()
