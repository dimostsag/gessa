#!/usr/bin/python
"""
Script for unscaling surfaces
"""

from __future__ import division
import os
from Surface import Surface
import numpy as np
import multiprocessing as mp
import cPickle as pickle
import sys

n_jobs = int(sys.argv[1]) # 4

surfaces_dir = sys.argv[2] # '../data/faces_scaled_4/'
output_dir = sys.argv[3] # '../data/faces_unscaled_4/'
points_file = sys.argv[4] # '../results/points/points.pkl'
newpoints_file = sys.argv[5] # '../results/points/points_unscaled.pkl'
std_centers_file = surfaces_dir+'old_stds_centers.txt'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

std_centers = np.loadtxt(std_centers_file)

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

for i in range(no_surfaces):
    surfaces[i].std = std_centers[i,0]
    surfaces[i].oldmeancenter = std_centers[i,1:4]
    surfaces[i].center = std_centers[i,4]
    newpoints[i] = surfaces[i].unscale(points = points[i])
    surfaces[i].savefile(output_dir+surfaces_filelist[i], form = 'ply', use_curvature = False)
    print surfaces[i].V.std(axis=0).mean(), surfaces[i].V.mean(axis=0)

if points_file is not None:
    pickle.dump((newpoints, faceindexes, borderpoints_no),open(newpoints_file,'w'))


