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
from obslib.zrap.theory import ZRAP
from obslib.zrap.reader import READER

def plot_zrap(wdir):

    print('\ngenerating Z-rapidity cross-section from %s'%(wdir))
    load_config('%s/input.py'%wdir)
    istep=core.get_istep()
    predictions = load('%s/data/predictions-%d.dat'%(wdir,istep))
    if 'zrap' not in predictions['reactions']: return

    nrows,ncols=1,1
    fig = py.figure(figsize=(ncols*7,nrows*4))
    ax = py.subplot(nrows,ncols,1)

    conf['path2zraptab'] = '%s/grids/grids-zrap'%os.environ['FITPACK']
    conf['aux']=aux.AUX()
    conf['datasets'] = {}
    conf['datasets']['zrap']={}
    conf['datasets']['zrap']['xlsx']={}
    conf['datasets']['zrap']['xlsx'][1000]='zrap/expdata/1000.xlsx'
    conf['datasets']['zrap']['xlsx'][1001]='zrap/expdata/1001.xlsx'
    conf['datasets']['zrap']['norm']={}
    conf['datasets']['zrap']['filters']=[]
    conf['zrap tabs']=READER().load_data_sets('zrap')
    tables = conf['zrap tabs'].keys()
    

    replicas=core.get_replicas(wdir)
    core.mod_conf(istep,replicas[0]) #--set conf as specified in istep   
   
    resman=RESMAN(nworkers=1,parallel=False,datasets=False)   #conf['pdf'] comes from this line!!!
    parman=resman.parman

    jar=load('%s/data/jar-%d.dat'%(wdir,istep))
    replicas=jar['replicas']
    parman.order=jar['order']


    data = predictions['reactions']['zrap']

    #--plot data
    for table in conf['zrap tabs']:
        Y = conf['zrap tabs'][table]['Y']
        values = conf['zrap tabs'][table]['value']
        alpha  = data[table]['alpha']
        if table==1001:
            values *= 100
            alpha  *= 100
        if table==1000: color,label = 'green',r'\rm{CDF(Z)}'
        if table==1001: color,label = 'blue',r'\rm{D0(Z)*100}'
        ax.errorbar(Y,values,xerr=0.05,yerr=alpha,color=color,label=label,fmt='o',ms=1.0)

    #--compute cross-section for all replicas        
    cnt=0
    for i in range(len(replicas)):
        cnt+=1
        lprint('%d/%d'%(cnt,len(replicas)))

        for table in conf['zrap tabs']:
            Y = conf['zrap tabs'][table]['Y']
            repdata=data[table]['prediction-rep'][i]
            #--multiply D0 data
            if table == 1001:
                repdata = repdata*100
            ax.plot(Y,repdata,color='red',alpha=0.5)

    ax.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=20)
    ax.plot([],[],color='red',label='JAM')
    ax.legend(frameon=False,fontsize=12)
    ax.set_xlim(-0.2,3)
    ax.set_ylim(0,80)
    ax.set_xlabel(r'$y_Z$',size=24)
    ax.set_ylabel(r'$N\frac{d\sigma(Z/\gamma^*)}{dy}$',size=24)
    py.tight_layout()

    checkdir('%s/gallery'%wdir)
    filename='%s/gallery/Z_xsec.png'%(wdir)

    py.savefig(filename)
    print
    print 'Saving Z cross-section plot to %s'%filename




