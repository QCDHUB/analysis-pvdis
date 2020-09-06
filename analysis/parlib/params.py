import os
import numpy as np

import matplotlib
matplotlib.use('Agg')
import pylab as py


#--from tools
from tools.tools     import checkdir,save,load
import tools.config
from tools.config    import load_config, conf, options
from tools.inputmod  import INPUTMOD

#--from local
from analysis.corelib import core
from analysis.corelib import classifier


def plot_params(wdir,dist,kc,histogram=False):

    #--histogram: If False, plot point by point.  If True, plot histogram.

    load_config('%s/input.py'%wdir)
    istep=core.get_istep()
    replicas = core.get_replicas(wdir) 
    core.mod_conf(istep,replicas[0])

    clusters,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc)

    _order = replicas[0]['order'][istep]

    #--get correct order from dist
    order  = []
    idx    = []
    for i in range(len(_order)):
        if _order[i][1] != dist: continue
        order.append(_order[i][2])
        idx.append(i)

    #--get correct params from dist
    params = np.zeros((len(order),len(replicas)))
    for i in range(len(order)):
        for j in range(len(replicas)):
            params[i][j] = replicas[j]['params'][istep][idx[i]]

    #--create plot with enough space for # of parameters
    nrows, ncols = np.ceil(len(order)/5.0), 5
    fig = py.figure(figsize=(ncols*7,nrows*4))
    X = np.linspace(1,len(replicas),len(replicas))

    #--create plot
    for i in range(len(order)):
        ax = py.subplot(nrows,ncols, i+1)
        ax.set_title('%s'%(order[i]), size=20)
        for j in range(nc):
            color  = colors[clusters[j]]
            par = [params[i][k] for k in range(len(params[i])) if clusters[k]==j]
            mean = np.mean(par)
            std  = np.std(par)
            if histogram:
                ax.hist(par,color=color,alpha=0.6,edgecolor='black')
                ax.axvline(mean,ymin=0,ymax=1,ls='--',color=color,alpha=0.8)
                ax.axvspan(mean-std,mean+std,alpha=0.1,color=color)
                if j==0:
                    ax.text(0.77,0.95,'mean:'%mean,transform=ax.transAxes,size=10)
                    ax.text(0.77,0.90,'std:'%std,  transform=ax.transAxes,size=10)
                    ax.text(0.87,0.95,'%6.5f'%mean,transform=ax.transAxes,size=10)
                    ax.text(0.87,0.90,'%6.5f'%std, transform=ax.transAxes,size=10)
            else:
                ax.scatter(X,par,color=color) 
                ax.axhline(mean,xmin=0,xmax=1,ls='--',color=color,alpha=0.8)
                ax.axhspan(mean-std,mean+std,alpha=0.1,color=color)

    if histogram: filename='%s/gallery/%s-params-hist.png'%(wdir,dist)
    else:         filename='%s/gallery/%s-params.png'%(wdir,dist)
    checkdir('%s/gallery'%wdir)
    py.savefig(filename)
    print 'Saving figure to %s'%filename
     



