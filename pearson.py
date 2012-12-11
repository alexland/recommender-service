#!/usr/local/bin/python
# encoding: utf-8

import os
import sys
from redis import StrictRedis as redis
import numpy as NP


def recommender(vec1, vec2) :
    """
        returns cosine for 2
        feature vectors;
        pass in 2 x NumPy 1D arrays (type is float,
        of *equal* size
    """
    vec1, vec2 = NP.squeeze(vec1), NP.squeeze(vec2)
    fnx = lambda v : NP.array(v, dtype=float)
    vec1, vec2 = fnx(vec1), fnx(vec2)
    # zero center & unit variance
    vec1 -= vec1.mean()
    vec2 -= vec2.mean()
    vec1 /= vec1.std()
    vec2 /= vec2.std()
    try :
        len(vec1) == len(vec2)
    except ValueError :
        print("the two vectors are not of equal length")
    return NP.corrcoef(vec1, vec2)[1, 0]

