#!/usr/bin/env python
import os,sys
import subprocess
import numpy as np
import scipy as sp
import pandas as pd
import copy

#--from tools
from tools           import config
from tools.tools     import load,save,checkdir,lprint
from tools.config    import conf,load_config
from tools.inputmod  import INPUTMOD
from tools.randomstr import id_generator

#--from fitlib
from fitlib.resman import RESMAN

#--from local
import core

def get_predictions(wdir,force=False,ncores=3,mod_conf=None,name=''):

    #--if force=False: previous predictions will not be repeated
    #--if force=True : previous predictions will be overwritten
    
    if mod_conf == None:
        load_config('%s/input.py'%wdir)
        replicas=core.get_replicas(wdir)
    else:
        config.conf = copy.deepcopy(mod_conf)
        replicas=core.get_replicas(wdir,mod_conf=conf)

    names= core.get_replicas_names(wdir)

    conf['bootstrap']=False
    istep=core.get_istep()
    core.mod_conf(istep,replicas[0]) #--set conf as specified in istep

    #--choose parallelization based on what experiments are present
    nopar = ['idis','pidis','sidis','sia']
    _ncores = 1
    parallel = False
    for exp in conf['steps'][istep]['datasets']:
        if exp not in nopar:
            parallel = True
            _ncores = ncores

    #--run RESMAN
    resman=RESMAN(nworkers=_ncores,parallel=parallel,datasets=True)
    parman=resman.parman
    order=parman.order

    #--get replicas that are already done if force=False
    if force==False:
        try:
            if mod_conf == None: done = load('%s/data/predictions-%d.dat'%(wdir,istep))
            else:                done = load('%s/data/predictions-%d-%s.dat'%(wdir,istep,name))
            done['res'].tolist()
            done['rres'].tolist()
            done['nres'].tolist()
            flag=True
        except: flag=False
    else: flag=False
       
    obsres={}
    if 'idis'     in conf['datasets'] : obsres['idis']     = resman.idis_res
    if 'pidis'    in conf['datasets'] : obsres['pidis']    = resman.pidis_res
    if 'sidis'    in conf['datasets'] : obsres['sidis']    = resman.sidis_res
    if 'psidis'   in conf['datasets'] : obsres['psidis']   = resman.psidis_res
    if 'dy'       in conf['datasets'] : obsres['dy']       = resman.dy_res
    if 'wzrv'     in conf['datasets'] : obsres['wzrv']     = resman.wzrv_res
    if 'wasym'    in conf['datasets'] : obsres['wasym']    = resman.wasym_res
    if 'zrap'     in conf['datasets'] : obsres['zrap']     = resman.zrap_res
    if 'sia'      in conf['datasets'] : obsres['sia']      = resman.sia_res
    if 'qpdf'     in conf['datasets'] : obsres['qpdf']     = resman.qpdf_res
    if 'dy-pion'  in conf['datasets'] : obsres['dy-pion']  = resman.dy_pion_res
    if 'pion_qT'  in conf['datasets'] : obsres['pion_qT']  = resman.pion_qTres
    if 'ln'       in conf['datasets'] : obsres['ln']       = resman.ln_res
    if 'jet'      in conf['datasets'] : obsres['jet']      = resman.jet_res
    if 'pjet'     in conf['datasets'] : obsres['pjet']     = resman.pjet_res
   
    #--setup big table to store all we want
    data={}
    data['name'] = [] 
    data['order']=order
    data['params']=[]
    data['reactions']={}
    data['res']=[]
    data['rres']=[]
    data['nres']=[]

    for _ in obsres:
        tabs=copy.copy(obsres[_].tabs)
        #--create a space to store all the predictions from replicas
        for idx in tabs:
            tabs[idx]['prediction-rep']=[]
            tabs[idx]['residuals-rep']=[]
        data['reactions'][_]=tabs
      

    print('\ngen predictions using %s\n'%wdir)

    #--total replica count
    cnt =0
    #--already completed replica count
    dcnt=0
    for replica in replicas:
        lprint('progress: %d/%d'%(cnt+1,len(replicas)))
        #--skip replicas that have already been generated
        if flag:
            if names[cnt] in done['name']:
                data['name']  .append(done['name'][dcnt])
                data['res']   .append(done['res'][dcnt])
                data['rres']  .append(done['rres'][dcnt])
                data['nres']  .append(done['nres'][dcnt])
                data['params']=np.append(data['params'],done['params'][dcnt])
                for _ in obsres:
                    for idx in data['reactions'][_]:
                        data['reactions'][_][idx]['prediction-rep'].append(done['reactions'][_][idx]['prediction-rep'][dcnt])
                        data['reactions'][_][idx]['residuals-rep'].append(done['reactions'][_][idx]['residuals-rep'][dcnt])
                dcnt+=1
                cnt+=1
                continue

        data['name'].append(names[cnt])
        cnt+=1
        parman.par=copy.copy(replica['params'][istep])
        parman.order=copy.copy(replica['order'][istep])
        data['params']=np.append(data['params'],parman.par)

        #--compute residuals (==theory)
        res,rres,nres=resman.get_residuals(parman.par)
        data['res'].append(res)
        data['rres'].append(rres)
        data['nres'].append(nres)

        #--save predictions of the current step and current replica at data
        for _ in obsres:
            for idx in data['reactions'][_]:
                prediction=copy.copy(obsres[_].tabs[idx]['prediction'])
                residuals=copy.copy(obsres[_].tabs[idx]['residuals'])
                data['reactions'][_][idx]['prediction-rep'].append(prediction)
                data['reactions'][_][idx]['residuals-rep'].append(residuals)
    print 

    #--close resman
    resman.shutdown()

    #--convert tables to numpy array before saving
    for _ in ['res','rres','nres']:
        data[_]=np.array(data[_])

    checkdir('%s/data'%wdir)
    if mod_conf==None:
        save(data,'%s/data/predictions-%d.dat'%(wdir,istep))
    else:
        save(data,'%s/data/predictions-%d-%s.dat'%(wdir,istep,name))

def get_summary(self,wdir,istep):

    #--needs revision NS (09/02/19)

    data=load('%s/data/predictions-%d.dat'%(wdir,istep))

    summary=[]
    dic={} 
    global_chi2=0
    global_npts=0
    for reaction in data['reactions']:
        dic[reaction]={}
        for idx in data['reactions'][reaction]:
            dic[reaction][idx]={}
            tab=data['reactions'][reaction][idx]
            value=tab['value']
            alpha=tab['alpha']
            CHI2=[]
            for i in range(len(tab['predictions'])):
                chi2tot=np.sum(data['res'][i]**2)/data['res'][i].size
                #if chi2tot>2: continue
                prediction=tab['predictions'][i]
                CHI2.append(np.sum(((value-prediction)/alpha)**2))
            npts=len(value)
            col=tab['col'][0]
            chi2min=np.amin(CHI2)/npts
            chi2max=np.amax(CHI2)/npts
            chi2ave=np.mean(CHI2)/npts

            global_chi2+=np.amin(CHI2)
            global_npts+=npts

            msg ='reaction: %8s' 
            msg+=' idx: %7d'
            msg+=' col: %10s'
            msg+=' chi2/npts (min,ave,max): %6.2f %6.2f %6.2f'
            msg+=' npts: %5d'
            msg=msg%(reaction,idx,col[:10],chi2min,chi2ave,chi2max,npts)
            dic[reaction][idx]['col']=col
            dic[reaction][idx]['chi2']=np.amin(CHI2)
            dic[reaction][idx]['chi2/npts']=np.amin(CHI2)/npts
            dic[reaction][idx]['npts']=npts
            if  reaction=='dy':
                msg+=' rea: %s'%tab['reaction'][0]
            if  reaction=='sia':
                msg+=' had: %s'%tab['hadron'][0]
            if  reaction=='idis':
                msg+=' tar: %s'%tab['target'][0]
                msg+=' obs: %s'%tab['obs'][0]
            if  reaction=='sidis':
                msg+=' tar: %1s'%tab['target'][0][0]
                msg+=' had: %5s'%tab['hadron'][0]
                msg+=' obs: %s'%tab['obs'][0]
            if  reaction=='pidis':
                msg+=' tar: %s'%tab['target'][0]
                msg+=' obs: %s'%tab['obs'][0]
            if  reaction=='psidis':
                msg+=' tar: %1s'%tab['target'][0][0]
                msg+=' had: %5s'%tab['hadron'][0]
                msg+=' obs: %s'%tab['obs'][0]
            #print msg
            summary.append(msg)
        #print tab.keys()

    print 'global summary'
    print 'chi2/npts =',global_chi2/global_npts
    print 'npts      =',global_npts

    summary=[_+'\n' for _ in summary]
    F=open('%s/data/summary-%d.txt'%(wdir,istep),'w')
    F.writelines(summary)
    F.close()
    save(dic,'%s/data/summary-%d.dat'%(wdir,istep))

def gen_exp_dict(self,wdir,istep):

    #--needs revision NS (09/02/19)

    data=load('%s/data/predictions-%d.dat'%(wdir,istep))
    summary=[]
    for reaction in data['reactions']:
        for idx in data['reactions'][reaction]:
            tab=data['reactions'][reaction][idx]
            col=tab['col'][0]
            value=tab['value']
            npts=len(value)

            msg ='reaction: %8s,' 
            msg+=' idx: %7d,'
            msg+=' col: %10s,'
            msg+=' npts: %5d,'
            msg=msg%(reaction,idx,col[:10],npts)
            if  reaction=='dy':
                msg+=' rea: %s,'%tab['reaction'][0]
            if  reaction=='sia':
                msg+=' had: %s,'%tab['hadron'][0]
            if  reaction=='idis':
                msg+=' tar: %s,'%tab['target'][0]
                msg+=' obs: %s,'%tab['obs'][0]
            if  reaction=='sidis':
                msg+=' tar: %1s,'%tab['target'][0][0]
                msg+=' had: %5s,'%tab['hadron'][0]
                msg+=' obs: %s,'%tab['obs'][0]
            if  reaction=='pidis':
                msg+=' tar: %s,'%tab['target'][0]
                msg+=' obs: %s,'%tab['obs'][0]
            if  reaction=='psidis':
                msg+=' tar: %1s,'%tab['target'][0][0]
                msg+=' had: %5s,'%tab['hadron'][0]
                msg+=' obs: %s,'%tab['obs'][0]
            summary.append(msg)

    summary=[_+'\n' for _ in summary]
    F=open('%s/data/exp-dict-%d.txt'%(wdir,istep),'w')
    F.writelines(summary)
    F.close()






