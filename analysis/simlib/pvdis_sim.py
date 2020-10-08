import os,sys
#--matplotlib
import matplotlib
matplotlib.use('Agg')
import pylab  as py
import pandas as pd
import numpy as np
from subprocess import Popen, PIPE
from scipy.integrate import quad

import lhapdf

#--from analysis
from analysis.corelib import core
from analysis.corelib import predict

#--from tools
from tools           import config
from tools.tools     import load,save,checkdir,lprint
from tools.config    import conf,load_config
from tools.inputmod  import INPUTMOD
from tools.randomstr import id_generator
from tools.config    import load_config,conf

#--from fitlib
from fitlib.resman import RESMAN
from fitlib.parman import PARMAN

#--from qcdlib
from qcdlib.aux import AUX
from qcdlib.alphaS import ALPHAS
from qcdlib.eweak import EWEAK

def pvdis(wdir,kind='e',tar='p',est='opt',obs='mean',lum='100:fb-1',force=True):

    #--generate initial data file
    gen_pvdis_xlsx(wdir,kind,tar,est,obs)

    #--modify conf with new data file
    conf = gen_conf(wdir,kind,tar,est,obs)

    #--get predictions on new data file if not already done
    print('Generating predictions...')
    name = 'pvdis-%s-%s-%s'%(kind,tar,est)
    predict.get_predictions(wdir,force=force,mod_conf=conf,name=name)

    #--update tables
    update_tabs(wdir,kind,tar,est,obs,lum)

    #--plot errors
    plot_errors(wdir,kind,tar,est,obs,lum)

    #--generate lhapdf info and data files
    if obs=='mean':
        gen_lhapdf_info_file(wdir,kind,tar,est,obs)
        gen_lhapdf_dat_file (wdir,kind,tar,est,obs)

#--generate pseudo-data
def gen_pvdis_xlsx(wdir,kind,tar,est,_obs):

    checkdir('%s/sim'%wdir)

    #-- the kinem. var.
    data={_:[] for _ in ['col','target','X','Xdo','Xup','Q2','Q2do','Q2up','obs','value','stat_u','syst_u','norm_c','RS']}

    #--get specific points from data file at fitpack/database/pvdis/expdata/1000.xlsx
    fdir = os.environ['FITPACK']
    grid = pd.read_excel(fdir + '/database/EIC/expdata/3000.xlsx')
    grid = grid.to_dict(orient='list')
    data['X']    = grid['X']
    data['Q2']   = grid['Q2']
    data['Xup']  = grid['Xup']
    data['Xdo']  = grid['Xdo']
    data['Q2up'] = grid['Q2up']
    data['Q2do'] = grid['Q2do']
    data['RS']   = grid['RS']

    obs = 'A_PV_%s'%kind

    for i in range(len(data['X'])):
        data['col']   .append('JAM4EIC')
        data['target'].append(tar)
        data['obs']   .append(obs)
        data['value'] .append(0.0)
        data['stat_u'].append(1e-10)
        data['syst_u'].append(0.0)
        data['norm_c'].append(0.0)

    df=pd.DataFrame(data)
    filename = '%s/sim/pvdis-%s-%s-%s-%s.xlsx'%(wdir,kind,tar,est,_obs)
    df.to_excel(filename, index=False)
    print('Generating xlsx file and saving to %s'%filename)

def gen_conf(wdir,kind,tar,est,obs):

    print('Modifying config with new experimental data file...')

    load_config('%s/input.py'%wdir)
    istep=core.get_istep()
    if kind == 'e':   exp = 'idis'
    if kind == 'had': exp = 'pidis'
    conf['steps'][istep]['datasets'] = {}
    conf['steps'][istep]['datasets'][exp]=[]
    conf['datasets'][exp]['filters']=[]

    #--placeholder index
    idx = 90000
    conf['datasets'][exp]['xlsx'][idx]='./%s/sim/pvdis-%s-%s-%s-%s.xlsx'%(wdir,kind,tar,est,obs)
    conf['steps'][istep]['datasets'][exp].append(idx)

    fn   = [conf['datasets'][exp]['xlsx'][idx]]
    if exp=='idis':
        conf['idis grid'] = {}
        if tar == 'p': conf['idis grid']['overwrite'] = True
        if tar == 'd': conf['idis grid']['overwrite'] = False
        conf['idis grid']['xlsx']  = fn
    elif exp=='pidis':
        conf['pidis grid']  = {}
        if tar =='p': conf['pidis grid']['overwrite'] = True
        if tar =='d': conf['pidis grid']['overwrite'] = False
        conf['pidis grid']['xlsx']  = fn
        conf['idis grid']   = {}
        if tar == 'p': conf['idis grid']['overwrite'] = True
        if tar == 'd': conf['idis grid']['overwrite'] = False
        conf['idis grid']['xlsx']   = fn

    return conf

def update_tabs(wdir,kind,tar,est,obs,lum):

    istep=core.get_istep()
    data=load('%s/data/predictions-%d-pvdis-%s-%s-%s.dat'%(wdir,istep,kind,tar,est))

    blist=[]
    blist.append('thy')
    blist.append('shift')
    blist.append('residuals')
    blist.append('prediction')
    blist.append('N')
    blist.append('Shift')
    blist.append('W2')
    blist.append('alpha')
    blist.append('residuals-rep')
    blist.append('r-residuals')
    blist.append('L')
    blist.append('H')

    #--placeholder index
    idx = 90000
    if kind == 'e':   exp = 'idis'
    if kind == 'had': exp = 'pidis'
    tab=data['reactions'][exp][idx]

    #--delete unnecessary data
    for k in blist: 
        try:    del tab[k]
        except: continue

    #--save mean value
    if obs=='mean': tab['value'] = np.mean(tab['prediction-rep'],axis=0)

    #--adjust to +-1 sigma of mean value
    if obs=='min':  tab['value'] = np.mean(tab['prediction-rep'],axis=0) - np.std(tab['prediction-rep'],axis=0)
    if obs=='max':  tab['value'] = np.mean(tab['prediction-rep'],axis=0) + np.std(tab['prediction-rep'],axis=0)

    #--save individual values
    for i in range(len(tab['prediction-rep'])):
        tab['value%s'%(i+1)] = tab['prediction-rep'][i]

    #--test distribution
    nrows,ncols=1,1
    fig = py.figure(figsize=(ncols*8,nrows*5))
    ax11=py.subplot(nrows,ncols,1)

    idx = np.array([i for i in range(len(tab['prediction-rep']))])
    points = sorted(np.array(tab['prediction-rep']).T[0])
    ax11.scatter(idx,points)
    ax11.set_ylim(-5e-7,5e-7)
    ax11.axhline(np.mean(tab['prediction-rep'],axis=0)[0],0,1)
    ax11.axhline(np.mean(tab['prediction-rep'],axis=0)[0]-np.std(tab['prediction-rep'],axis=0)[0],0,1,color='black')
    ax11.axhline(np.mean(tab['prediction-rep'],axis=0)[0]+np.std(tab['prediction-rep'],axis=0)[0],0,1,color='black')

    #py.savefig('test.png')
    py.clf()

    del tab['prediction-rep']

    if kind == 'e':   tab['stat_u'],tab['syst_u'],tab['norm_c'] = A_PV_e_errors  (wdir,kind,tar,est,obs,tab['value'],lum)
    if kind == 'had': tab['stat_u'],tab['syst_u'],tab['norm_c'] = A_PV_had_errors(wdir,kind,tar,est,obs,tab['value'],lum)

    df=pd.DataFrame(tab)
    filename = '%s/sim/pvdis-%s-%s-%s-%s.xlsx'%(wdir,kind,tar,est,obs)
    df.to_excel(filename, index=False)
    print('Updating xlsx file and saving to %s'%filename)

def A_PV_e_errors(wdir,kind,tar,est,obs,value,lum):

    conf['aux'] = AUX()
    conf['eweak'] = EWEAK()
    data = pd.read_excel('%s/sim/pvdis-%s-%s-%s-%s.xlsx'%(wdir,kind,tar,est,obs), index=False)
    data = data.to_dict(orient='list')
    l    = len(value)

    X    = np.array(data['X'])
    Q2   = np.array(data['Q2'])
    Xup  = np.array(data['Xup'])
    Xdo  = np.array(data['Xdo'])
    Q2up = np.array(data['Q2up'])
    Q2do = np.array(data['Q2do'])
    dx  = Xup  - Xdo
    dQ2 = Q2up - Q2do
    bins = dx*dQ2

    RS = np.array(data['RS'])
    S  = RS**2

    M2 = conf['aux'].M2
    #if tar=='d': M2 = 4*M2

    #--luminosity
    lum = convert_lum(lum)

    GF = conf['aux'].GF

    #--get structure functions
    resman=RESMAN(parallel=False,datasets=False)
    parman = resman.parman
    resman.setup_idis()
    idis  = resman.idis_thy
    idis.data[tar]['F2g']  = np.zeros(idis.X.size)
    idis.data[tar]['FLg']  = np.zeros(idis.X.size)
    idis.data[tar]['F2gZ'] = np.zeros(idis.X.size)
    idis.data[tar]['FLgZ'] = np.zeros(idis.X.size)
    idis.data[tar]['F3gZ'] = np.zeros(idis.X.size)
    if tar == 'd':
        idis.data['p']['F2g']  = np.zeros(idis.X.size)
        idis.data['p']['FLg']  = np.zeros(idis.X.size)
        idis.data['p']['F2gZ'] = np.zeros(idis.X.size)
        idis.data['p']['FLgZ'] = np.zeros(idis.X.size)
        idis.data['p']['F3gZ'] = np.zeros(idis.X.size)
        idis.data['n']['F2g']  = np.zeros(idis.X.size)
        idis.data['n']['FLg']  = np.zeros(idis.X.size)
        idis.data['n']['F2gZ'] = np.zeros(idis.X.size)
        idis.data['n']['FLgZ'] = np.zeros(idis.X.size)
        idis.data['n']['F3gZ'] = np.zeros(idis.X.size)

    #--get average over replicas
    istep = sorted(conf['steps'])[-1]
    jar   = load('%s/data/jar-%d.dat'%(wdir,istep))
    parman.order = jar['order']
    replicas = jar['replicas']
  
    F2g, FLg, F2gZ, FLgZ, F3gZ = 0,0,0,0,0
    for i in range(len(replicas)):
        lprint('Generating stastical errors: %s/%s'%(i+1,len(replicas)))
        par = replicas[i]
        parman.set_new_params(par,initial=True)
        idis._update()
        F2g  += idis.get_stf(X,Q2,stf='F2g',tar=tar)
        FLg  += idis.get_stf(X,Q2,stf='FLg',tar=tar)
        F2gZ += idis.get_stf(X,Q2,stf='F2gZ',tar=tar)
        FLgZ += idis.get_stf(X,Q2,stf='FLgZ',tar=tar)
        F3gZ += idis.get_stf(X,Q2,stf='F3gZ',tar=tar)
 
    print
 
    F2g  /= len(replicas) 
    FLg  /= len(replicas)
    F2gZ /= len(replicas)
    FLgZ /= len(replicas)
    F3gZ /= len(replicas)

    rho2 =  1 + 4*X**2*M2/Q2

    y= (Q2/2/X)/((S)/2)

    YP = y**2*(rho2+1)/2 - 2*y +2
    YM = 1-(1-y)**2

    sin2w = np.array([conf['eweak'].get_sin2w(q2) for q2 in Q2])
    alpha = np.array([conf['eweak'].get_alpha(q2) for q2 in Q2])

    gA = -0.5
    gV = -0.5 + 2*sin2w

    C  = GF*Q2/(2*np.sqrt(2)*np.pi*alpha)
  
    C1 = np.pi*alpha**2/(X*y*Q2)

    T1g  = YP*F2g  - y**2*FLg
    T1gZ = YP*F2gZ - y**2*FLgZ

    T2 = X*YM*F3gZ

    sigR = C1*(T1g + C*(gV-gA)*(T1gZ - T2))
    sigL = C1*(T1g + C*(gV+gA)*(T1gZ + T2))

    ##--Jacobian d/dy -> d/dQ2
    yjac = 1/(X*S)

    #--assuming same luminosity
    NR = lum*sigR*yjac*bins
    NL = lum*sigL*yjac*bins

    a = (NR-NL)/(NR+NL)

    #--% uncertainty (not divided by sigma) 
    stat2 = (1 + a**2)/(NR + NL)/(a**2)

    stat = np.sqrt(stat2)

    #--theory asymmetry
    A = np.array(value)

    #--statistical uncertainty
    data['stat_u'] = stat*A

    #--normalization uncertainty
    pol   = 0.01   #polarization
    Q2det = 0.002  #Q2 determination
    recon = 0.002  #reconstruction error
    DAQ   = 0.0015 #DAQ pile up and dead time
    data['norm_c'] = np.sqrt(pol**2 + Q2det**2 + recon**2 + DAQ**2)*A

    Y = np.array(data['Q2'])/2/np.array(data['X'])/((S-M2)/2)
    #--add systemic uncertainties
    #--optimistic: 
    if est == 'opt':
        pion = 0.01  #pion background
        rad  = 0.002 #radiative correction
        data['syst_u'] = np.sqrt(pion**2 + rad**2)*A

    #--moderate: do not have
    elif est == 'mod':
        return

    #--pessimistic: do not have
    elif est == 'pes':
        return

    else:
        print('est must be opt, mod, or pes')
        return

    return data['stat_u'],data['syst_u'],data['norm_c']

def A_PV_had_errors(wdir,kind,tar,est,obs,value,lum):

    conf['aux'] = AUX()
    conf['eweak'] = EWEAK()
    data = pd.read_excel('%s/sim/pvdis-%s-%s-%s-%s.xlsx'%(wdir,kind,tar,est,obs), index=False)
    data = data.to_dict(orient='list')
    target=data['target'][0]
    l    = len(data['value'])
    X    = np.array(data['X'])
    Q2   = np.array(data['Q2'])
    Xup  = np.array(data['Xup'])
    Xdo  = np.array(data['Xdo'])
    Q2up = np.array(data['Q2up'])
    Q2do = np.array(data['Q2do'])
    dx  = Xup  - Xdo
    dQ2 = Q2up - Q2do
    bins = dx*dQ2

    RS = np.array(data['RS'])
    S  = RS**2

    M2 = conf['aux'].M2

    #if tar=='d': M2 = 4*M2

    #--luminosity
    lum = convert_lum(lum)

    GF = conf['aux'].GF

    #--get structure functions
    resman=RESMAN(parallel=False,datasets=False)
    parman = resman.parman
    resman.setup_idis()
    resman.setup_pidis()
    pidis = resman.pidis_thy
    idis  = resman.idis_thy
    pidis.data[tar]['g1gZ'] = np.zeros(pidis.X.size)
    pidis.data[tar]['g5gZ'] = np.zeros(pidis.X.size)
    idis.data [tar]['F2g']  = np.zeros(idis.X.size)
    idis.data [tar]['FLg']  = np.zeros(idis.X.size)
    idis.data [tar]['F2gZ'] = np.zeros(idis.X.size)
    idis.data [tar]['FLgZ'] = np.zeros(idis.X.size)
    idis.data [tar]['F3gZ'] = np.zeros(idis.X.size)
    idis   = resman.idis_thy
    pidis  = resman.pidis_thy

    #--get average over replicas
    istep = sorted(conf['steps'])[-1]
    jar   = load('%s/data/jar-%d.dat'%(wdir,istep))
    parman.order = jar['order']
    replicas = jar['replicas']
  
    g1gZ, g5gZ, F2g, FLg, F2gZ, FLgZ, F3gZ = 0,0,0,0,0,0,0
    for i in range(len(replicas)):
        lprint('Generating stastical errors: %s/%s'%(i+1,len(replicas)))
        par = replicas[i]
        parman.set_new_params(par,initial=True)
        idis._update()
        pidis._update()
        g1gZ += pidis.get_stf(X,Q2,stf='g1gZ',tar=tar) 
        g5gZ += pidis.get_stf(X,Q2,stf='g5gZ',tar=tar) 
        F2g  += idis .get_stf(X,Q2,stf='F2g'  ,tar=tar) 
        FLg  += idis .get_stf(X,Q2,stf='FLg'  ,tar=tar) 
        F2gZ += idis .get_stf(X,Q2,stf='F2gZ' ,tar=tar) 
        FLgZ += idis .get_stf(X,Q2,stf='FLgZ' ,tar=tar) 
        F3gZ += idis .get_stf(X,Q2,stf='F3gZ' ,tar=tar) 
 
    print
 
    g1gZ /= len(replicas) 
    g5gZ /= len(replicas) 
    F2g  /= len(replicas) 
    FLg  /= len(replicas) 
    F2gZ /= len(replicas) 
    FLgZ /= len(replicas) 
    F3gZ /= len(replicas) 
 
    rho2 = 1 + 4*X**2*M2/Q2

    y = (Q2/2/X)/((S)/2)

    YP = y**2 - 2*y +2
    YM = 1-(1-y)**2

    sin2w = np.array([conf['eweak'].get_sin2w(q2) for q2 in Q2])
    alpha = np.array([conf['eweak'].get_alpha(q2) for q2 in Q2])

    gA = -0.5
    gV = -0.5 + 2*sin2w

    C  = GF*Q2/(2*np.sqrt(2)*np.pi*alpha)
  
    C1 = np.pi*alpha**2/(X*y*Q2)

    T1g  = YP*F2g  - y**2*FLg
    T1gZ = YP*F2gZ - y**2*FLgZ

    T2 = X*YM*F3gZ

    T3 = YP*gV*g5gZ + YM*gA*g1gZ

    sigR = C1*(T1g + C*(gV*T1gZ + gA*T2) + 2*X*C*T3)
    sigL = C1*(T1g + C*(gV*T1gZ + gA*T2) - 2*X*C*T3)

    ##--Jacobian d/dy -> d/dQ2
    yjac = 1/(X*S)

    NR = lum*sigR*yjac*bins
    NL = lum*sigL*yjac*bins

    a = (NR-NL)/(NR+NL)

    #--% uncertainty
    stat2 = np.abs((1 + a**2)/(NR + NL)/(a**2))

    stat = np.sqrt(stat2)

    #--theory asymmetry
    A = np.array(value)

    #--statistical uncertainties
    data['stat_u'] = stat*A

    #--normalization uncertainty
    pol   = 0.02   #polarization
    Q2det = 0.002  #Q2 determination
    recon = 0.002  #reconstruction error
    DAQ   = 0.0015 #DAQ pile up and dead time
    data['norm_c'] = np.sqrt(pol**2 + Q2det**2 + recon**2 + DAQ**2)*A

    Y = np.array(data['Q2'])/2/np.array(data['X'])/((S-M2)/2)
    #--add systemic uncertainties
    #--optimistic: 
    if est == 'opt':
        pion = 0.01  #pion background
        rad  = 0.002 #radiative correction
        data['syst_u'] = np.sqrt(pion**2 + rad**2)*A

    #--moderate: do not have
    elif est == 'mod':
        return

    #--pessimistic: do not have
    elif est == 'pes':
        return

    return data['stat_u'],data['syst_u'],data['norm_c']

def convert_lum(lum):
    one=0.3893793721  #--GeV2 mbarn from PDG
    lum,units=lum.split(':')
    lum=float(lum)
    units=units.strip()
    if units=='fb-1':   return lum*one*1e12
    else:               sys.exit('units not convertible!')

def plot_errors(wdir,kind,tar,est,obs,lum):

    nrows,ncols=1,1
    fig = py.figure(figsize=(ncols*9,nrows*5))
    ax11=py.subplot(nrows,ncols,1)

    tab   = pd.read_excel('%s/sim/pvdis-%s-%s-%s-%s.xlsx'%(wdir,kind,tar,est,obs))
    tab   = tab.to_dict(orient='list')
    X     = np.array(tab['X'])
    value = np.array(tab['value'])
    stat  = np.abs(np.array(tab['stat_u'])/value)
    syst  = np.abs(np.array(tab['syst_u'])/value)

    #--check for zero systematic uncertainty
    zero = True
    for i in range(len(syst)):
        if syst[i] != 0: zero = False

    alpha = np.sqrt((stat**2 + syst**2))

    hand = {}
    hand['alpha'] = ax11.scatter(X,alpha,color='red'    ,s=20,marker='s')
    hand['stat']  = ax11.scatter(X,stat ,color='green'  ,s=10,marker='o')
    hand['syst']  = ax11.scatter(X,syst ,color='magenta',s=10,marker='v')

    ax11.set_xlim(2e-5,1)
    ax11.semilogx()
    ax11.semilogy()

    if kind == 'e':
        #ax11.set_ylim(1e-4,1e-1)
        ax11.set_ylabel(r'\boldmath$|\sigma_{A_{PV}^e}/A_{PV}^e|$',size=30)
        #if est == 'opt': ax11.text(0.6,0.4,r'\textrm{Optimistic}' ,transform = ax11.transAxes,size=30)
        #if est == 'mod': ax11.text(0.6,0.4,r'\textrm{Moderate}'   ,transform = ax11.transAxes,size=30)
        #if est == 'pes': ax11.text(0.6,0.4,r'\textrm{Pessimistic}',transform = ax11.transAxes,size=30)
    if kind == 'had':
        #ax11.set_ylim(1e-3,1e3)
        ax11.set_yticks([1e-3,1e-2,1e-1,1e0,1e1,1e2,1e3])
        locmin = matplotlib.ticker.LogLocator(base=10.0,subs=(0.2,0.4,0.6,0.8),numticks=7)
        ax11.yaxis.set_minor_locator(locmin)
        ax11.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
        ax11.set_ylabel(r'\boldmath$|\sigma_{A_{PV}^{p}}/A_{PV}^{p}|$',size=30)
        #if est == 'opt': ax11.text(0.6,0.6,r'\textrm{Optimistic}' ,transform = ax11.transAxes,size=30)
        #if est == 'mod': ax11.text(0.6,0.6,r'\textrm{Moderate}'   ,transform = ax11.transAxes,size=30)
        #if est == 'pes': ax11.text(0.6,0.6,r'\textrm{Pessimistic}',transform = ax11.transAxes,size=30)


    ax11.set_xlabel(r'\boldmath$x$',size=30)

    ax11.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=30)


    if tar == 'p':   ax11.text(0.05,0.85,r'\textrm{Proton}'     ,transform = ax11.transAxes,size=30)
    if tar == 'd':   ax11.text(0.05,0.85,r'\textrm{Deuteron}'   ,transform = ax11.transAxes,size=30)

    handles = [hand['alpha'],hand['stat'],hand['syst']]
    label1 = r'\textbf{\textrm{Total}}'
    label2 = r'\textbf{\textrm{Stat}}'
    label3 = r'\textbf{\textrm{Syst}}'
    labels = [label1,label2,label3]

    ax11.legend(handles,labels,loc='lower left', fontsize = 20, frameon = 0, handletextpad = 0.3, handlelength = 1.0)
    py.tight_layout()
    checkdir('%s/gallery'%wdir)
    filename = '%s/gallery/pvdis-errors-%s-%s-%s-%s'%(wdir,kind,tar,est,obs)
    py.savefig(filename)
    print('Saving error plot to %s'%filename)
    py.clf()

#--generate lhapdf info and data files
def gen_lhapdf_info_file(wdir,kind,tar,est,obs):

    info={}
    if kind == 'e':   info['<description>'] = 'PVDIS (electron)'
    if kind == 'had': info['<description>'] = 'PVDIS (hadron)'
    info['<index>']       = '0'
    info['<authors>']     = 'JAM Collaboration'
    info['<reference>']   = ''
    info['<particle>']    = '%s'%tar

    #--get tables
    X,Q2,table,replicas=get_tables(wdir,kind,tar,est,obs)

    #--kinematic limits
    xmin=X[0]
    xmax=X[-1]
    Qmin=Q2[0]**0.5
    Qmax=Q2[-1]**0.5

    #--qcd params
    load_config('%s/input.py'%wdir)
    RESMAN(nworkers=1,parallel=False,datasets=False)
    aS=[conf['alphaS'].get_alphaS(_) for _ in Q2]
    mZ=conf['aux'].mZ
    mb=conf['aux'].mb
    mc=conf['aux'].mc
    alphaSMZ=conf['aux'].alphaSMZ

    #--begin lhapdf info file
    lines=[]
    lines.append('SetDesc:         "<description>"')
    lines.append('SetIndex:        <index>')
    lines.append('Authors:         <authors>')
    lines.append('Reference:       <reference>')
    lines.append('Format:          lhagrid1')
    lines.append('DataVersion:     1')
    lines.append('NumMembers:      1')
    lines.append('Particle:        <particle>')
    lines.append('Flavors:         [90000]')
    lines.append('OrderQCD:        1')
    lines.append('FlavorScheme:    <flav scheme>')
    lines.append('NumFlavors:      1')
    lines.append('ErrorType:       no error')
    lines.append('XMin:            %0.2e'%xmin)
    lines.append('XMax:            %0.2e'%xmax)
    lines.append('QMin:            %0.2e'%Qmin)
    lines.append('QMax:            %0.2e'%Qmax)
    lines.append('MZ:              %f'%mZ)
    lines.append('MUp:             0.0')
    lines.append('MDown:           0.0')
    lines.append('MStrange:        0.0')
    lines.append('MCharm:          %f'%mc)
    lines.append('MBottom:         %f'%mb)
    lines.append('MTop:            180.0')
    lines.append('AlphaS_MZ:       %f'%alphaSMZ)
    lines.append('AlphaS_OrderQCD: 1')
    lines.append('AlphaS_Type:     ipol')
    line='AlphaS_Qs: ['
    for _ in Q2: line+=('%10.5e, '%_**0.5).upper()
    line=line.rstrip(',')+']'
    lines.append(line)
    line='AlphaS_Vals: ['
    for _ in aS: line+=('%10.5e, '%_).upper()
    line=line.rstrip(',')+']'
    lines.append(line)
    lines.append('AlphaS_Lambda4: 0')
    lines.append('AlphaS_Lambda5: 0')

    for i in range(len(lines)):
        for _ in info:
            lines[i]=lines[i].replace(_,info[_])


    lines=[l+'\n' for l in lines]
    dirname = 'pvdis-%s-%s'%(kind,tar)
    checkdir('%s/lhapdf/%s'%(wdir,dirname))
    tab=open('%s/lhapdf/%s/%s.info'%(wdir,dirname,dirname),'w')
    tab.writelines(lines)
    tab.close()
    print('Saving lhapdf info file to %s/lhapdf/%s/%s.info'%(wdir,dirname,dirname))

def gen_lhapdf_dat_file(wdir,kind,tar,est,obs):

    #--get tables
    X,Q2,central,replicas=get_tables(wdir,kind,tar,est,obs)
    nx=len(X)
    nQ2=len(Q2)
    nrep = len(replicas)
    L = nx


    #--central value
    #--start lhapdf file
    lines=[]
    lines.append('PdfType: central')
    lines.append('Format: lhagrid1')
    lines.append('---')
    line=''
    for _ in X: line+=('%10.5e '%_).upper()
    lines.append(line)
    line=''
    for _ in Q2: line+=('%10.5e '%_**0.5).upper()
    lines.append(line)
    flavs=''
    flavs+='90000 '
    lines.append(flavs)

    for i in range(L):
        line=''
        line+=('%10.5e '%central[i]).upper()
        lines.append(line)
    lines.append('---')
    lines=[l+'\n' for l in lines]
    if central: idx=str(0).zfill(4)
    else:       idx=str(0).zfill(4)

    dirname = 'pvdis-%s-%s'%(kind,tar)
    checkdir('%s/lhapdf/%s'%(wdir,dirname))
    tab=open('%s/lhapdf/%s/%s_%s.dat'%(wdir,dirname,dirname,idx),'w')
    tab.writelines(lines)
    tab.close()

    #--individual replicas
    for j in range(nrep): 
        #--start lhapdf file
        lines=[]
        lines.append('PdfType: replica')
        lines.append('Format: lhagrid1')
        lines.append('---')
        line=''
        for _ in X: line+=('%10.5e '%_).upper()
        lines.append(line)
        line=''
        for _ in Q2: line+=('%10.5e '%_**0.5).upper()
        lines.append(line)
        flavs=''
        flavs+='90000 '
        lines.append(flavs)

        for i in range(L):
            line=''
            line+=('%10.5e '%replicas[j][i]).upper()
            lines.append(line)
        lines.append('---')
        lines=[l+'\n' for l in lines]
        l = len(str(j+1))
        idx=str(0).zfill(4-l)+str((j+1))

        tab=open('%s/lhapdf/%s/%s_%s.dat'%(wdir,dirname,dirname,idx),'w')
        tab.writelines(lines)
        tab.close()

    print('Saving lhapdf data files inside %s/lhapdf/%s'%(wdir,dirname))

def get_tables(wdir,kind,tar,est,obs):
    replicas = []
    tab=pd.read_excel('%s/sim/pvdis-%s-%s-%s-%s.xlsx'%(wdir,kind,tar,est,obs))
    tab=tab.to_dict(orient='list')
    central = tab['value']
    _replicas = {}
    for key in tab:
        if key[:5] != 'value': continue
        if key     == 'value': continue
        _replicas[key] = tab[key]
    for i in range(len(_replicas)):
        replicas.append(_replicas['value%s'%(i+1)])

    X    = tab['X']
    Q2   = tab['Q2']

    return X,Q2,central,replicas







 
