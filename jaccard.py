#!/usr/local/bin/python
# encoding: utf-8

import os
import sys
from redis import StrictRedis as redis
import numpy as NP


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