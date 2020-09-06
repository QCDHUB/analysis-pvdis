#!/usr/bin/env python
import os,sys
import matplotlib
matplotlib.use('Agg')
import time
import numpy as np
import pylab as py
from tools.tools           import checkdir,save,load,lprint
from tools.config          import load_config,conf
from tools.randomstr       import id_generator
from analysis.corelib      import core
from scipy.optimize        import linprog

class OPT():

    def __init__(self,wdir,nsamples=1000,hull=True):

        #--shape of points = (# replicas, # params) (norms not included?)
        points = self.get_points(wdir)
        dim    = points.shape[1]

        #--get min and max
        pmin,pmax,mean,std=[], [], [], []
        for i in range(dim):
            pmin.append(np.min(points.T[i]))
            pmax.append(np.max(points.T[i]))
            mean.append(np.mean(points.T[i]))
            std .append(np.std(points.T[i]))
        pmin = np.array(pmin)
        pmax = np.array(pmax)
        mean = np.array(mean)
        std  = np.array(std)
        cov  = np.cov(points.T)

        grid = []
        start = time.time()
        while len(grid) < nsamples:
            lprint('Generating samples: [%s/%s]'%(len(grid)+1,nsamples))

            #x = pmin + (pmax - pmin) * np.random.rand(dim)
            #x = np.random.normal(mean,std,dim)
            x = np.random.multivariate_normal(mean,cov)

            #--check if point is in hull
            if hull:
                if self.in_hull(points,x)==True:

                    #--check if point is in limits
                    flag = False
                    for i in range(dim):
                        if x[i] < pmin[i]: flag = True
                        if x[i] > pmax[i]: flag = True
                    if flag==False: 
                        grid.append(x)

            else:

               #--check if point is in limits
               flag = False
               for i in range(dim):
                   if x[i] < pmin[i]: flag = True
                   if x[i] > pmax[i]: flag = True
               if flag==False: 
                   grid.append(x)

        end = time.time() - start
 
        print
        print('The time taken was %s'%end) 
        #--grid now has shape (nsamples, dim)
        checkdir('%s/msr-opt-priors'%wdir)
        istep = core.get_istep()
        #--template replica
        replica = core.get_replicas(wdir)[0]
        #--save new replicas
        for i in range(nsamples):
            replica['params'][istep] = grid[i]
            fname = '%s/msr-opt-priors/%s.msr'%(wdir,id_generator(12))
            save(replica,fname)
        
        print('%s replicas created and saved in %s/msr-opt-priors'%(nsamples,wdir))

    def get_points(self, wdir):
        #--get parameters from replicas
        load_config('%s/input.py'%wdir)
        istep = core.get_istep()
        replicas = core.get_replicas(wdir)
        order = replicas[0]['order'][istep]

        #--get params (ignore norms)
        params  = []
        for i in range(len(replicas)):
            params.append([])
            for j in range(len(order)):
                #if order[j][0] == 1:
                #    params[i].append(replicas[i]['params'][istep][j])
                params[i].append(replicas[i]['params'][istep][j])
                 
        return np.array(params)

    def in_hull(self,points,x):
        #--use linear algebra to test if point is in hull without constructing hull
        npts = len(points)
        dim  = len(x)
        c = np.zeros(npts)
        A = np.r_[points.T,np.ones((1,npts))]
        b = np.r_[x, np.ones(1)]
        lp = linprog(c, A_eq = A, b_eq = b)
        return lp.success


class TEST():

    def __init__(self,dim=2,nreplicas=50,nsamples=1000,dist='mult',hull=True):

        self.hull = hull
        points = np.random.rand(nreplicas,dim)
        
        #--get min and max
        pmin,pmax,mean,std=[], [], [], []
        for i in range(dim):
            pmin.append(np.min(points.T[i]))
            pmax.append(np.max(points.T[i]))
            mean.append(np.mean(points.T[i]))
            std .append(np.std(points.T[i]))
        pmin = np.array(pmin)
        pmax = np.array(pmax)
        mean = np.array(mean)
        std  = np.array(std)
        cov  = np.cov(points.T)

        grid = []
        start = time.time()
        while len(grid) < nsamples:
            lprint('Generating samples: [%s/%s]'%(len(grid)+1,nsamples))

            if dist=='flat':  x = pmin + (pmax - pmin) * np.random.rand(dim)
            if dist=='gauss': x = np.random.normal(mean,std,dim)
            if dist=='mult':  x = np.random.multivariate_normal(mean,cov)

            #--check if point is in hull
            if hull:
                if self.in_hull(points,x)==True:

                    #--check if point is in limits
                    flag = False
                    for i in range(dim):
                        if x[i] < pmin[i]: flag = True
                        if x[i] > pmax[i]: flag = True
                    if flag==False: 
                        grid.append(x)
            else:

                #--check if point is in limits
                flag = False
                for i in range(dim):
                    if x[i] < pmin[i]: flag = True
                    if x[i] > pmax[i]: flag = True
                if flag==False: 
                    grid.append(x)

        end = time.time() - start

 
        print
        print('The time taken was %s'%end) 
        #--if 2D, make plot
        if dim==2: self.plot(points, np.array(grid))

    def in_hull(self,points,x):
        #--use linear algebra to test if point is in hull without constructing hull
        npts = len(points)
        dim  = len(x)
        c = np.zeros(npts)
        A = np.r_[points.T,np.ones((1,npts))]
        b = np.r_[x, np.ones(1)]
        lp = linprog(c, A_eq = A, b_eq = b)
        return lp.success

    def plot(self,points,grid):

        nrows, ncols = 1,1
        fig = py.figure(figsize=(nrows*6,ncols*6))
        ax = py.subplot(nrows,ncols,1)

        X = points.T[0]
        Y = points.T[1]

        GX = grid.T[0]
        GY = grid.T[1]

        ax.scatter(X,Y,label='points')
        ax.scatter(GX,GY,label='grid')
        
        ax.set_xlabel(r'$X$')
        ax.set_ylabel(r'$Y$')
        ax.set_xlim(-0.2,1.2)
        ax.set_ylim(-0.2,1.2)
        ax.legend(loc='upper right') 

        if self.hull: filename = 'grid-hull.png'
        else:         filename = 'grid-no-hull.png'
        py.savefig(filename)
        print('Saving figure to %s'%filename)


