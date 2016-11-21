#!/usr/bin/python
"""
Script for scaling surfaces
"""

from __future__ import division
import os
from Surface import Surface
import numpy as np
import multiprocessing as mp
import cPickle as pickle
import sys

n_jobs = int(sys.argv[1]) # 4

surfaces_dir = sys.argv[2] # '../data/faces_unscaled_4/'
output_dir = sys.argv[3] # '../data/faces_scaled_4/'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
points_file = None # '../results/points/points_unscaled.pkl'
newpoints_file = None # '../results/points/points_scaled.pkl'
scale_std = 75
scale_center = 0.0

surfaces_filelist = [f for f in sorted(os.listdir(surfaces_dir)) if f.endswith('.ply')]

if n_jobs == 1:
    surfaces = [Surface(surfaces_dir+f) for f in surfaces_filelist]
else:
    pool = mp.Pool(processes=n_jobs,maxtasksperchild=1)
    surfaces_filelist2 = [surfaces_dir+f for f in surfaces_filelist]
    surfaces = pool.map(Surface, surfaces_filelist2)
    pool.close()
    pool.join()

no_surfaces = len(surfaces)

if points_file is None:
    points = [None for i in range(no_surfaces)]
else:
    points, faceindexes, borderpoints_no = pickle.load(open(points_file,'r'))

newpoints = [None for i in range(no_surfaces)]

old_values = np.zeros((no_surfaces,5))

for i in range(no_surfaces):
    newpoints[i] = surfaces[i].scale(std = scale_std, center = scale_center, points = points[i])
    old_values[i,0] = surfaces[i].std 
    old_values[i,1:4] = surfaces[i].oldmeancenter
    old_values[i,4] = scale_center
    surfaces[i].savefile(output_dir+surfaces_filelist[i], form = 'ply', use_curvature = False)
    print old_values[i]
    print surfaces[i].V.std(axis=0).mean(), surfaces[i].V.mean(axis=0)

np.savetxt(output_dir+'old_stds_centers.txt',old_values,'%f')
if points_file is not None:
    pickle.dump((newpoints, faceindexes, borderpoints_no),open(newpoints_file,'w'))

