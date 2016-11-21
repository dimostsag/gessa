#!/usr/bin/python
"""
Helper Class for loading and saving surfaces from/to .ply files
"""

from __future__ import division
import numpy as np

class PlyReader:
   
    @classmethod
    def load_ply(cls, filename):
        V = [] 
        F = [] 
        D = []

        fh = open(filename)
        for line in fh :
            if (line.startswith('ply') or line.startswith('format') or line.startswith('comment') or line.startswith('property') or line.startswith('element') or line.startswith('end')):
                continue
            line = line.strip().split(' ')
            if line[0] == '3' : 
                face = line[1:]
                F.append(face)
            else: 
                V.append(line[:3])
                D.append(line[3])
        fh.close()
        V = np.asarray(V,dtype=float)
        F = np.asarray(F,dtype=int)
        D = np.asarray(D,dtype=float)
        return V,F,D
     
    @classmethod
    def save_ply(cls, filename, V, F, D):
        print filename
        with open(filename,'w') as fw:
            fw.write('ply\nformat ascii 1.0\ncomment VCGLIB generated\nelement vertex ' + str(len(V)) + '\nproperty float x\nproperty float y\nproperty float z\nproperty float quality\nelement face ' + str(len(F)) + '\nproperty list uchar int vertex_indices\nend_header\n')
            temp_ind = 0
            V = V.astype(str)
            F = F.astype(str)
            V = V.tolist()
            F = F.tolist()
            for v in V:
                fw.write(' '.join(v) + ' ' + str(D[temp_ind]) + '\n')
                temp_ind += 1
            for f in F:
                fw.write(str(len(f)) + ' ' + ' '.join(f) + '\n')
        return filename

if __name__ == '__main__':
    print 'Testing PlyReader...'
    V,F,D = PlyReader.load_ply('./Test/nose_sc.ply')
    PlyReader.save_ply('./Test/nose_sc.ply', V,F,D)
    print 'OK'
