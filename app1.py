#!/usr/local/bin/python
# encoding: utf-8

"""
to use: curl -i http://127.0.0.1:5000/jaccard?user_id=12896
"""

# TODO: in similarity(), create cache


from flask import Flask
from flask.ext import restful
from flask.ext.restful import (reqparse, abort, fields, marshal_with,
                               marshal)
from redis import Redis as redis
from contextlib import closing
import numpy as NP

REDIS_DB = 2
DEBUG = True
SECRET_KEY = "!Erew9reQir549&3d394W*"
USERNAME = None
PASSWORD = None
REDIS_HOST = 'localhost'
PORT = 6379

app = Flask(__name__)
api = restful.Api(app)

TODOS = [
    { 'task': 'build an API' },
    { 'task': '?????', 'otherField': 'secret data!',},
    { 'task': 'profit!'},
]

# only output the ‘task’ field
fields = {
    'task': fields.String
}


def connect_db():
	return redis(db=REDIS_DB, host=REDIS_HOST, port=PORT)


@app.before_request
def before_request():
	Flask.g.db = connect_db()


def jaccard_prep(bitstr):
	"""
	returns bit vectors (as NP arrays);
	pass in bitstrings
	"""
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
	
	
	
class Todo(restful.Resource):
	
	@marshal_with(fields)
	def get(self, user_id):
		FK.g.db = connect_db()
		if not len(str(uid)) == 5:
			abort(404, message="{0} not a valid user id".format(uid))
		return 	
		return r0.get(uid)	


parser = reqparse.RequestParser()
parser.add_argument('rec', type=str)


class Rec(restful.Resource):
	
	@marshal_with(fields)
	def get(self):
		return Recs

	def post(self):
		args = parser.parse_args()
		task = {'rec': args['rec']}
		recs.append(rec)
		return marshal(hi_scores, fields), 201


## configure the Api resource routing here
api.add_resource(TodoList, '/todos')
api.add_resource(Rec, '/rec/<int:rec_id>')

if __name__ == '__main__':
	app.run(debug=True)
	
	