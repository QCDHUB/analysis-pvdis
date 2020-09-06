import sys,os
import numpy as np
import copy
from subprocess import Popen, PIPE, STDOUT

#--matplotlib
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.lines import Line2D
import pylab as py
import matplotlib.gridspec as gridspec

#--from scipy stack 
from scipy.integrate import fixed_quad
from scipy import interpolate

#--from tools
from tools.tools     import load,save,checkdir,lprint
from tools.config    import conf,load_config

#--from fitlib
from fitlib.resman import RESMAN

#-- from qcdlib
from qcdlib import aux

#--from local
from analysis.corelib import core
from analysis.corelib import classifier

#--from obslib
from obslib.wasym.theory import WASYM
from obslib.wasym.reader import READER

def plot_wasym(wdir,kc):

    print('\ngenerating W asymmetry from %s'%(wdir))
    load_config('%s/input.py'%wdir)
    istep=core.get_istep()
    predictions = load('%s/data/predictions-%d.dat'%(wdir,istep))
    if 'wasym' not in predictions['reactions']: return

    nrows,ncols=1,1
    fig = py.figure(figsize=(ncols*7,nrows*4))
    ax = py.subplot(nrows,ncols,1)

    conf['path2wasymtab'] = '%s/grids/grids-wasym'%os.environ['FITPACK']
    conf['aux']=aux.AUX()
    conf['datasets'] = {}
    conf['datasets']['wasym']={}
    conf['datasets']['wasym']['xlsx']={}
    conf['datasets']['wasym']['xlsx'][1000]='wasym/expdata/1000.xlsx'
    conf['datasets']['wasym']['xlsx'][1001]='wasym/expdata/1001.xlsx'
    conf['datasets']['wasym']['norm']={}
    conf['datasets']['wasym']['filters']=[]
    conf['wasym tabs']=READER().load_data_sets('wasym')
    tables = conf['wasym tabs'].keys()
    

    replicas=core.get_replicas(wdir)
    core.mod_conf(istep,replicas[0]) #--set conf as specified in istep   
   
    resman=RESMAN(nworkers=1,parallel=False,datasets=False)   #conf['pdf'] comes from this line!!!
    parman=resman.parman

    jar=load('%s/data/jar-%d.dat'%(wdir,istep))
    replicas=jar['replicas']
    parman.order=jar['order']


    data = predictions['reactions']['wasym']

    cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc)

    #--plot data
    for table in conf['wasym tabs']:
        Y = conf['wasym tabs'][table]['Y']
        values = conf['wasym tabs'][table]['value']
        #--undo scaling
        alpha  = data[table]['alpha']
        if table==1000: color,label = 'green',r'\rm{CDF(W)}'
        if table==1001: color,label = 'blue',r'\rm{D0(W)}'
        ax.errorbar(Y,values,yerr=alpha,color=color,label=label,fmt='o',ms=3.0)

    #--compute cross-section for all replicas        
    cnt=0
    for i in range(len(replicas)):
        cnt+=1
        lprint('%d/%d'%(cnt,len(replicas)))

        #parman.set_new_params(par,initial=True)

        Y = conf['wasym tabs'][1001]['Y']
        color = colors[cluster[i]]
        repdata=data[1001]['prediction-rep'][i]
        ax.plot(Y,repdata,color=color,alpha=0.5)

    ax.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=20)
    ax.plot([],[],color='red',label='JAM')
    ax.legend(frameon=False,fontsize=15)
    ax.set_xlabel(r'$y_W$',size=24)
    ax.set_ylabel(r'$A_W$',size=24)
    py.tight_layout()

    ax.set_xlim(0,3)
    ax.set_ylim(0,0.8)

    checkdir('%s/gallery'%wdir)
    filename='%s/gallery/W_asym.png'%(wdir)

    py.savefig(filename)
    print
    print 'Saving W asymmetry plot to %s'%filename


def plot_wasym_ratio(wdir,kc):

    print('\ngenerating W asymmetry from %s'%(wdir))
    load_config('%s/input.py'%wdir)
    istep=core.get_istep()
    predictions = load('%s/data/predictions-%d.dat'%(wdir,istep))
    if 'wasym' not in predictions['reactions']: return

    nrows,ncols=1,2
    fig = py.figure(figsize=(ncols*7,nrows*4))
    ax11 = py.subplot(nrows,ncols,1)
    ax12 = py.subplot(nrows,ncols,2)

    conf['path2wasymtab'] = '%s/grids/grids-wasym'%os.environ['FITPACK']
    conf['aux']=aux.AUX()
    conf['datasets'] = {}
    conf['datasets']['wasym']={}
    conf['datasets']['wasym']['xlsx']={}
    conf['datasets']['wasym']['xlsx'][1000]='wasym/expdata/1000.xlsx'
    conf['datasets']['wasym']['xlsx'][1001]='wasym/expdata/1001.xlsx'
    conf['datasets']['wasym']['norm']={}
    conf['datasets']['wasym']['filters']=[]
    conf['wasym tabs']=READER().load_data_sets('wasym')
    
    tables = conf['datasets']['wasym']['xlsx'].keys()
    replicas=core.get_replicas(wdir)
    core.mod_conf(istep,replicas[0]) #--set conf as specified in istep   
   
    resman=RESMAN(nworkers=1,parallel=False,datasets=False)   #conf['pdf'] comes from this line!!!
    parman=resman.parman

    jar=load('%s/data/jar-%d.dat'%(wdir,istep))
    replicas=jar['replicas']
    parman.order=jar['order']

    cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc)

    data = predictions['reactions']['wasym']

    cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc)

    #--get theory by seperating solutions and taking mean
    for idx in tables:
        predictions = copy.copy(data[idx]['prediction-rep'])
        del data[idx]['prediction-rep']
        del data[idx]['residuals-rep']
        for ic in range(nc):
            predictions_ic = [predictions[i] for i in range(len(predictions)) if cluster[i] == ic]
            data[idx]['thy-%d'%ic]  = np.mean(predictions_ic,axis=0)
            data[idx]['dthy-%d'%ic] = np.std(predictions_ic,axis=0)**0.5


    for idx in data:
        if idx==1000: ax,label = ax11,r'\rm{CDF(W)}'
        if idx==1001: ax,label = ax12,r'\rm{D0(W)}'
        for ic in range(nc):
            Y = conf['wasym tabs'][idx]['Y']
            color = colors[cluster[ic]]
            thy = data[idx]['thy-%d'%ic]
            ratio = data[idx]['value']/thy
            alpha = data[idx]['alpha']
            ax.errorbar(Y,ratio,yerr=alpha/thy,color=color)
            ax.text(0.8,0.9,label,fontsize=15,transform=ax.transAxes)
            ax.axhline(1,0,3,alpha=0.3,color='black')
            


    ax11.set_xlabel(r'\rm{rapidity}',size=24)
    ax12.set_xlabel(r'\rm{rapidity}',size=24)
    ax11.set_ylabel(r'\rm{data/theory}',size=24)
    py.tight_layout()

    checkdir('%s/gallery'%wdir)
    filename='%s/gallery/W_asym_ratio.png'%(wdir)

    py.savefig(filename)
    print
    print 'Saving W asymmetry plot to %s'%filename


