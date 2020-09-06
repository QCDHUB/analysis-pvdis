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

def plot_wzrv(wdir):

    print('\ngenerating WZRV from %s'%(wdir))
    load_config('%s/input.py'%wdir)
    istep=core.get_istep()
    predictions = load('%s/data/predictions-%d.dat'%(wdir,istep))
    if 'wzrv' not in predictions['reactions']: return

    nrows,ncols=2,3
    fig = py.figure(figsize=(ncols*7,nrows*4))
    ax11 = py.subplot(nrows,ncols,1)
    ax12 = py.subplot(nrows,ncols,2)
    ax13 = py.subplot(nrows,ncols,3)
    ax21 = py.subplot(nrows,ncols,4)
    ax22 = py.subplot(nrows,ncols,5)
    ax23 = py.subplot(nrows,ncols,6)

    conf['path2wzrvtab'] = '%s/grids/grids-wzrv'%os.environ['FITPACK']
    conf['aux']=aux.AUX()
    conf['datasets'] = {}
    conf['datasets']['wzrv']={}
    conf['datasets']['wzrv']['xlsx']={}
    conf['datasets']['wzrv']['xlsx'][2000]='wzrv/expdata/2000.xlsx'
    conf['datasets']['wzrv']['xlsx'][2003]='wzrv/expdata/2003.xlsx'
    conf['datasets']['wzrv']['xlsx'][2006]='wzrv/expdata/2006.xlsx'
    conf['datasets']['wzrv']['xlsx'][2007]='wzrv/expdata/2007.xlsx'
    #conf['datasets']['wzrv']['xlsx'][2008]='wzrv/expdata/2008.xlsx'
    conf['datasets']['wzrv']['xlsx'][2009]='wzrv/expdata/2009.xlsx'
    conf['datasets']['wzrv']['xlsx'][2010]='wzrv/expdata/2010.xlsx'
    conf['datasets']['wzrv']['xlsx'][2011]='wzrv/expdata/2011.xlsx'
    conf['datasets']['wzrv']['xlsx'][2012]='wzrv/expdata/2012.xlsx'
    conf['datasets']['wzrv']['xlsx'][2013]='wzrv/expdata/2013.xlsx'
    conf['datasets']['wzrv']['xlsx'][2014]='wzrv/expdata/2014.xlsx'
    conf['datasets']['wzrv']['xlsx'][2015]='wzrv/expdata/2015.xlsx'
    conf['datasets']['wzrv']['norm']={}
    conf['datasets']['wzrv']['filters']=[]
    conf['wzrv tabs']=READER().load_data_sets('wzrv')

    replicas=core.get_replicas(wdir)
    core.mod_conf(istep,replicas[0]) #--set conf as specified in istep   
  
    tables = conf['datasets']['wzrv']['xlsx'].keys()
 
    resman=RESMAN(nworkers=1,parallel=False,datasets=False)
    parman=resman.parman

    jar=load('%s/data/jar-%d.dat'%(wdir,istep))
    replicas=jar['replicas']
    parman.order=jar['order']


    data = predictions['reactions']['wzrv']
  
    #--plot data
    for table in tables:
        values = conf['wzrv tabs'][table]['value']
        alpha  = data[table]['alpha']
        if table==2000: ax,color,label = ax11,'darkblue',r'$\rm{D0(e)}$'
        if table==2003: ax,color,label = ax11,'green',r'$\rm{CDF(e)}$'
        if table==2006: ax,color,label = ax11,'cyan',r'$\rm{D0(\mu)}$'
        if table==2007: ax,color,label = ax21,'green',r'$\rm{ATLAS(2012)}$'
        if table==2015: ax,color,label = ax22,'green',r'$\rm{ATLAS(2011)}$'
        if table==2009: ax,color,label = ax23,'green',r'$\rm{ATLAS(2010)}$'
        if table==2010: ax,color,label = ax21,'blue',r'$\rm{CMS}$'
        if table==2011: ax,color,label = ax12,'green',r'$\rm{CMS(\mu)(2011)}$'
        if table==2012: ax,color,label = ax13,'green',r'$\rm{CMS(e)(2011)}$'
        if table==2013: ax,color,label = ax12,'blue',r'$\rm{CMS(e)(2010)}$'
        if table==2014: ax,color,label = ax12,'purple',r'$\rm{CMS(\mu)(2010)}$'
        if 'eta' in conf['wzrv tabs'][table]:
            eta = conf['wzrv tabs'][table]['eta']
            ax.errorbar(eta,values,yerr=alpha,color=color,label=label,fmt='o',ms=5.0,capsize=3.0)

        else: 
            eta = (conf['wzrv tabs'][table]['eta_min'] + conf['wzrv tabs'][table]['eta_max'])/2.0
            eta_min = conf['wzrv tabs'][table]['eta_min']
            eta_max = conf['wzrv tabs'][table]['eta_max']
            xerr = np.zeros((2,len(eta)))
            #for i in range(len(eta)):
            #    xerr[0][i] = eta_max[i] - eta[i]
            #    xerr[1][i] = eta[i] - eta_min[i]
            ax.errorbar(eta,values,yerr=alpha,color=color,label=label,fmt='o',ms=5.0,capsize=3.0)

    #--compute cross-section for all replicas        
    cnt=0
    for i in range(len(replicas)):
        cnt+=1
        lprint('%d/%d'%(cnt,len(replicas)))

        #parman.set_new_params(par,initial=True)

        #for table in [2000,2007,2009,2010,2008,2011,2012]:
        for table in [2000,2007,2009,2010,2011,2012,2015]:
            if table not in tables: continue
            if table==2000: ax = ax11
            if table==2007: ax = ax21
            if table==2010: ax = ax21
            if table==2011: ax = ax12
            if table==2012: ax = ax13
            if table==2015: ax = ax22
            if table==2009: ax = ax23
            eta0, eta1 = [], []
            repdata0, repdata1 = [], []
            boson = conf['wzrv tabs'][table]['boson']
            #--separate W+ data from W- data
            for j in range(len(boson)):
                if boson[j]=='W':
                    if 'eta' in conf['wzrv tabs'][table]: eta = conf['wzrv tabs'][table]['eta']
                    else: eta = (conf['wzrv tabs'][table]['eta_min'] + conf['wzrv tabs'][table]['eta_max'])/2.0
                    repdata=data[table]['prediction-rep'][i]
                    break
                if boson[j]=='W+':
                    if 'eta' in conf['wzrv tabs'][table]: eta0.append(conf['wzrv tabs'][table]['eta'][j])
                    else: eta0.append((conf['wzrv tabs'][table]['eta_min'][j] + conf['wzrv tabs'][table]['eta_max'][j])/2.0)
                    repdata0.append(data[table]['prediction-rep'][i][j])
                if boson[j]=='W-':
                    if 'eta' in conf['wzrv tabs'][table]: eta1.append(conf['wzrv tabs'][table]['eta'][j])
                    else: eta1.append((conf['wzrv tabs'][table]['eta_min'][j] + conf['wzrv tabs'][table]['eta_max'][j])/2.0)
                    repdata1.append(data[table]['prediction-rep'][i][j])

            if boson[0]=='W':  ax.plot(eta,repdata,color='red',alpha=0.3)
            else:  
                ax.plot(eta0,repdata0,color='red',alpha=0.3)
                ax.plot(eta1,repdata1,color='red',alpha=0.3)

    
    ax11.plot([],[],color='red',label='JAM')
    for ax in [ax11,ax12,ax13,ax21,ax22,ax23]:
        ax.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=20)
        ax.legend(fontsize=12,frameon=False)

    ax11.set_ylabel(r'$A_l$',size=24)
    ax21.set_ylabel(r'$\frac{d\sigma_W}{d|\eta|}$',size=24)
    ax21.set_xlabel(r'$\rm{|\eta|}$',size=24)
    ax22.set_xlabel(r'$\rm{|\eta|}$',size=24)
    ax23.set_xlabel(r'$\rm{|\eta|}$',size=24)

    ax11.axhline(0,0,3,alpha=0.3,color='black')
    ax11.set_xlim(0.0,3.0)
    ax11.set_ylim(-0.5,0.28)
    ax12.set_xlim(-0.1,2.5)
    ax12.set_ylim(0.05,0.30)
    ax13.set_xlim(-0.1,2.5)
    ax13.set_ylim(0.00,0.27)
    ax21.set_xlim(-0.3,2.5)
    ax21.set_ylim(300,800)
    ax22.set_xlim(-0.3,2.5)
    ax22.set_ylim(300,700)
    ax23.set_xlim(-0.3,2.5)
    ax23.set_ylim(300,700)

    ax11.text(0.2,-0.35,r'\rm{RS = 1960 GeV}',fontsize=20)
    ax11.text(0.2,-0.45, r'\rm{$p_T$ $>$ 25 GeV}',fontsize=20)
    ax12.text(1.6,0.10,r'\rm{RS = 7000 GeV}',fontsize=20)
    ax12.text(1.6,0.07,r'\rm{$p_T$ $>$ 25 GeV}',fontsize=20)
    ax13.text(1.6,0.05,r'\rm{RS = 7000 GeV}',fontsize=20)
    ax13.text(1.6,0.02,r'\rm{$p_T$ $>$ 35 GeV}',fontsize=20)
    ax21.text(0.5,350,r'\rm{RS = 8000 GeV}',fontsize=20)
    ax21.text(0.5,310,r'\rm{$p_T$ $>$ 25 GeV}',fontsize=20)
    ax21.text(-0.2,650,r'\rm{$W^+$}',fontsize=20)
    ax21.text(-0.2,500,r'\rm{$W^-$}',fontsize=20)
    ax22.text(0.0,350,r'\rm{RS = 7000 GeV}',fontsize=20)
    ax22.text(0.0,310,r'\rm{$p_T$ $>$ 25 GeV}',fontsize=20)
    ax22.text(-0.2,550,r'\rm{$W^+$}',fontsize=20)
    ax22.text(-0.2,425,r'\rm{$W^-$}',fontsize=20)
    ax23.text(0.0,350,r'\rm{RS = 7000 GeV}',fontsize=20)
    ax23.text(0.0,310,r'\rm{$p_T$ $>$ 20 GeV}',fontsize=20)
    ax23.text(-0.2,600,r'\rm{$W^+$}',fontsize=20)
    ax23.text(-0.2,425,r'\rm{$W^-$}',fontsize=20)
    py.tight_layout()

    checkdir('%s/gallery'%wdir)
    filename='%s/gallery/wzrv.png'%(wdir)

    py.savefig(filename)
    print
    print 'Saving wzrv plot to %s'%filename


def plot_wzrv_ratio(wdir,kc):

    print('\ngenerating WZRV ratio from %s'%(wdir))
    load_config('%s/input.py'%wdir)
    istep=core.get_istep()
    predictions = load('%s/data/predictions-%d.dat'%(wdir,istep))
    if 'wzrv' not in predictions['reactions']: return

    nrows,ncols=2,5
    fig = py.figure(figsize=(ncols*7,nrows*4))
    ax11 = py.subplot(nrows,ncols,1)
    ax12 = py.subplot(nrows,ncols,2)
    ax13 = py.subplot(nrows,ncols,3)
    ax14 = py.subplot(nrows,ncols,4)
    ax15 = py.subplot(nrows,ncols,5)
    ax21 = py.subplot(nrows,ncols,6)
    ax22 = py.subplot(nrows,ncols,7)
    ax23 = py.subplot(nrows,ncols,8)
    ax24 = py.subplot(nrows,ncols,9)
    ax25 = py.subplot(nrows,ncols,10)

    conf['path2wzrvtab'] = '%s/grids/grids-wzrv'%os.environ['FITPACK']
    conf['aux']=aux.AUX()
    conf['datasets'] = {}
    conf['datasets']['wzrv']={}
    conf['datasets']['wzrv']['xlsx']={}
    conf['datasets']['wzrv']['xlsx'][2000]='wzrv/expdata/2000.xlsx'
    conf['datasets']['wzrv']['xlsx'][2003]='wzrv/expdata/2003.xlsx'
    conf['datasets']['wzrv']['xlsx'][2006]='wzrv/expdata/2006.xlsx'
    conf['datasets']['wzrv']['xlsx'][2007]='wzrv/expdata/2007.xlsx'
    #conf['datasets']['wzrv']['xlsx'][2008]='wzrv/expdata/2008.xlsx'
    conf['datasets']['wzrv']['xlsx'][2009]='wzrv/expdata/2009.xlsx'
    conf['datasets']['wzrv']['xlsx'][2010]='wzrv/expdata/2010.xlsx'
    conf['datasets']['wzrv']['xlsx'][2011]='wzrv/expdata/2011.xlsx'
    conf['datasets']['wzrv']['xlsx'][2012]='wzrv/expdata/2012.xlsx'
    conf['datasets']['wzrv']['xlsx'][2013]='wzrv/expdata/2013.xlsx'
    conf['datasets']['wzrv']['xlsx'][2014]='wzrv/expdata/2014.xlsx'
    conf['datasets']['wzrv']['xlsx'][2015]='wzrv/expdata/2015.xlsx'
    conf['datasets']['wzrv']['norm']={}
    conf['datasets']['wzrv']['filters']=[]
    conf['wzrv tabs']=READER().load_data_sets('wzrv')

    replicas=core.get_replicas(wdir)
    core.mod_conf(istep,replicas[0]) #--set conf as specified in istep   
  
    tables = conf['datasets']['wzrv']['xlsx'].keys()
 
    resman=RESMAN(nworkers=1,parallel=False,datasets=False)
    parman=resman.parman

    jar=load('%s/data/jar-%d.dat'%(wdir,istep))
    replicas=jar['replicas']
    parman.order=jar['order']

    cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc)

    data = predictions['reactions']['wzrv']
 
    #--get theory by seperating solutions and taking mean
    for idx in tables:
        predictions = copy.copy(data[idx]['prediction-rep'])
        del data[idx]['prediction-rep']
        del data[idx]['residuals-rep']
        for ic in range(nc):
            predictions_ic = [predictions[i] for i in range(len(predictions)) if cluster[i] == ic]
            data[idx]['thy-%d'%ic]  = np.mean(predictions_ic, axis = 0)
            data[idx]['dthy-%d'%ic] = np.std(predictions_ic, axis=0)**0.5

    for idx in data:
        if idx==2003: continue
        if idx==2000: ax,label = ax11,r'$\rm{D0(e)}$'
        if idx==2006: ax,label = ax12,r'$\rm{D0(\mu)}$'
        if idx==2007: ax,label = ax13,r'$\rm{ATLAS(2012)}$'
        if idx==2015: ax,label = ax14,r'$\rm{ATLAS(2011)}$'
        if idx==2009: ax,label = ax15,r'$\rm{ATLAS(2010)}$'
        if idx==2010: ax,label = ax21,r'$\rm{CMS}$'
        if idx==2011: ax,label = ax22,r'$\rm{CMS(\mu)(2011)}$'
        if idx==2012: ax,label = ax23,r'$\rm{CMS(e)(2011)}$'
        if idx==2013: ax,label = ax24,r'$\rm{CMS(e)(2010)}$'
        if idx==2014: ax,label = ax25,r'$\rm{CMS(\mu)(2010)}$'
        for ic in range(nc):
            color = colors[cluster[ic]]
            eta0, eta1 = [], []
            thy0, thy1, ratio0, ratio1, alpha0, alpha1 = [], [], [], [], [], []
            boson = conf['wzrv tabs'][idx]['boson']
            #--separate W+ data from W- data
            for j in range(len(boson)):
                if boson[j]=='W':
                    if 'eta' in conf['wzrv tabs'][idx]: eta = conf['wzrv tabs'][idx]['eta']
                    else: eta = (conf['wzrv tabs'][idx]['eta_min'] + conf['wzrv tabs'][idx]['eta_max'])/2.0
                    thy   = data[idx]['thy-%d'%ic]
                    ratio = data[idx]['value']/thy
                    alpha = data[idx]['alpha']
                    break
                if boson[j]=='W+':
                    if 'eta' in conf['wzrv tabs'][idx]: eta0.append(conf['wzrv tabs'][idx]['eta'][j])
                    else: eta0.append((conf['wzrv tabs'][idx]['eta_min'][j] + conf['wzrv tabs'][idx]['eta_max'][j])/2.0)
                    thy0.append(data[idx]['thy-%d'%ic][j])
                    ratio0.append(data[idx]['value'][j]/thy0[j])
                    alpha0.append(data[idx]['alpha'][j])
                if boson[j]=='W-':
                    if 'eta' in conf['wzrv tabs'][idx]: eta1.append(conf['wzrv tabs'][idx]['eta'][j])
                    else: eta1.append((conf['wzrv tabs'][idx]['eta_min'][j] + conf['wzrv tabs'][idx]['eta_max'][j])/2.0)
                    thy1.append(data[idx]['thy-%d'%ic][j])
                    ratio1.append(data[idx]['value'][j]/data[idx]['thy-%d'%ic][j])
                    alpha1.append(data[idx]['alpha'][j])

            if boson[0]=='W':  ax.errorbar(eta,ratio,yerr=alpha/thy,color=color)
            else:  
                ax.errorbar(eta0,ratio0,yerr=np.array(alpha0)/np.array(thy0),color=color)
                ax.errorbar(eta1,ratio1,yerr=np.array(alpha1)/np.array(thy1),color=color)
            ax.text(0.8,0.9,label,fontsize=15,transform = ax.transAxes)
            ax.axhline(1,0,3,alpha=0.3,color='black')
             
 
    ax11.set_ylabel(r'$data/theory$',size=24)
    ax21.set_ylabel(r'$data/theory$',size=24)
    ax21.set_xlabel(r'$\rm{|\eta|}$',size=24)
    ax22.set_xlabel(r'$\rm{|\eta|}$',size=24)
    ax23.set_xlabel(r'$\rm{|\eta|}$',size=24)
    ax24.set_xlabel(r'$\rm{|\eta|}$',size=24)
    ax25.set_xlabel(r'$\rm{|\eta|}$',size=24)


    py.tight_layout()

    checkdir('%s/gallery'%wdir)
    filename='%s/gallery/wzrv_ratio.png'%(wdir)

    py.savefig(filename)
    print
    print 'Saving wzrv ratio plot to %s'%filename


