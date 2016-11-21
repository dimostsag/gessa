#!/usr/bin/python
"""
Example code for loading landmark points and surfaces, either using one core or multiple.
"""

from __future__ import division
import numpy as np
import os
import time
import cPickle as pickle
from Surface import Surface
from scipy.spatial import distance
import sys
import multiprocessing as mp

n_jobs = int(sys.argv[1])
points_file = sys.argv[2] # '../results/points/points.pkl'
surfaces_dir =  sys.argv[3] # '../data/faces_scaled_4/'

points, faceindexes, borderpoints_no = pickle.load(open(points_file,'r'))
#points = points[:150]

no_surfaces = len(points)
surfaces_filelist = [f for f in sorted(os.listdir(surfaces_dir)) if f.endswith('.ply')]
#surfaces_filelist = surfaces_filelist[:150]
no_surfaces_2 = len(surfaces_filelist)
if no_surfaces != no_surfaces_2:
    print 'Points and surfaces size different'
    raise

if n_jobs == 1:
    surfaces = [Surface(surfaces_dir+f) for f in surfaces_filelist]
else:
    pool = mp.Pool(processes=n_jobs,maxtasksperchild=1)
    surfaces_filelist2 = [surfaces_dir+f for f in surfaces_filelist]
    surfaces = pool.map(Surface, surfaces_filelist2)
    pool.close()
    pool.join()

