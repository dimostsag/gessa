#!/usr/bin/python
"""
Script file for plotting multiple surfaces and their landmark points
"""

from __future__ import division
import numpy as np
import os
import time
import cPickle as pickle
from Surface import Surface
from FaceViewer import FaceViewer
import sys

plot_inter = False

points_file = sys.argv[1] # '../results/points/points_unscaled.pkl'
#inter_points_file = './Test/points_inter.pkl'

surfaces_dir = sys.argv[2] # '../data/faces_unscaled_4/'
surfaces_filelist = [f for f in sorted(os.listdir(surfaces_dir)) if f.endswith('.ply')]

points, faceindexes, borderpoints_no = pickle.load(open(points_file,'r'))
#intermediate_results  = pickle.load(open(inter_points_file,'r'))

#start = int(sys.argv[3])
#end = int(sys.argv[4])
#points = points[start:end]
#surfaces_filelist = surfaces_filelist[start:end]

no_surfaces = len(points)
surfaces = [Surface(surfaces_dir+f) for f in surfaces_filelist]
#for i in range(no_surfaces):
#    surfaces[i].scale(std=75, center = 0.0)
#print surfaces
FaceViewer.plot_multiple(surfaces, points, borderpoints_no, point_scale_factor = 4, colormap = 'autumn')

if plot_inter == True:
    for i in range(len(intermediate_results[0])):
        points_inter = [intermediate_results[j][i][0]  for j in range(no_surfaces)]
        FaceViewer.plot_multiple(surfaces, points_inter, borderpoints_no, point_scale_factor = 2.0, colormap = 'Accent')
