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


def plot_ht(PLOT,kc,mode=0,name='',nrep=None):

    #--mode 0: plot each replica
    #--mode 1: plot average and standard deviation of replicas

    nrows,ncols=1,1
    fig = py.figure(figsize=(ncols*6,nrows*4))
    ax11 = py.subplot(nrows,ncols,1) 

    for plot in PLOT: 
        wdir, Q2, color, style, label, alpha = plot[0], plot[1], plot[2], plot[3], plot[4], plot[5]
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

        if 'ht4' in conf: ht4 = conf['ht4']
        else:
            print('Higher twist corrections not present.')
            return       

        ht_type = 'mult'
        if 'ht type' in conf: ht_type = conf['ht type']

        ##############################################
        #--plot ht
        ##############################################
        X1=10**np.linspace(-4,-1,100)
        X2=np.linspace(0.1,0.99,100)
        X=np.append(X1,X2)
        Q2=1.0
        cnt = 0
        F2p, F2n = [], []
        for par in replicas:
            if nrep != None and cnt >= nrep: break
            lprint('Generating ht %s/%s'%(cnt+1,len(replicas))) 
            parman.set_new_params(par,initial=True)
            F2p.append(ht4.get_ht(X,Q2,'p','F2'))
            F2n.append(ht4.get_ht(X,Q2,'n','F2'))
            if mode==0:
                ax11.plot(X,F2p[cnt],'r-',alpha=alpha)
                ax11.plot(X,F2n[cnt],'g-',alpha=alpha)
            cnt+=1

        if mode == 1:
            meanp = np.mean(np.array(F2p),axis=0)
            stdp  = np.std(np.array(F2p),axis=0)
            meann = np.mean(np.array(F2n),axis=0)
            stdn  = np.std(np.array(F2n),axis=0)
            ax11.plot(X,meanp,'r-')
            ax11.fill_between(X,meanp-stdp,meanp+stdp,color='red',alpha=0.5)
            ax11.plot(X,meann,'g-')
            ax11.fill_between(X,meann-stdn,meann+stdn,color='green',alpha=0.5)

        print 
    ##############################################
    if ht_type=='mult':
        h0 =-3.2874
        h1 = 1.9274
        h2 =-2.0701
        ht = h0*X**h1*(1+h2*X)
        ax11.plot(X,ht,'b--',label=r'$\rm CJ15$')
        ax11.set_ylim(-0.5,2)
        ax11.set_ylabel(r'$C_{\rm HT}^N$',size=30)
    elif ht_type=='add':
        ax11.set_ylim(-0.05,0.075)
        ax11.set_ylabel(r'$H^N$',size=30)

    ax11.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=15)

    ax11.set_xlim(0,1)

    ax11.plot([],[],color='r',label=r'${\rm JAM}~p$')
    ax11.plot([],[],color='g',label=r'${\rm JAM}~n$')

    ax11.legend(frameon=False,loc=2,fontsize=15)
    ax11.axhline(0,0,1,ls='--',color='black',alpha=0.5)
    if conf['tmc']=='GP':  ax11.text(0.75,0.1,r'$GP$' ,size=20,transform=ax11.transAxes)
    if conf['tmc']=='AOT': ax11.text(0.75,0.1,r'$AOT$',size=20,transform=ax11.transAxes)

    py.tight_layout()
    filename = '%s/gallery/ht'%PLOT[0][0]
    if mode == 1: filename += '-bands'
    filename += name
    filename += '.png'
    print('Saving figures to %s'%filename)
    py.savefig(filename)
    
    
    
    








