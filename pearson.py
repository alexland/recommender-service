#!/usr/local/bin/python
# encoding: utf-8

import os
import sys
from redis import StrictRedis as redis
import numpy as NP


def recommender(v1, v2) :
    """
        returns Pearson similarity score for for 2 vectors;
        pass in 2 x NumPy 1D arrays of *equal* size
        (type is float)
    """
    v1, v2 = NP.squeeze(v1), NP.squeeze(v2)
    fnx = lambda v : NP.array(v, dtype=float)
    v1, v2 = fnx(v1), fnx(v2)
    try :
        numer = NP.sum(v1 == v2)
    except ValueError :
        print("check that the two vectors are of equal length")
    numer = NP.sum(v1*v2) - (NP.sum(v1) * NP.sum(v2)/v1.size)
    denom = ( (NP.sum(v1**2) - NP.sum(v1)**2/v1.size) *
                (NP.sum(v2**2) - NP.sum(v2)**2/v2.size) )**.5
    if denom == 0 :
        return 0
    return numer / denom


