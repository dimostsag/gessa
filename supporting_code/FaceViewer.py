#!/usr/bin/python
"""
Class for Surface and Landmark Visualization
"""

from __future__ import division
import numpy as np
import os
import time

from mayavi import mlab
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

from Surface import Surface

class FaceViewer:
    
    @classmethod
    def plot(self, surface, points, borderpoints_no, point_scale_factor = 1.0, colormap = 'Accent'):
        if points is None:
            mlab.figure(bgcolor=(1,1,1))
            m = mlab.triangular_mesh(surface.V[:,0], surface.V[:,1] ,surface.V[:,2], surface.F, color = (0.6,0.6,0.6), representation = 'surface')
            mlab.show()
        else:
            cols = range(1,points[borderpoints_no:,0].shape[0]+1) 
            f = mlab.figure(bgcolor=(1,1,1))
            m = mlab.triangular_mesh(surface.V[:,0], surface.V[:,1] ,surface.V[:,2], surface.F, color = (0.5,0.5,0.5), representation = 'surface')
            b = mlab.points3d(points[:borderpoints_no,0], points[:borderpoints_no,1], points[:borderpoints_no,2], color = (0,0,0), scale_factor = point_scale_factor, scale_mode = 'none')
            #p = mlab.points3d(points[borderpoints_no:,0], points[borderpoints_no:,1], points[borderpoints_no:,2], cols, colormap = colormap, scale_factor = point_scale_factor, scale_mode = 'none')
            p = mlab.points3d(points[borderpoints_no:,0], points[borderpoints_no:,1], points[borderpoints_no:,2], color = (1,0,0), scale_factor = point_scale_factor, scale_mode = 'none')
            mlab.show()
        return None
    
    @classmethod
    def plot_dif_sets(self, surface, points_list, point_scale_factor = 1.0):
        cols = ((1,0,0),(0,0.5,1),(0,1,0),(1,0.6,0)) # red, cyan,  green, yellow
        #modes = ('2dcircle','2dcross','2ddiamond','cone')
        f = mlab.figure(bgcolor=(1,1,1))
        m = mlab.triangular_mesh(surface.V[:,0], surface.V[:,1] ,surface.V[:,2], surface.F, color = (0.5,0.5,0.5), representation = 'surface')
        for i in range(len(points_list)):
            points = points_list[i]
            col = cols[i]
            p = mlab.points3d(points[:,0], points[:,1], points[:,2], color = col, scale_factor = point_scale_factor, scale_mode = 'none', opacity=0.5)
        mlab.show()
        return None
    
    @classmethod
    def plot_transitions(self, surface, intermediate_results, borderpoints_no, point_scale_factor = 1.0, colormap = 'Accent'):
        cols = range(1,intermediate_results[-1][3][-1][2][borderpoints_no:,0].shape[0]+1) 
        f=mlab.figure()
        m = mlab.triangular_mesh(surface.V[:,0], surface.V[:,1] ,surface.V[:,2], surface.F, color = (0.3,0.3,0.3), representation = 'surface')
        f.scene.y_plus_view()
        f.scene.full_screen = True
        f.scene.background = (1,1,1)
        iteration, cost, points = intermediate_results[0][3][0]
        b = mlab.points3d(points[:borderpoints_no,0], points[:borderpoints_no,1], points[:borderpoints_no,2], color = (0,0,0), scale_factor = point_scale_factor, scale_mode = 'none')
        p = mlab.points3d(points[borderpoints_no:,0], points[borderpoints_no:,1], points[borderpoints_no:,2], cols[:points[borderpoints_no:,0].shape[0]], colormap = colormap, scale_factor = point_scale_factor, scale_mode = 'none')
        anim(intermediate_results, cols, borderpoints_no, p)
        mlab.show()
        return None
    
    @classmethod
    def plot_multiple(self, surfaces, points, borderpoints_no, point_scale_factor = 1.0, colormap = 'Accent'): # surfaces must have the same number of points
        if (points is None):
            for i in range(len(surfaces)):
                mlab.figure(bgcolor=(1,1,1))
                m = mlab.triangular_mesh(surfaces[i].V[:,0], surfaces[i].V[:,1] ,surfaces[i].V[:,2], surfaces[i].F, color = (0.3,0.3,0.3), representation = 'surface')
            mlab.show()
        elif (borderpoints_no is None):
            for i in range(len(surfaces)):
                mlab.figure(bgcolor=(1,1,1))
                m = mlab.triangular_mesh(surfaces[i].V[:,0], surfaces[i].V[:,1] ,surfaces[i].V[:,2], surfaces[i].F, color = (0.5,0.5,0.5), representation = 'surface')
                p = mlab.points3d(points[i][:,0], points[i][:,1], points[i][:,2], color = (1,0,0), scale_factor = point_scale_factor, scale_mode = 'none')
            mlab.show()
        else:
            cols = range(1,points[0][borderpoints_no[0]:,0].shape[0]+1) 
            #np.random.rand(points[0][borderpoints_no[0]:,0].shape[0])
            for i in range(len(surfaces)):
                mlab.figure(bgcolor=(1,1,1))
                m = mlab.triangular_mesh(surfaces[i].V[:,0], surfaces[i].V[:,1] ,surfaces[i].V[:,2], surfaces[i].F, color = (0.5,0.5,0.5), representation = 'surface')
                b = mlab.points3d(points[i][:borderpoints_no[i],0], points[i][:borderpoints_no[i],1], points[i][:borderpoints_no[i],2], color = (0,0,0), scale_factor = point_scale_factor, scale_mode = 'none')
                p = mlab.points3d(points[i][borderpoints_no[i]:,0], points[i][borderpoints_no[i]:,1], points[i][borderpoints_no[i]:,2], cols, colormap = colormap, scale_factor = point_scale_factor, scale_mode = 'none')
            mlab.show()
        return None

    @classmethod
    def plot_transitions_multiple(self, surfaces, intermediate_results, borderpoints_no, point_scale_factor = 1.0, colormap = 'Accent'):
        cols = range(1,intermediate_results[-1][3][-1][2][borderpoints_no:,0].shape[0]+1) 
        f=mlab.figure()
        m = mlab.triangular_mesh(surface.V[:,0], surface.V[:,1] ,surface.V[:,2], surface.F, color = (0.3,0.3,0.3), representation = 'surface')
        f.scene.y_plus_view()
        f.scene.full_screen = True
        f.scene.background = (1,1,1)
        iteration, cost, points = intermediate_results[0][3][0]
        b = mlab.points3d(points[:borderpoints_no,0], points[:borderpoints_no,1], points[:borderpoints_no,2], color = (0,0,0), scale_factor = point_scale_factor, scale_mode = 'none')
        p = mlab.points3d(points[borderpoints_no:,0], points[borderpoints_no:,1], points[borderpoints_no:,2], cols[:points[borderpoints_no:,0].shape[0]], colormap = colormap, scale_factor = point_scale_factor, scale_mode = 'none')
        anim(intermediate_results, cols, borderpoints_no, p)
        mlab.show()
        return None

@mlab.animate(delay=15)
def anim(intermediate_results, cols, borderpoints_no, p):
    f = mlab.gcf()
    for up_no in range(len(intermediate_results)):
        time.sleep(1)
        update = intermediate_results[up_no][3]
        #print 'Update ', up_no
        for iter_no in range(len(update)):
            iteration, cost, points = update[iter_no]
            print iteration, cost
            p.mlab_source.set(points = points[borderpoints_no:])
            p.mlab_source.set(x=points[borderpoints_no:,0], y=points[borderpoints_no:,1], z=points[borderpoints_no:,2], scalars = cols[:points[borderpoints_no:,0].shape[0]])
            p.mlab_source.set( colormap = 'Accent')            
            if iter_no == 1:
                time.sleep(1)
            yield

if __name__ == '__main__':
    print 'Testing FaceViewer...'
    surfaces_dir = './Test/'
    surfaces_filelist = [f for f in sorted(os.listdir(surfaces_dir)) if f.endswith('.ply')]
    surfaces = [Surface(surfaces_dir+f) for f in surfaces_filelist]
    FaceViewer.plot(surfaces,None,None)
    print 'Ok'


