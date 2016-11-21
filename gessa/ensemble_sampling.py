#!/usr/bin/python

from __future__ import division
import numpy as np
import os
import time
import cPickle as pickle
os.system('taskset -p 0xffffffff %d' % os.getpid()) 
import sys
from Surface import Surface
from SurfaceSampler import EnsembleSurfaceSampler
import multiprocessing as mp

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

if __name__ == '__main__':
    print 'GESSA Ensemble Surface Sampling...'
    
    # Parameters
    n_jobs = int(sys.argv[1])
    max_points = int(sys.argv[2])
    max_iterations = int(sys.argv[3])
    surfaces_dir = sys.argv[4]
    results_filename = sys.argv[5]
    #

    # Fixed and Advanced Parameters - Please leave fixed
    test_ensemble = True
    save_results = True
    previous_point_file = None
    previous_points=None
    max_iterations_inc_step = 0
    inter_results_filename = '../results/points/points_inter.pkl'
    sigma_continue = 1.1
    curvature_adapt = False
    curvature_index = 0
    regression_adapt = False
    regression_weights_file = None
    rerun_iterations = 10
    keep_intermediate = False
    print_iterations = False
    plot = False
    plot_inter = False
    save_final_density = False
    density_output_dir = '../results/density_plys/'
    if plot == True:
        from FaceViewer import FaceViewer
    weights = 'uniform'
    weight_matrix = None
    #
    
    start_time = time.time()
    
    surfaces_filelist = [f for f in sorted(os.listdir(surfaces_dir)) if f.endswith('.ply')]

    if test_ensemble == True:
        # Read Surfaces
        if n_jobs == 1:
            surfaces = [Surface(surfaces_dir+f) for f in surfaces_filelist]
        else:
            pool = mp.Pool(processes=n_jobs,maxtasksperchild=1)
            surfaces_filelist2 = [surfaces_dir+f for f in surfaces_filelist]
            surfaces = pool.map(Surface, surfaces_filelist2)
            pool.close()
            pool.join()
        print [surface.surface_filename for surface in surfaces]
        
        # RUN GESSA
        sampler = EnsembleSurfaceSampler()
        sampler.fit(surfaces, max_points = max_points, initials = None, speed = 'minsquarredsigma', threshold=0.0000000005, max_iterations = max_iterations, max_iteration_inc_step = max_iterations_inc_step, cost='entropy', sigma = 'fixed', sigma_min = 1.1, sigma_max = 75, weights = weights, weight_matrix = weight_matrix, kernel='gaussian', truncate_kernel=True, borders = True, relative_cost_weight = 1, n_jobs = n_jobs, previous_points = previous_points, sigma_continue = sigma_continue, print_iterations = print_iterations, keep_intermediate = keep_intermediate, save_final_density = save_final_density, scale = False)

        end_time = time.time()

        # Save results
        points, faceindexes, borderpoints_no = sampler.get_results()
        if save_results == True:
            pickle.dump(sampler.get_results(),open(results_filename,'w'))
 
    print 'Elapsed time (Sec):', (end_time - start_time)
