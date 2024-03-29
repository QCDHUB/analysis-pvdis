import sys,os
import numpy as np
import copy
from subprocess import Popen, PIPE, STDOUT
import pandas as pd

#--matplotlib
import matplotlib
matplotlib.use('Agg')
#matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
#matplotlib.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#matplotlib.rc('text',usetex=True)
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.lines import Line2D
import pylab as py


#--from tools
from tools.tools     import load,save,checkdir,lprint
from tools.config    import conf,load_config

#--from fitlib
from fitlib.resman import RESMAN

#--from local
from analysis.corelib import core
from analysis.corelib import classifier

def get_norm(wdir,kc): 
    istep=core.get_istep()
    replicas=core.get_replicas(wdir)
    core.mod_conf(istep,replicas[0]) #--set conf as specified in istep   
    tab={}
    for replica in replicas: 
        order=replica['order'][istep]
        params=replica['params'][istep]
        for i in range(len(order)):
            if order[i][0]==2:
                reaction=order[i][1]
                idx=order[i][2]
                if reaction not in tab: tab[reaction]={}
                if idx not in tab[reaction]: tab[reaction][idx]=[] 
                tab[reaction][idx].append(params[i])
                        
    for reaction in tab:
        for idx in tab[reaction]:
            norm=tab[reaction][idx][:]
            tab[reaction][idx]={}
            tab[reaction][idx]['mean']=np.mean(norm)
            tab[reaction][idx]['std']=np.std(norm)
    return tab

def get_chi2(wdir,kc): 

    istep=core.get_istep()
    #replicas=core.get_replicas(wdir)
    #core.mod_conf(istep,replicas[0]) #--set conf as specified in istep   

    predictions=load('%s/data/predictions-%d.dat'%(wdir,istep))
    data=predictions['reactions']
    tab={}
    for reaction in data:
        for idx in data[reaction]:
            if reaction not in tab: tab[reaction]={}
            if idx not in tab[reaction]: tab[reaction][idx]={}
      
            value=data[reaction][idx]['value']
            alpha=data[reaction][idx]['alpha']
            thy=np.mean(data[reaction][idx]['prediction-rep'],axis=0)
            col=data[reaction][idx]['col'][0]
            if 'target' in            data[reaction][idx]: tar=data[reaction][idx]['target'][0]
            elif 'tar' in             data[reaction][idx]: tar=data[reaction][idx]['tar'][0]
            elif 'particles-in' in    data[reaction][idx]: tar=data[reaction][idx]['particles-in'][0]
            obs=data[reaction][idx]['obs'][0]
            res=(value-thy)/alpha
            chi2=np.sum(res**2)
            npts=res.size
            chi2_npts=chi2/npts

            tab[reaction][idx]['col']=col
            tab[reaction][idx]['tar']=tar
            tab[reaction][idx]['obs']=obs
            tab[reaction][idx]['chi2']=chi2
            tab[reaction][idx]['npts']=npts
            tab[reaction][idx]['chi2_npts']=chi2_npts
    return tab

def print_summary(wdir,kc): 
    print('\nsummary of  %s\n'%(wdir))
    load_config('%s/input.py'%wdir)
    norm_tab=get_norm(wdir,kc)
    chi2_tab=get_chi2(wdir,kc)

    msg1 ='%10s '
    msg1+='%10s '
    msg1+='%10s '
    msg1+='%25s '
    msg1+='%5s '
    msg1+='%20s '
    msg1+='%5s '
    msg1+='%10s '
    msg1+='%10s '
    msg1+='%10s '
    msg1=msg1%('prediction','reaction','idx','col','tar','obs','npts','chi2','chi2/npts','norm')
    print(msg1)
    chi2_tot=0
    npts_tot=0
    for reaction in chi2_tab:
        for idx in chi2_tab[reaction]:
            col=chi2_tab[reaction][idx]['col']
            tar=chi2_tab[reaction][idx]['tar']
            obs=chi2_tab[reaction][idx]['obs']
            npts=chi2_tab[reaction][idx]['npts']
            chi2=chi2_tab[reaction][idx]['chi2']
            chi2_npts=chi2_tab[reaction][idx]['chi2_npts']
            if reaction in norm_tab:
                if idx in norm_tab[reaction]:
                    norm=norm_tab[reaction][idx]['mean']
                elif idx in conf['datasets'][reaction]['norm']:
                    norm=conf['datasets'][reaction]['norm'][idx]['value']
                else:
                    norm='N/A'
            else: norm = 'N/A'

            prediction=False

            if 'prediction' in conf:
                if reaction in conf['prediction']:
                    if any([idx==_ for _ in conf['prediction'][reaction]]): 
                        prediction=True

            if prediction==False:
                chi2_tot+=chi2
                npts_tot+=npts

            msg2 ='%10s '
            msg2+='%10s '
            msg2+='%10d '
            msg2+='%25s '
            msg2+='%5s '
            msg2+='%20s '
            msg2+='%5d '
            msg2+='%10.2f '
            msg2+='%10.2f '
            if type(norm).__name__=='float64': msg2+='%10.2f '
            if type(norm).__name__=='float': msg2+='%10.2f '
            if type(norm).__name__=='str':   msg2+='%10s '
            print(msg2%(prediction,reaction,idx,col,tar,obs,npts,chi2,chi2_npts,norm))

    chi2_npts_tot=chi2_tot/npts_tot

    print("-"*len(msg1))
    msg3 ='%10s '
    msg3+='%10s '
    msg3+='%10s '
    msg3+='%25s '
    msg3+='%5s '
    msg3+='%20s '
    msg3+='%5d '
    msg3+='%10.2f '
    msg3+='%10.3f '
    msg3+='%10s'
    print(msg3%(' ',' ',' ',' ',' ',' ',npts_tot,chi2_tot,chi2_npts_tot,' '))

 



