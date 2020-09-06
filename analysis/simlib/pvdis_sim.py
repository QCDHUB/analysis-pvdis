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

def pvdis(wdir,kind='e',tar='p',est='opt',lum='100:fb-1',force=True):

    #--generate initial data file
    gen_pvdis_xlsx(wdir,kind,tar,est)

    #--modify conf with new data file
    conf = gen_conf(wdir,kind,tar,est)

    #--get predictions on new data file if not already done
    print('Generating predictions...')
    name = 'pvdis-%s-%s-%s'%(kind,tar,est)
    predict.get_predictions(wdir,force=force,mod_conf=conf,name=name)

    #--update tables
    update_tabs(wdir,kind,tar,est,lum)

    #--plot errors
    plot_errors(wdir,kind,tar,est,lum)

    #--generate lhapdf info and data files
    gen_lhapdf_info_file(wdir,kind,tar,est)
    gen_lhapdf_dat_file (wdir,kind,tar,est)

#--generate pseudo-data
def gen_pvdis_xlsx(wdir,kind,tar,est):

    checkdir('%s/sim'%wdir)

    #-- the kinem. var.
    data={_:[] for _ in ['col','target','X','Xdo','Xup','Q2','Q2do','Q2up','obs','value','stat_u','syst_u','pol','pol_u','RS']}

    #--get specific points from data file at fitpack/database/pvdis/expdata/1000.xlsx
    fdir = os.environ['FITPACK']
    grid = pd.read_excel(fdir + '/database/pvdis/expdata/1000.xlsx')
    grid = grid.to_dict(orient='list')
    data['X']    = grid['X']
    data['Q2']   = grid['Q2']
    data['Xup']  = grid['Xup']
    data['Xdo']  = grid['Xdo']
    data['Q2up'] = grid['Q2up']
    data['Q2do'] = grid['Q2do']
    data['RS']   = grid['RS']

    obs = 'A_PV_%s'%kind

    if kind == 'e':   pol = 0.7
    if kind == 'had': pol = 0.7

    for i in range(len(data['X'])):
        data['col']   .append('JAM4EIC')
        data['target'].append(tar)
        data['obs']   .append(obs)
        data['value'] .append(0.0)
        data['stat_u'].append(1e-10)
        data['syst_u'].append(0.0)
        data['pol']   .append(pol)
        data['pol_u'] .append(0.0)

    df=pd.DataFrame(data)
    filename = '%s/sim/pvdis-%s-%s-%s.xlsx'%(wdir,kind,tar,est)
    df.to_excel(filename, index=False)
    print('Generating xlsx file and saving to %s'%filename)

def gen_conf(wdir,kind,tar,est):

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
    conf['datasets'][exp]['xlsx'][idx]='./%s/sim/pvdis-%s-%s-%s.xlsx'%(wdir,kind,tar,est)
    conf['steps'][istep]['datasets'][exp].append(idx)

    fdir = os.environ['FITPACK']
    fn   = [fdir + '/database/pvdis/expdata/1000.xlsx']
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

def update_tabs(wdir,kind,tar,est,lum):

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
    tab['value']=np.mean(tab['prediction-rep'],axis=0)

    #--save individual values
    for i in range(len(tab['prediction-rep'])):
        tab['value%s'%(i+1)] = tab['prediction-rep'][i]

    del tab['prediction-rep']

    if kind == 'e':   tab['stat_u'],tab['pol_u'],tab['syst_u'] = A_PV_e_errors  (wdir,kind,tar,est,tab['value'],lum)
    if kind == 'had': tab['stat_u'],tab['pol_u'],tab['syst_u'] = A_PV_had_errors(wdir,kind,tar,est,tab['value'],lum)

    df=pd.DataFrame(tab)
    filename = '%s/sim/pvdis-%s-%s-%s.xlsx'%(wdir,kind,tar,est)
    df.to_excel(filename, index=False)
    print('Updating xlsx file and saving to %s'%filename)

def A_PV_e_errors(wdir,kind,tar,est,value,lum):

    conf['aux'] = AUX()
    conf['eweak'] = EWEAK()
    data = pd.read_excel('%s/sim/pvdis-%s-%s-%s.xlsx'%(wdir,kind,tar,est), index=False)
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

    pol = data['pol'][0]

    RS = data['RS'][0]
    S  = RS**2

    M2 = conf['aux'].M2
    if tar=='d': M2 = 4*M2

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

    idis._update()

    F2g  = lambda x,q2: idis.get_stf(x,q2,stf='F2g' ,tar=tar) 
    FLg  = lambda x,q2: idis.get_stf(x,q2,stf='FLg' ,tar=tar) 
    F2gZ = lambda x,q2: idis.get_stf(x,q2,stf='F2gZ',tar=tar) 
    FLgZ = lambda x,q2: idis.get_stf(x,q2,stf='FLgZ',tar=tar) 
    F3gZ = lambda x,q2: idis.get_stf(x,q2,stf='F3gZ',tar=tar) 

    rho2 = lambda x,q2: 1 + 4*x**2*M2/q2

    y=lambda x,q2: (q2/2/x)/((S-M2)/2)

    YP = lambda x,q2: y(x,q2)**2*(rho2(x,q2)+1)/2 - 2*y(x,q2) +2
    YM = lambda x,q2: 1-(1-y(x,q2))**2

    sin2w = lambda q2: conf['eweak'].get_sin2w(q2)
    alpha = lambda q2: conf['eweak'].get_alpha(q2)

    gA = -0.5
    gV = lambda q2: -0.5 + 2*sin2w(q2)

    C  = lambda q2: GF*q2/(2*np.sqrt(2)*np.pi*alpha(q2))
  
    C1 = lambda x,q2: np.pi*alpha(q2)**2/(x*y(x,q2)*q2)

    T1g  = lambda x,q2: YP(x,q2)*F2g(x,q2)  - y(x,q2)**2*FLg(x,q2)
    T1gZ = lambda x,q2: YP(x,q2)*F2gZ(x,q2) - y(x,q2)**2*FLgZ(x,q2)

    T2 = lambda x,q2: x*YM(x,q2)*F3gZ(x,q2)

    _ddsigR = lambda x,q2: C1(x,q2)*(T1g(x,q2) + C(q2)*(gV(q2)-gA)*(T1gZ(x,q2) - T2(x,q2)))
    _ddsigL = lambda x,q2: C1(x,q2)*(T1g(x,q2) + C(q2)*(gV(q2)+gA)*(T1gZ(x,q2) + T2(x,q2)))

    #--integrate over bin
    z1,w1 = np.polynomial.legendre.leggauss(3)
    z2,w2 = np.polynomial.legendre.leggauss(3)

    ddsigR = np.zeros((len(X),len(z1),len(z2)))
    ddsigL = np.zeros((len(X),len(z1),len(z2)))
    for i in range(len(X)):
        _x   = 0.5*((Xup[i] -Xdo[i])*z1  + Xup[i]  + Xdo[i])
        _q2  = 0.5*((Q2up[i]-Q2do[i])*z2 + Q2up[i] + Q2do[i])
        xjac  = 0.5*(Xup[i] -Xdo[i])
        q2jac = 0.5*(Q2up[i]-Q2do[i])
        for j in range(len(_x)):
            for k in range(len(_q2)):
                ddsigR[i][j][k] = _ddsigR(_x[j],_q2[k])*xjac*q2jac
                ddsigL[i][j][k] = _ddsigL(_x[j],_q2[k])*xjac*q2jac
   
    #--integrate over Q2
    dsigR = np.sum(w2*ddsigR,axis=2) 
    dsigL = np.sum(w2*ddsigL,axis=2) 

    #--integrate over X
    sigR = np.sum(w1*dsigR,axis=1) 
    sigL = np.sum(w1*dsigL,axis=1) 

    #--Jacobian dQ2/dy
    yjac = X*S

    #--assuming same luminosity
    NR = lum*sigR*yjac
    NL = lum*sigL*yjac

    #--measured asymmetry (already multiplied by pol in idis/residuals)
    Am = np.array(value)
 
    #--absolute uncertainty (not divided by sigma) 
    stat2 = (1 + Am**2)/(NR + NL)/(pol**2)

    stat = np.sqrt(stat2)

    #--statistical uncertainty
    data['stat_u'] = stat

    #--polarization uncertainty (1%)
    data['pol_u']  = Am*0.01

    #--add systemic uncertainties outside of polarization
    Y = np.array(data['Q2'])/2/np.array(data['X'])/((S-M2)/2)

    #--optimistic: no extra errors
    if est == 'opt':
        data['syst_u'] = Am*0.00

    #--moderate: 1% below y = 0.01, 1.5% above 
    elif est == 'mod':
        data['syst_u'] = np.zeros(l)
        for i in range(l):
            if Y[i] <= 0.01: data['syst_u'][i] = Am[i]*0.010
            if Y[i] >  0.01: data['syst_u'][i] = Am[i]*0.015

    #--pessimistic: do not have yet
    elif est == 'pes':
        return

    else:
        print('est must be opt, mod, or pes')
        return

    return data['stat_u'],data['pol_u'],data['syst_u']

def A_PV_had_errors(wdir,kind,tar,est,value,lum):

    conf['aux'] = AUX()
    conf['eweak'] = EWEAK()
    data = pd.read_excel('%s/sim/pvdis-%s-%s-%s.xlsx'%(wdir,kind,tar,est), index=False)
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

    pol = data['pol'][0]

    RS = data['RS'][0]
    S  = RS**2

    M2 = conf['aux'].M2

    if tar=='d': M2 = 4*M2

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

    idis._update()
    pidis._update()

    g1gZ = lambda x,q2: pidis.get_stf(x,q2,stf='g1gZ',tar=tar) 
    g5gZ = lambda x,q2: pidis.get_stf(x,q2,stf='g5gZ',tar=tar) 
    F2g  = lambda x,q2: idis.get_stf(x,q2,stf='F2g'  ,tar=tar) 
    FLg  = lambda x,q2: idis.get_stf(x,q2,stf='FLg'  ,tar=tar) 
    F2gZ = lambda x,q2: idis.get_stf(x,q2,stf='F2gZ' ,tar=tar) 
    FLgZ = lambda x,q2: idis.get_stf(x,q2,stf='FLgZ' ,tar=tar) 
    F3gZ = lambda x,q2: idis.get_stf(x,q2,stf='F3gZ' ,tar=target) 

    rho2 = lambda x,q2: 1 + 4*x**2*M2/q2

    y=lambda x,q2: (q2/2/x)/((S-M2)/2)

    YP = lambda x,q2: y(x,q2)**2 - 2*y(x,q2) +2
    YM = lambda x,q2: 1-(1-y(x,q2))**2

    sin2w = lambda q2: conf['eweak'].get_sin2w(q2)
    alpha = lambda q2: conf['eweak'].get_alpha(q2)

    gA = -0.5
    gV = lambda q2: -0.5 + 2*sin2w(q2)

    C  = lambda q2: GF*q2/(2*np.sqrt(2)*np.pi*alpha(q2))
  
    C1 = lambda x,q2: np.pi*alpha(q2)**2/(x*y(x,q2)*q2)

    T1g  = lambda x,q2: YP(x,q2)*F2g(x,q2)  - y(x,q2)**2*FLg(x,q2)
    T1gZ = lambda x,q2: YP(x,q2)*F2gZ(x,q2) - y(x,q2)**2*FLgZ(x,q2)

    T2 = lambda x,q2: x*YM(x,q2)*F3gZ(x,q2)

    T3 = lambda x,q2: YP(x,q2)*gV(q2)*g5gZ(x,q2) + YM(x,q2)*gA*g1gZ(x,q2)

    _ddsigR = lambda x,q2: C1(x,q2)*(T1g(x,q2) + C(q2)*(gV(q2)*T1gZ(x,q2) + gA*T2(x,q2)) + 2*x*C(q2)*T3(x,q2))
    _ddsigL = lambda x,q2: C1(x,q2)*(T1g(x,q2) + C(q2)*(gV(q2)*T1gZ(x,q2) + gA*T2(x,q2)) - 2*x*C(q2)*T3(x,q2))

    #--integrate over bin
    z1,w1 = np.polynomial.legendre.leggauss(3)
    z2,w2 = np.polynomial.legendre.leggauss(3)

    ddsigR = np.zeros((len(X),len(z1),len(z2)))
    ddsigL = np.zeros((len(X),len(z1),len(z2)))
    for i in range(len(X)):
        _x   = 0.5*((Xup[i] -Xdo[i])*z1  + Xup[i]  + Xdo[i])
        _q2  = 0.5*((Q2up[i]-Q2do[i])*z2 + Q2up[i] + Q2do[i])
        xjac  = 0.5*(Xup[i] -Xdo[i])
        q2jac = 0.5*(Q2up[i]-Q2do[i])
        for j in range(len(_x)):
            for k in range(len(_q2)):
                ddsigR[i][j][k] = _ddsigR(_x[j],_q2[k])*xjac*q2jac
                ddsigL[i][j][k] = _ddsigL(_x[j],_q2[k])*xjac*q2jac
   
    #--integrate over Q2
    dsigR = np.sum(w2*ddsigR,axis=2) 
    dsigL = np.sum(w2*ddsigL,axis=2) 

    #--integrate over X
    sigR = np.sum(w1*dsigR,axis=1) 
    sigL = np.sum(w1*dsigL,axis=1) 


    #--Jacobian dQ2/dy
    yjac = X*S

    NR = lum*sigR*yjac
    NL = lum*sigL*yjac

    #--polarization and polarization uncertainty
    P    = 0.7
    sigP = 0.07

    #--measured asymmetry (already multiplied by pol in pidis/residuals)
    Am = np.array(value)
 
    #--absolute uncertainty (not divided by sigma) 
    stat2 = (1 + Am**2)/(NR + NL)/(P**2)

    stat = np.sqrt(stat2)

    #--statistical uncertainties
    data['stat_u'] = stat

    #--polarization uncertainty (1%)
    data['pol_u']  = Am*0.01

    #--add systemic uncertainties beyond polarization
    Y = np.array(data['Q2'])/2/np.array(data['X'])/((S-M2)/2)

    #--optimistic: flat 1%
    if est == 'opt':
        data['syst_u'] = Am*0.01

    #--moderate: 2% below y = 0.01, 2.5% above 
    elif est == 'mod':
        data['syst_u'] = np.zeros(l)
        for i in range(l):
            if Y[i] <= 0.01: data['syst_u'][i] = Am[i]*0.020
            if Y[i] >  0.01: data['syst_u'][i] = Am[i]*0.025
    #--pessimistic: do not have yet
    elif est == 'pes':
        return

    else:
        print('est must be opt, mod, or pes')
        return

    return data['stat_u'],data['pol_u'],data['syst_u']

def convert_lum(lum):
    one=0.3893793721  #--GeV2 mbarn from PDG
    lum,units=lum.split(':')
    lum=float(lum)
    units=units.strip()
    if units=='fb-1':   return lum*one*1e12
    else:               sys.exit('units not convertible!')

def plot_errors(wdir,kind,tar,est,lum):

    nrows,ncols=1,1
    fig = py.figure(figsize=(ncols*8,nrows*5))
    ax11=py.subplot(nrows,ncols,1)

    tab   = pd.read_excel('%s/sim/pvdis-%s-%s-%s.xlsx'%(wdir,kind,tar,est))
    tab   = tab.to_dict(orient='list')
    X     = np.array(tab['X'])
    value = np.array(tab['value'])
    stat  = np.abs(np.array(tab['stat_u'])/value)
    pol   = np.abs(np.array(tab['pol_u']) /value)
    syst  = np.abs(np.array(tab['syst_u'])/value)

    #--check for zero systematic uncertainty
    zero = True
    for i in range(len(syst)):
        if syst[i] != 0: zero = False

    alpha = np.sqrt((stat**2 + pol**2 + syst**2))

    hand = {}
    hand['alpha']                 = ax11.scatter(X,alpha,color='red'    ,s=20,marker='s')
    hand['stat']                  = ax11.scatter(X,stat ,color='green'  ,s=10,marker='o')
    hand['pol']                   = ax11.scatter(X,pol  ,color='blue'   ,s=10,marker='*')
    if zero != True: hand['syst'] = ax11.scatter(X,syst ,color='magenta',s=10,marker='v')

    ax11.set_xlim(1e-4,1)
    ax11.semilogx()
    ax11.semilogy()

    if kind == 'e':
        ax11.set_ylim(1e-4,1e-1)
        ax11.set_ylabel(r'$|\sigma_{A_{PV}^e}/A_{PV}^e|$',size=30)
        if est == 'opt': ax11.text(0.6,0.4,r'\textrm{Optimistic}' ,transform = ax11.transAxes,size=30)
        if est == 'mod': ax11.text(0.6,0.4,r'\textrm{Moderate}'   ,transform = ax11.transAxes,size=30)
        if est == 'pes': ax11.text(0.6,0.4,r'\textrm{Pessimistic}',transform = ax11.transAxes,size=30)
    if kind == 'had':
        ax11.set_ylim(1e-3,1e3)
        ax11.set_yticks([1e-3,1e-2,1e-1,1e0,1e1,1e2,1e3])
        locmin = matplotlib.ticker.LogLocator(base=10.0,subs=(0.2,0.4,0.6,0.8),numticks=7)
        ax11.yaxis.set_minor_locator(locmin)
        ax11.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
        ax11.set_ylabel(r'$|\sigma_{A_{PV}^{had}}/A_{PV}^{had}|$',size=30)
        if est == 'opt': ax11.text(0.6,0.6,r'\textrm{Optimistic}' ,transform = ax11.transAxes,size=30)
        if est == 'mod': ax11.text(0.6,0.6,r'\textrm{Moderate}'   ,transform = ax11.transAxes,size=30)
        if est == 'pes': ax11.text(0.6,0.6,r'\textrm{Pessimistic}',transform = ax11.transAxes,size=30)


    ax11.set_xlabel(r'$x$',size=30)

    ax11.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=30)


    if tar == 'p':   ax11.text(0.7,0.85,r'\textrm{Proton}'     ,transform = ax11.transAxes,size=30)
    if tar == 'd':   ax11.text(0.7,0.85,r'\textrm{Deuteron}'   ,transform = ax11.transAxes,size=30)

    handles = [hand['alpha'],hand['stat'],hand['pol']]
    label1 = r'\textbf{\textrm{Total}}'
    label2 = r'\textbf{\textrm{Stat}}'
    label3 = r'\textbf{\textrm{Pol}}'
    labels = [label1,label2,label3]

    if zero != True:
        handles.append(hand['syst'])
        labels.append(r'\textbf{\textrm{Syst}}')

    ax11.legend(handles,labels,loc='lower left', fontsize = 20, frameon = 0, handletextpad = 0.3, handlelength = 1.0)
    py.tight_layout()
    checkdir('%s/gallery'%wdir)
    filename = '%s/gallery/pvdis-errors-%s-%s-%s'%(wdir,kind,tar,est)
    py.savefig(filename)
    print('Saving error plot to %s'%filename)
    py.clf()

#--generate lhapdf info and data files
def gen_lhapdf_info_file(wdir,kind,tar,est):

    info={}
    if kind == 'e':   info['<description>'] = 'PVDIS (electron)'
    if kind == 'had': info['<description>'] = 'PVDIS (hadron)'
    info['<index>']       = '0'
    info['<authors>']     = 'JAM Collaboration'
    info['<reference>']   = ''
    info['<particle>']    = '%s'%tar

    #--get tables
    X,Q2,table,replicas=get_tables(wdir,kind,tar,est)

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

def gen_lhapdf_dat_file(wdir,kind,tar,est):

    #--get tables
    X,Q2,central,replicas=get_tables(wdir,kind,tar,est)
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

def get_tables(wdir,kind,tar,est):
    replicas = []
    tab=pd.read_excel('%s/sim/pvdis-%s-%s-%s.xlsx'%(wdir,kind,tar,est))
    tab=tab.to_dict(orient='list')
    central = tab['value']
    _replicas = {}
    for key in tab:
        if key[:5] != 'value': continue
        if key     == 'value': continue
        _replicas[key] = tab[key]
    for i in range(len(_replicas)):
        replicas.append(_replicas['value%s'%(i+1)])

    #--get specific points from data file at fitpack/database/pvdis/expdata/1000.xlsx
    fdir = os.environ['FITPACK']
    grid = pd.read_excel(fdir + '/database/pvdis/expdata/1000.xlsx')
    grid = grid.to_dict(orient='list')
    X    = grid['X']
    Q2   = grid['Q2']

    return X,Q2,central,replicas







 
