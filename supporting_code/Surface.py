#!/usr/bin/python
"""
Surface Class
"""


from __future__ import division
import numpy as np
import cPickle as pickle

from PlyReader import PlyReader

class Surface(object):
    
    #~ def __new__(cls, surface_filename, form='ply'):
        #~ if form == 'ply':
            #~ return super(Surface, cls).__new__(cls)
        #~ elif form == 'pkl':
            #~ return pickle.load(open(surface_filename,'rb'))
        #~ else:
            #~ print 'Only ascii ply or pickled surface objects supported for 3D meshes at the moment'
            #~ raise
        
    def __init__(self, surface_filename, form='ply'):
        if form == 'ply':
            self.surface_filename = surface_filename
            self.V, self.F, self.D = PlyReader.load_ply(surface_filename)
            
            #self.E = dict() # dictionary of edges and their adjacent face indexes
            #self.VF = dict() # list of vertices and their adjacent face indexes and face angles in that vertex
            #self.FA = dict() # list of adjacent faces, the edge vector and angle to rotate from f1 to f2
            #self.A = np.empty((self.F.shape[0],)) # areas of triangles
            #self.N = Surface._face_normals(self.V, self.F) # triangle normals ### Checks direction during edge adjacency
            #for i in range(self.F.shape[0]):
            #    indexes = self.F[i,:]
            #    points = self.V[indexes,:]
            #    self.A[i] = Surface._area(points[0,:], points[1,:], points[2,:])
            
            self.A, self.N = Surface._face_areas_normals(self.V, self.F)
            self.E = Surface._edge_adjacent_faceindexes(self.V, self.F)
            self.FA = Surface._face_adjacent_rotations(self.V, self.F, self.N, self.E)
            self.VF = Surface._vertex_adjacent_faceindexes(self.V, self.F, self.E, self.FA)
        elif form == 'pkl':
            pass
        else:
            print 'Only ascii ply or pickled surface objects supported for 3D meshes at the moment'
            raise
   
    @classmethod
    def _area(cls, a, b, c) :
        return 0.5 * np.linalg.norm( np.cross( b-a, c-a ) )

    @classmethod
    def _face_normals(cls, V, F) :
        tris = V[F]
        n = np.cross( tris[::,1 ] - tris[::,0]  , tris[::,2 ] - tris[::,0] )
        return Surface._normalize_normals(n)
    
    @classmethod
    def _face_areas_normals(cls, V, F) :
        tris = V[F]
        n = np.cross( tris[::,1 ] - tris[::,0]  , tris[::,2 ] - tris[::,0] )
        return 0.5 * np.linalg.norm( n, axis=1 ), Surface._normalize_normals(n)
    
    @classmethod
    def _face_adjacent_rotations(cls, V, F, N, E):
        FA = dict()
        for edge in E.keys():
            faceindexes = E[edge]
            if len(faceindexes) == 1:
                pass
            elif len(faceindexes) == 2:
                fp1 = tuple(faceindexes)
                fp2 = tuple(( faceindexes[1], faceindexes[0]))
                F1 = F[faceindexes[0]]
                F2 = F[faceindexes[1]]
                Fex1 = np.setdiff1d(F1, edge)
                Fex2 = np.setdiff1d(F2, edge)
               
                Va = edge[0]
                Vb = edge[1]
                if (np.where(F1 == Va)[0][0] == 0 and np.where(F1 == Vb)[0][0] == 1) or (np.where(F1 == Va)[0][0] == 1 and np.where(F1 == Vb)[0][0] == 2) or (np.where(F1 == Va)[0][0] == 2 and np.where(F1 == Vb)[0][0] == 0):
                    edge_vector1 = V[Vb] - V[Va]
                else:
                    edge_vector1 = V[Va] - V[Vb]
                edge_vector2 = - edge_vector1
                
                angle_between_normals = np.arctan2(np.linalg.norm(np.cross(N[faceindexes[0]], N[faceindexes[1]])), np.dot(N[faceindexes[0]], N[faceindexes[1]]))
                # correct angle... Let's see
                Fexvector = V[Fex2] - V[Fex1]
                if np.dot(Fexvector, N[faceindexes[0]]) >= 0:
                    angle_between_normals = - angle_between_normals
                
                angle1 = angle_between_normals
                angle2 = angle_between_normals
               
                FA[fp1] = (edge_vector1, angle1, (Va, Vb)) # vertex indices added here for the folding function
                FA[fp2] = (edge_vector2, angle2, (Va, Vb))
            else:
                print 'edges must have 1 or 2 adjacent faces. Check smth wrong.'
                raise
            
        return FA
    
    @classmethod
    def _border_vertex_indices(cls, E):
        border_edges = [(e[0], e[1]) for e in E.keys() if len(E[e]) == 1]
        border_edges = np.array(border_edges, dtype=int)
        border_vertices = np.unique(border_edges.flatten())
        return border_vertices
        
    @classmethod
    def _vertex_adjacent_faceindexes(cls, V, F, E, FA): 
        VF = dict()
        pairs = FA.keys()
        
        border_vertex_indices = Surface._border_vertex_indices(E)
        for edge in E.keys():
            v1 = edge[0]
            v2 = edge[1]
            faceindexes = E[edge]
            if v1 not in VF:
                VF[v1] = list()
            if v2 not in VF:
                VF[v2] = list()
            VF[v1].extend(faceindexes)
            VF[v2].extend(faceindexes)
                
        for v in VF.keys():
            list_of_faceindexes = np.unique(VF[v])
            if v in border_vertex_indices: # points should never reach border vertices so no need to get into the trouble of sorting the order
                list_of_faceindexes_arranged = list_of_faceindexes
            else: # Closed vertices
                list_of_faceindexes_arranged = np.empty(list_of_faceindexes.shape, dtype=int)
                # arrange faceindexes so consecutive entries are neighbours:
                list_of_faceindexes_arranged[0] = list_of_faceindexes[0]
                
                for jjj in range(1,list_of_faceindexes.shape[0]):
                    face = F[list_of_faceindexes_arranged[jjj-1]]
                    if face[0] == v:
                        nextedge = (face[2],v)
                    elif face[1] == v:
                        nextedge = (face[0],v)
                    elif face[2] == v:
                        nextedge = (face[1],v)
                    else:
                        print 'Vertex not found in faceindexes'
                        raise
                    list_of_faceindexes_arranged[jjj] = np.setdiff1d(E[tuple(sorted(nextedge))],list_of_faceindexes_arranged[jjj-1])
                     
            list_of_angles = np.zeros(list_of_faceindexes_arranged.shape)
            for i in range(len(list_of_faceindexes_arranged)):
                face = F[list_of_faceindexes_arranged[i]]
                triangle = V[face]
                v_index = np.where(face == v)[0][0]
                vdif_indexes = np.where(face != v)[0]
                edge1 = V[vdif_indexes[0]] - V[v_index]
                edge2 = V[vdif_indexes[1]] - V[v_index]
                angle = np.arccos( np.dot(edge1, edge2) / ( np.linalg.norm(edge1) * np.linalg.norm(edge2) ) )
                list_of_angles[i] = angle
            
            VF[v] = (list_of_faceindexes_arranged, list_of_angles)
    
        return VF        
    
    @classmethod
    def _edge_adjacent_faceindexes(cls, V, F): # IMPORTANT: Incorporates check that face normals are all on the same direction
        E = dict() # Every edge should have at the end max 2 face indexes. 1 index means the edge is in the border.
        for i in range(F.shape[0]):
            edge1 = (min(F[i,0], F[i,1]),max(F[i,0], F[i,1]))
            edge2 = (min(F[i,1], F[i,2]),max(F[i,1], F[i,2]))
            edge3 = (min(F[i,2], F[i,0]),max(F[i,2], F[i,0]))
            if edge1 in E:
                E[edge1].append(i)
            else:
                E[edge1] = [i,]
            if edge2 in E:
                E[edge2].append(i)
            else:
                E[edge2] = [i,]
            if edge3 in E:
                E[edge3].append(i)
            else:
                E[edge3] = [i,]
        for edge in E.keys(): # Check normal direction
            face_indexes = E[edge]
            if len(face_indexes) == 1:
                continue
            elif len(face_indexes) == 2:
                face1 = F[face_indexes[0]]
                face2 = F[face_indexes[1]]
                # Check comprises of: The edge in each face must be traversed in opposite directions
                ind11 = np.where(face1 == edge[0])[0]
                ind12 = np.where(face1 == edge[1])[0]
                ind21 = np.where(face2 == edge[0])[0]
                ind22 = np.where(face2 == edge[1])[0]
                direct1 = (ind12 == ind11+1) or (ind11 == 2 and ind12 == 0)
                direct2 = (ind22 == ind21+1) or (ind21 == 2 and ind22 == 0)
                if direct1 == direct2:
                    print 'Direction of edge traversion is not correct. Normals will not have correct orientation.'
                    raise
            else:
                print 'mesh edge should have 1 or 2 adjacent faces. Something is wrong'
                raise
        return E
    
    @classmethod
    def _vertex_normals(cls, V, F) :
        print 'Vertex normals not implemented' # Not needed
        raise
        return None
    
    @classmethod
    def _normalize_normals(cls, arr) :
        ''' Normalize a numpy array of 3 component vectors shape=(n,3) '''
        lens = np.sqrt( arr[:,0]**2 + arr[:,1]**2 + arr[:,2]**2 )
        return arr / lens[:,np.newaxis]
    
    def get_vertices(self):
        return self.V
    
    def get_faces(self):
        return self.F
        
    def get_quality(self):
        return self.D
    
    def get_areas(self):
        return self.A
        
    def get_face_normals(self):
        return self.N
        
    def savefile(self, filename, form = 'ply', use_curvature = False):
        if form == 'ply':
            if use_curvature == True:
                return PlyReader.save_ply(filename, self.V, self.F, self.curvatures)
            else:
                return PlyReader.save_ply(filename, self.V, self.F, self.D)
        elif form == 'pkl':
            pickle.dump(self, open(filename,'wb'))
            return filename
        else:
            print 'Only ascii ply or pkl save format supported for 3D meshes at the moment'
            raise

    def __str__(self):
        return ''.join(('Surface Instance\nFileName: ', self.surface_filename, '\nNo of V,F,E: ', str(self.V.shape[0]), ',', str(self.F.shape[0]), ',', str(len(self.E))))

    def scale(self, std, center = None, points = None):         
        mean = self.V.mean(axis=0)
        if center is None:
            center = mean

        # move to (0,0,0)
        V = self.V - mean
        #scale to 1
        V = V / self.V.std(axis=0).mean()
        # scale to std
        V = V * std
        # move to new center
        V = V + center

        if points is not None:
            points = points - mean
            points = points / self.V.std(axis=0).mean()
            points = points * std
            points = points + center

        self.oldmeancenter = mean
        self.center = center
        self.std = self.V.std(axis=0).mean()
        self.V = V #(self.V - move) / (self.std / std)
        
        self.A, self.N = Surface._face_areas_normals(self.V, self.F)
        self.E = Surface._edge_adjacent_faceindexes(self.V, self.F)
        self.FA = Surface._face_adjacent_rotations(self.V, self.F, self.N, self.E)
        self.VF = Surface._vertex_adjacent_faceindexes(self.V, self.F, self.E, self.FA)       
        return points
        
    def unscale(self, points = None):
        
        # reverse order from scale
        V = self.V - self.center
        V = V / self.V.std(axis=0).mean()
        V = V * self.std
        V = V + self.oldmeancenter

        if points is not None:
            points = points - self.center
            points = points / self.V.std(axis=0).mean()
            points = points * self.std
            points = points + self.oldmeancenter
        
        self.V = V
        self.A, self.N = Surface._face_areas_normals(self.V, self.F)
        self.E = Surface._edge_adjacent_faceindexes(self.V, self.F)
        self.FA = Surface._face_adjacent_rotations(self.V, self.F, self.N, self.E)
        self.VF = Surface._vertex_adjacent_faceindexes(self.V, self.F, self.E, self.FA)  
        return points
        
    def load_curvature(self, filename, curvature_index = 0, absolute = False): # Sizewise must be equal to vertices
        curvatures = np.loadtxt(filename,dtype=float)
        curvatures = curvatures[:,curvature_index]
        if absolute == True:
            curvatures = np.absolute(curvatures)
        facevertexcurvatures = curvatures[self.F]
        self.curvatures = facevertexcurvatures.mean(axis=1)
        self.curvature_max = self.curvatures.max()
    
    def get_face_curvatures(self, faceindexes,  pdf_weights = False):
        curvatures = self.curvatures[faceindexes[:,0]]
        if pdf_weights == True:
            curvatures = 0.85 + (0.3 * (curvatures / self.curvature_max))
        return curvatures

if __name__ == '__main__':
    import time
    print 'Testing Surface...'
    tt = time.time()
    surface = Surface('./Test/mean_face.ply', form = 'ply')
    surface.load_curvature('./Test/mean_face.ply.curves.txt', curvature_index = 0)
    faceindexes = np.array((1,100,1000,100),dtype=int)[:,np.newaxis]
    curves = surface.get_face_curvatures(faceindexes)
    print 'Processing Time:', time.time() - tt
    print surface
    #surface.save('./Test/ww.ply', form = 'ply')
    #surface.save('./Test/ww.pkl', form = 'pkl')
    #surface = Surface('./Test/ww.pkl', form = 'pkl')
    surface.load_curvatures('./Test/1.ply.curves.txt',curvature_index = 1)
    print surface.curvatures.shape
    #print surface
    print 'OK'
