#!/usr/local/bin/python
# encoding: utf-8

import numpy as NP


def recommender(v1, v2) :
    """
    returns Jaccard Index for 2 bit-wise vectors;
    pass in 2 x NumPy 1D arrays (any dtype);
    but values are {0,1}, and len(v1) == len(v2)
    """
    v1, v2 = NP.squeeze(v1), NP.squeeze(v2)
    fnx = lambda v : NP.array(v, dtype=bool)
    v1, v2 = fnx(v1), fnx(v2)
    try :
        numer = NP.sum(v1 == v2)
    except ValueError :
        print("check that the two vtors are of equal length")
    denom = float(v1.size)
    return numer / denom

