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


def plot_params(wdir,dist,kc,hist=False):

    #--hist: If False, plot point by point.  If True, plot histogram.

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

    #--sort alphabetically
    z = sorted(zip(order,params))
    order  = [z[i][0] for i in range(len(z))]
    params = [z[i][1] for i in range(len(z))]

    #--get names for organization
    names = [(order[i].split()[0],order[i].split()[1]) for i in range(len(order))]
    n0    = sorted(list(set(names[i][0] for i in range(len(names)))))
    n1    = sorted(list(set(names[i][1] for i in range(len(names)))))

    #--create plot with enough space for # of parameters
    nrows,ncols = len(n0),len(n1)
    fig = py.figure(figsize=(ncols*7,nrows*4))
    X = np.linspace(1,len(replicas),len(replicas))

    #--create plot
    for i in range(len(order)):
        j  = n0.index(names[i][0])
        k  = [names[m][1] for m in range(len(names)) if names[m][0]==n0[j]].index(names[i][1])
        idx = j*ncols + k + 1
        ax = py.subplot(nrows,ncols, idx)
        ax.set_title('%s'%(order[i]), size=30)
        for j in range(nc):
            color  = colors[clusters[j]]
            par = [params[i][k] for k in range(len(params[i])) if clusters[k]==j]
            mean = np.mean(par)
            std  = np.std(par)
            meanl = r'mean: %6.5f'%mean
            stdl  = r'std: %6.5f'%std
            if hist:
                ax.hist(par,color=color,alpha=0.6,edgecolor='black')
                ax.axvline(mean,ymin=0,ymax=1,ls='--',color=color,alpha=0.8,label=meanl)
                ax.axvspan(mean-std,mean+std,alpha=0.2,color=color,label=stdl)
            else:
                ax.scatter(X,par,color=color) 
                ax.axhline(mean,xmin=0,xmax=1,ls='--',color=color,alpha=0.8)
                ax.axhspan(mean-std,mean+std,alpha=0.2,color=color)
        ax.legend(loc='best',frameon=False,fontsize=15)
        ax.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=20)

    if hist: filename='%s/gallery/params-%s-hist.png'%(wdir,dist)
    else:         filename='%s/gallery/params-%s.png'%(wdir,dist)
    checkdir('%s/gallery'%wdir)
    py.tight_layout()
    py.savefig(filename)
    print 'Saving figure to %s'%filename
     



