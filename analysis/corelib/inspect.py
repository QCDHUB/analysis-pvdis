#!/usr/bin/env python
import os,sys,shutil
import subprocess
import numpy as np

#--matplotlib
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
#matplotlib.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
matplotlib.rc('text',usetex=True)
import pylab as py


#--from tools
from tools.tools     import load,save,checkdir,lprint
from tools.config    import conf,load_config

def get_msr_inspected(wdir,limit=3,FILT=[]):

    #--FILT is a list of tuples: (param, limit, 'greater'/'less')
    #--param is the parameter that you want to use to filter
    #--limit is the limit on that parameter
    #--choose 'greater' for an upper limit, 'less' for a lower limit

    print('\nget msr inspected (filtered msr files) using %s\n'%wdir)

    replicas=sorted(os.listdir('%s/msr'%wdir))
  
    #--remove directory if it exists, then recreate it
    try:    
        shutil.rmtree('%s/msr-inspected'%wdir)
        checkdir('%s/msr-inspected'%wdir)
    except: checkdir('%s/msr-inspected'%wdir)

    X=[]
    for i in range(len(replicas)):
        lprint('progress: %d/%d'%(i+1,len(replicas)))
        replica=load('%s/msr/%s'%(wdir,replicas[i]))
        istep=sorted(replica['params'].keys())[-1] #--pick last step
        order = replica['order'][istep]
        params = replica['params'][istep]
        flag = False
        for filt in FILT:
            dist, par, _, lim = filt[0],filt[1],filt[2],filt[3]
            for j in range(len(order)):
                if order[j][1] == dist:
                    if order[j][2] == par:
                        if _ == '>':
                            if params[j] > lim: flag = True 
                        if _ == '<':
                            if params[j] < lim: flag = True
        if flag: continue

        if params is None: continue
        if istep not in replica['chi2']: data=replica['chi2']
        else:                            data=replica['chi2'][istep]
        chi2,npts=0,0
        for reaction in data: 
            for idx in  data[reaction]:
                chi2+=data[reaction][idx]['chi2']
                npts+=data[reaction][idx]['npts']
        if chi2/npts-1<limit:
            X.append(chi2/npts-1)
            cmd=['cp']
            cmd.append('%s/msr/%s'%(wdir,replicas[i]))
            cmd.append('%s/msr-inspected/%s'%(wdir,replicas[i]))
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    print()
    print('original  num. samples :%d'%len(replicas))
    print('inspected num. samples :%d'%len(X))

    nrows=1
    ncols=1
    #print np.mean(X)
    #--plot labeled residuals
    ax=py.subplot(nrows,ncols,1)
    ax.hist(X,bins=10) 
    if istep < 10: title = r'\textrm{\textbf{step0%s $\chi^2$ distribution}}'%istep
    else:          title = r'\textrm{\textbf{step%s $\chi^2$ distribution}}'%istep
    py.title(title,size=20)
    ax.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=20)
    #py.tight_layout()
    checkdir('%s/gallery'%wdir)
    py.savefig('%s/gallery/chi2-dist-inspect.png'%(wdir))
    py.close()







