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
from obslib.wzrv.theory import WZRV
from obslib.wzrv.reader import READER

def plot_A_L(wdir):

    nrows,ncols=2,3
    fig = py.figure(figsize=(ncols*7,nrows*4))
    ax = py.subplot(nrows,ncols,1)

    conf['path2wzrvtab'] = '%s/grids/grids-wzrv'%os.environ['FITPACK']
    conf['aux']=aux.AUX()
    conf['datasets'] = {}
    conf['datasets']['wzrv']={}
    conf['datasets']['wzrv']['xlsx']={}
    conf['datasets']['wzrv']['xlsx'][1000]='wzrv/expdata/1000.xlsx'
    conf['datasets']['wzrv']['xlsx'][1001]='wzrv/expdata/1001.xlsx'
    conf['datasets']['wzrv']['norm']={}
    conf['datasets']['wzrv']['filters']=[]
    conf['wzrv tabs']=READER().load_data_sets('wzrv')
    tables = conf['wzrv tabs'].keys()

    print('\ngenerating A_L from %s'%(wdir))
    load_config('%s/input.py'%wdir)
    istep=core.get_istep()
    replicas=core.get_replicas(wdir)
    core.mod_conf(istep,replicas[0]) #--set conf as specified in istep   
   
    resman=RESMAN(nworkers=1,parallel=False,datasets=False)
    parman=resman.parman

    jar=load('%s/data/jar-%d.dat'%(wdir,istep))
    replicas=jar['replicas']
    parman.order=jar['order']

    predictions = load('%s/data/predictions-%d.dat'%(wdir,istep))
    data = predictions['reactions']['wzrv']
  
    #--plot data
    for table in conf['wzrv tabs']:
        values = conf['wzrv tabs'][table]['value']
        alpha  = data[table]['alpha']
        if table == 1000: color='blue'
        if table == 1001: color='red'
        if 'eta' in conf['wzrv tabs'][table]:
            eta = conf['wzrv tabs'][table]['eta']
            ax.errorbar(eta,values,yerr=alpha,color=color,fmt='o',ms=5.0)
        else: 
            eta = (conf['wzrv tabs'][table]['eta_min'] + conf['wzrv tabs'][table]['eta_max'])/2.0
            eta_min = conf['wzrv tabs'][table]['eta_min']
            eta_max = conf['wzrv tabs'][table]['eta_max']
            xerr = np.zeros((2,len(eta)))
            #for i in range(len(eta)):
            #    xerr[0][i] = eta_max[i] - eta[i]
            #    xerr[1][i] = eta[i] - eta_min[i]
            ax.errorbar(eta,values,xerr=xerr,yerr=alpha,color=color,label=label,fmt='o',ms=5.0)

    #--compute cross-section for all replicas        
    cnt=0
    for i in range(len(replicas)):
        cnt+=1
        lprint('%d/%d'%(cnt,len(replicas)))

        #parman.set_new_params(par,initial=True)

        for table in [1000,1001]:
            if table == 1000: color='blue'
            if table == 1001: color='red'
            if 'eta' in conf['wzrv tabs'][table]: eta = conf['wzrv tabs'][table]['eta']
            else: eta = (conf['wzrv tabs'][table]['eta_min'] + conf['wzrv tabs'][table]['eta_max'])/2.0
            repdata=data[table]['prediction-rep'][i]
            
            ax.plot(eta,repdata,color=color,alpha=0.3)

    #ax.legend()

    ax.plot(np.linspace(-2,2,100),np.zeros(100),'k--',alpha=0.5)
    ax.set_ylabel(r'$A_L$',size=24)
    ax.set_xlabel(r'$\eta$',size=24)

    ax.set_xlim(-1.6,1.5)
    ax.set_ylim(-0.7,0.7)
    ax.text(-1.5,-0.35,r'\rm{$W^+$}',fontsize=20)
    ax.text(-1.5, 0.2, r'\rm{$W^-$}',fontsize=20)
    py.tight_layout()

    checkdir('%s/gallery'%wdir)
    filename='%s/gallery/A_L.png'%(wdir)

    py.savefig(filename)
    print
    print 'Saving A_L plot to %s'%filename




