#!/usr/bin/python
"""
Script for plotting a Surface and its landmark points
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

surfaces_file = sys.argv[2] # '../data/faces_unscaled_4/'

points, faceindexes, borderpoints_no = pickle.load(open(points_file,'r'))
#intermediate_results  = pickle.load(open(inter_points_file,'r'))

surface = Surface(surfaces_file)
FaceViewer.plot(surface, points, borderpoints_no, point_scale_factor = 3.5, colormap = 'Accent')

