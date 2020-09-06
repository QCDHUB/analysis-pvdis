#!/usr/bin/env python
from tools.config import load_config,conf
from fitlib.resman import RESMAN
import numpy as np

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


def plot_off(PLOT,kc,mode=0,iso=True,name='',compare=True,nrep=None):

    #--mode 0: plot each replica
    #--mode 1: plot average and standard deviation of replicas

    nrows,ncols=1,1
    fig = py.figure(figsize=(ncols*6,nrows*4))
    ax11 = py.subplot(nrows,ncols,1) 

    for plot in PLOT: 
        wdir, q2, color, style, label, alpha = plot[0], plot[1], plot[2], plot[3], plot[4], plot[5]
        replicas = core.get_replicas(wdir)

        load_config('%s/input.py'%wdir)

        istep = core.get_istep()
        core.mod_conf(istep,replicas[0])
        conf['idis grid'] = 'prediction'
        conf['datasets']['idis'] = {_:{} for _ in ['xlsx','norm']}
        resman=RESMAN(parallel=False,datasets=False)
        parman = resman.parman
        cluster,colors,nc,cluster_order= classifier.get_clusters(wdir,istep,kc) 

        replicas = core.get_replicas(wdir)

        jar = load('%s/data/jar-%d.dat'%(wdir,istep))
        parman.order = jar['order']
        replicas = jar['replicas']
        resman.setup_idis()
        
        idis=resman.idis_thy
        idis._update()
        pdf=conf['pdf']
        
        if 'off' in conf: off = conf['off']
        else:
            print('Offshell corrections not present.')
            return

        ax11.plot([],[],label=label,color=color)
        ##############################################
        #--plot offshell
        ##############################################
        off = conf['off']
        X1   = 10**np.linspace(-4,-1,100)
        X2   = np.linspace(0.1,0.98,100)
        X    = np.append(X1,X2)
        Q2   = np.ones(X.size)*q2
        cnt = 0
        df = []
        for par in replicas:
           
            if nrep != None and cnt >= nrep: break 
            #if len(PLOT) == 1: color = colors[cluster[cnt]]
    
            lprint('Generating offshell %s/%s'%(cnt+1,len(replicas))) 
            parman.set_new_params(par,initial=True) 
            #--isospin symmetry
            if iso:
                df.append(off.get_offshell(X,Q2,'p','F2'))
            else:
                F2p  = idis.get_stf(X,Q2,stf='F2',tar='p')
                F2n  = idis.get_stf(X,Q2,stf='F2',tar='n')
                pof2 = off.get_offshell(X,Q2,'p','F2')
                nof2 = off.get_offshell(X,Q2,'n','F2')
                df.append((F2p*pof2+F2n*nof2)/(F2p+F2n))

            if mode==0: ax11.plot(X,df[cnt],color=color,alpha=alpha)
            cnt += 1
   
        if mode == 1:
            mean = np.mean(np.array(df),axis=0)
            std  = np.std(np.array(df),axis=0)
            ax11.plot(X,mean,color=color)
            ax11.fill_between(X,mean-std,mean+std,color=color,alpha=0.5)

        print
 
    ##############################################
    X1   = 10**np.linspace(-4,-1,100)
    X2   = np.linspace(0.1,0.98,100)
    X    = np.append(X1,X2)
    if compare:
        #--CJ15 
        C =-3.6735
        x0= 5.7717e-2
        x1=0.36419
        dfcj=C*(X-x0)*(X-x1)*(1+x0-X)
        ax11.plot(X,dfcj,'b--',label=r'$\rm CJ15$')
        #--KP 
        C = 8.10
        x0= 0.448
        x1= 0.05
        dfcj=C*(X-x0)*(X-x1)*(1+x0-X)
        ax11.plot(X,dfcj,'g--',label=r'$\rm KP$')

    ax11.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=15)

    ax11.set_ylim(-1.0,1.0)
    #ax11.set_ylim(-2.0,2.0)

    ax11.set_xlim(0,1)
    ax11.set_ylabel(r'$\delta f^0$',size=30)
    ax11.set_xlabel(r'$x$'         ,size=30)
    ax11.legend(frameon=False,loc='upper left',fontsize=15)
    ax11.axhline(0,alpha=0.5,color='k',ls='--')
    if 'dsmf type' in conf:
        if conf['dsmf type']=='paris':    ax11.text(0.1,0.05,r'$Paris$'  ,size=20,transform=ax11.transAxes)
        if conf['dsmf type']=='av18':     ax11.text(0.1,0.05,r'$AV18$'   ,size=20,transform=ax11.transAxes)
        if conf['dsmf type']=='cdbonn':   ax11.text(0.1,0.05,r'$CD-Bonn$',size=20,transform=ax11.transAxes)
        if conf['dsmf type']=='wjc-1':    ax11.text(0.1,0.05,r'$WJC-1$'  ,size=20,transform=ax11.transAxes)
        if conf['dsmf type']=='wjc-2':    ax11.text(0.1,0.05,r'$WJC-2$'  ,size=20,transform=ax11.transAxes)
       
    ax11.text(0.1,0.1,r'$Q^2=%s{\rm~GeV^2}$'%q2,size=20,transform=ax11.transAxes)

 
    py.tight_layout()
    filename = '%s/gallery/off'%PLOT[0][0]
    if mode == 1: filename += '-bands'
    filename += name
    filename += '.png'
    print('Saving figures to %s'%filename)
    py.savefig(filename)
    
    
    
    








