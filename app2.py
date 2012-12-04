#!/usr/local/bin/python
# encoding: utf-8


from flask import Flask
from flask.ext import restful
from flask import request, g
from flask.ext.restful import (reqparse, abort, fields, marshal_with,
                               marshal)
from redis import StrictRedis as redis
from contextlib import closing
import numpy as NP


REDIS_DB = 0
DEBUG = True
SECRET_KEY = "!Erew9reQir549&3d394W*"
USERNAME = None
PASSWORD = None
REDIS_HOST = 'localhost'
PORT = 6379

app = Flask(__name__)
api = restful.Api(app)

parser = reqparse.RequestParser()
parser.add_argument('rec', type=str)

TODOS = {
    'rec1': {'uid': '34567'},
    'rec2': {'uid': '84309'},
    'rec3': {'uid': '32865'},
}

r0 = redis(REDIS_DB, REDIS_HOST, PORT)


def connect_db():
	return redis(db=REDIS_DB, host=REDIS_HOST, port=PORT)


@app.before_request
def before_request():
	g.db = connect_db()


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


def recommendations(uid, num_recs=100):
	vec1 = jaccard_prep(r0.get(uid))
	all_vecs = [ [jaccard_prep(r0.get(k)), int(k)] for k in r0.keys('*') ]
	return sorted([[jaccard(vec1, row[0]), row[1]] for row in all_vecs],
		reverse=True)[1:][:num_recs]


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


# to use, just curl at the endpoint to get a recommendation

