#!/usr/bin/env python
import os
from tools.config import load_config,conf
from fitlib.resman import RESMAN
import numpy as np
import pandas as pd

#--matplotlib
import matplotlib
matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
matplotlib.rc('text',usetex=True)
import pylab  as py
from matplotlib.lines import Line2D

#--from tools
from tools.tools import load,lprint

#--from corelib
from analysis.corelib import core,classifier

def plot_sin2w(PLOT,kc,mode=0,name='',nrep=None):

    #--mode 0: plot each replica
    #--mode 1: plot average and standard deviation of replicas

    nrows,ncols=1,1
    fig = py.figure(figsize=(ncols*6,nrows*4))
    ax11 = py.subplot(nrows,ncols,1) 

    for plot in PLOT: 
        wdir, color, style, label, alpha = plot[0], plot[2], plot[3], plot[4], plot[5]
        replicas = core.get_replicas(wdir)

        load_config('%s/input.py'%wdir)

        istep = core.get_istep()
        core.mod_conf(istep,replicas[0])
        resman=RESMAN(parallel=False,datasets=False)
        parman = resman.parman
        cluster,colors,nc,cluster_order= classifier.get_clusters(wdir,istep,kc) 

        replicas = core.get_replicas(wdir)

        jar = load('%s/data/jar-%d.dat'%(wdir,istep))
        parman.order = jar['order']
        replicas = jar['replicas']
        
        if 'eweak' not in conf['params']:
            print('Electoweak parameters not present.')
            return


        #--plot EIC kinematics
        EIC = pd.read_excel('%s/database/EIC/expdata/3000.xlsx'%os.environ['FITPACK']).to_dict(orient='list')
        Qmin = np.sqrt(np.min(EIC['Q2']))
        Qmax = np.sqrt(np.max(EIC['Q2']))
        ax11.axvspan(Qmin,Qmax,0,0.2,alpha=0.2,color='darkcyan')
        ##############################################
        #--plot offshell
        ##############################################
        weak = conf['eweak']
        Q    = np.geomspace(1e-4,1e4,500)
        where = []
        for i in range(len(Q)):
            if Q[i] < Qmin:   where.append(0)
            elif Q[i] > Qmax: where.append(0)
            else:             where.append(1)
        cnt = 0
        sin2w = []
        for par in replicas:
           
            if nrep != None and cnt >= nrep: break 
            if len(PLOT) == 1: color = colors[cluster[cnt]]
    
            lprint('Generating sin2w %s/%s'%(cnt+1,len(replicas))) 
            parman.set_new_params(par,initial=True)
            _sin2w = [weak.get_sin2w(q**2) for q in Q]
            sin2w.append(_sin2w)

            if mode==0: ax11.plot(Q,sin2w[cnt],color=color,alpha=alpha)
            cnt += 1
   
        if mode == 1:
            mean = np.mean(np.array(sin2w),axis=0)
            std  = np.std(np.array(sin2w),axis=0)
            ax11.plot(Q,mean,color='black')
            ax11.fill_between(Q,mean-std,mean+std,color=color,alpha=alpha,where=where,label=label)

        print
 
    ##############################################

    #--plot other data points (by eye)
    #--nu-DIS
    ax11.errorbar(10**0.65,0.24075,yerr = 0.2425-0.24075, marker='o',capsize=3,color='black')
    #--PVDIS
    ax11.errorbar(10**0.02,0.2355,yerr = 0.240-0.2355, marker='o',capsize=3,color='black')
    #--E158
    ax11.errorbar(10**(-0.8),0.2405,yerr = 0.242-0.2405, marker='o',capsize=3,color='black')
    #--SoLID
    ax11.errorbar(10**(0.4),0.230,yerr = 0.2305-0.230, marker='o',capsize=3,color='black',fillstyle='none')

    ax11.text(5.0e0,0.226,r'\textrm{EIC}',size=20)
    ax11.text(8e0  ,0.24075, r'\textrm{$\nu$-DIS*}',size=16)
    ax11.text(1e-1 ,0.23550, r'\textrm{PVDIS}'     ,size=16)
    ax11.text(3e-2 ,0.24050, r'\textrm{E158}'      ,size=16)
    ax11.text(4e0  ,0.23000, r'\textrm{SoLID}'     ,size=16)

    ax11.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=20)

    ax11.set_ylim(0.224,0.246)

    ax11.set_xlim(1e-3,1e3)
    ax11.semilogx()

    #ax11.text(0.05,0.85,r'\textrm{\textbf{JAM+EIC}}',transform=ax11.transAxes,size=30)
    ax11.text(0.05,0.85,r'\textrm{\textbf{JAM}}',transform=ax11.transAxes,size=30)
    ax11.text(0.05,0.05,r'\boldmath$\sin^2(\theta_W)$',transform=ax11.transAxes,size=30)
    ax11.set_xlabel(r'\boldmath$Q~(\rm{GeV})$',size=30)
    #ax11.legend(handles,labels,loc=(0.02,0.35), fontsize = 20, frameon = 0, handletextpad = 0.3, handlelength = 1.0)
    #ax11.legend(loc=(0.02,0.22), fontsize = 20, frameon = 0, handletextpad = 0.3, handlelength = 1.0)
       
    py.tight_layout()
    filename = '%s/gallery/sin2w'%PLOT[0][0]
    if mode == 1: filename += '-bands'
    filename += name
    filename += '.png'
    print('Saving figures to %s'%filename)
    py.savefig(filename)
    
    
    
    








