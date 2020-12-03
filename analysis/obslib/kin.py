#!/usr/bin/env python

import sys,os
import numpy as np
import copy

#--matplotlib
import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import cm
import pylab as py

#--from local
from analysis.corelib import core,classifier

#--from tools
from tools.tools     import load,save,checkdir,lprint
from tools.config    import conf,load_config

#--from fitpack
from obslib.idis.reader    import READER as idisREAD
from obslib.pidis.reader   import READER as pidisREAD
from obslib.dy.reader      import READER as dyREAD
from obslib.wasym.reader   import READER as wasymREAD
from obslib.zrap.reader    import READER as zrapREAD
from obslib.wzrv.reader    import READER as wzrvREAD
from obslib.pjets.reader   import READER as pjetREAD
from qcdlib import aux

conf['aux']=aux.AUX()

#--make kinematic plots

def plot(wdir,pol):

    data = load_data(pol)
    if pol: plot_kin_pol(wdir,data)
    else:   plot_kin_upol(wdir,data)

def get_kin(exp,data):
    #--get X, Q2
    if exp == 'idis' or exp=='pidis':
        X  = data['X']
        Q2 = data['Q2']
    elif exp == 'dy' or exp == 'wasym' or exp == 'zrap':
        Y = data['Y']
        if exp == 'dy':
            Q2  = data['Q2']
            tau = data['tau']
        if exp == 'wasym':
            Q2  = 80.398**2*np.ones(len(Y))
            S   = data['S']
            tau = Q2/S
        if exp == 'zrap':
            Q2  = 91.1876**2*np.ones(len(Y))
            S   = data['S']
            tau = Q2/S
        X = np.sqrt(tau)*np.cosh(Y)
    elif exp == 'wzrv':
        if 'eta' in data:
            eta = data['eta']
        else:
            eta = (data['eta_min'] + data['eta_max'])
        Q2  = 80.398**2*np.ones(len(eta))
        S   = data['cms']**2
        tau = Q2/S
        X = np.sqrt(tau)*np.cosh(eta)
    elif exp == 'pjet':
        pT   = (data['pt-max'] + data['pt-min'])/2.0
        Q2   = pT**2
        S    = data['S']
        tau  = Q2/S
        if 'eta-max' in data:
            etamin,etamax = data['eta-max'],data['eta-min']
            Xmin = 2*np.sqrt(tau)*np.cosh(etamin)
            Xmax = 2*np.sqrt(tau)*np.cosh(etamax)
            X = (Xmin+Xmax)/2.0
        else:
            eta = (data['eta-abs-max']+data['eta-abs-min'])/2.0
            X = 2*np.sqrt(tau)*np.cosh(eta)

    return X,Q2

def load_data(pol=False):

    conf['datasets'] = {}
    data = {}
    if pol==False:
        ##--IDIS
        Q2cut=1.3**2
        W2cut=3.0
        conf['datasets']['idis']={}
        conf['datasets']['idis']['filters']=[]
        conf['datasets']['idis']['filters'].append("Q2>%f"%Q2cut)
        conf['datasets']['idis']['filters'].append("W2>%f"%W2cut)
        conf['datasets']['idis']['xlsx']={}
        #------------------------------------------------------------------------------------------------------------------
        conf['datasets']['idis']['xlsx'][10010]='idis/expdata/10010.xlsx' # proton   | F2            | SLAC
        conf['datasets']['idis']['xlsx'][10016]='idis/expdata/10016.xlsx' # proton   | F2            | BCDMS
        conf['datasets']['idis']['xlsx'][10020]='idis/expdata/10020.xlsx' # proton   | F2            | NMC
        conf['datasets']['idis']['xlsx'][10003]='idis/expdata/10003.xlsx' # proton   | sigma red     | JLab Hall C (E00-106)
        conf['datasets']['idis']['xlsx'][10026]='idis/expdata/10026.xlsx' # proton   | sigma red     | HERA II NC e+ (1)
        conf['datasets']['idis']['xlsx'][10027]='idis/expdata/10027.xlsx' # proton   | sigma red     | HERA II NC e+ (2)
        conf['datasets']['idis']['xlsx'][10028]='idis/expdata/10028.xlsx' # proton   | sigma red     | HERA II NC e+ (3)
        conf['datasets']['idis']['xlsx'][10029]='idis/expdata/10029.xlsx' # proton   | sigma red     | HERA II NC e+ (4)
        conf['datasets']['idis']['xlsx'][10030]='idis/expdata/10030.xlsx' # proton   | sigma red     | HERA II NC e-
        conf['datasets']['idis']['xlsx'][10031]='idis/expdata/10031.xlsx' # proton   | sigma red     | HERA II CC e+
        conf['datasets']['idis']['xlsx'][10032]='idis/expdata/10032.xlsx' # proton   | sigma red     | HERA II CC e-
        #conf['datasets']['idis']['xlsx'][10007]='idis/expdata/10007.xlsx' # proton   | sigma red     | HERMES
        #------------------------------------------------------------------------------------------------------------------
        conf['datasets']['idis']['xlsx'][10011]='idis/expdata/10011.xlsx' # deuteron | F2            | SLAC
        conf['datasets']['idis']['xlsx'][10017]='idis/expdata/10017.xlsx' # deuteron | F2            | BCDMS
        conf['datasets']['idis']['xlsx'][10021]='idis/expdata/10021.xlsx' # d/p      | F2d/F2p       | NMC
        #conf['datasets']['idis']['xlsx'][10006]='idis/expdata/10006.xlsx' # deuteron | F2            | HERMES
        conf['datasets']['idis']['xlsx'][10002]='idis/expdata/10002.xlsx' # deuteron | F2            | JLab Hall C (E00-106)
        conf['datasets']['idis']['xlsx'][10033]='idis/expdata/10033.xlsx' # n/d      | F2n/F2d       | BONUS
        #------------------------------------------------------------------------------------------------------------------
        data['idis'] = idisREAD().load_data_sets('idis')  
 
        ##--DY 
        conf['datasets']['dy']={}
        conf['datasets']['dy']['filters']=[]
        conf['datasets']['dy']['filters'].append("Q2>36") 
        conf['datasets']['dy']['xlsx']={}
        #------------------------------------------------------------------------------------------------------------------
        conf['datasets']['dy']['xlsx'][10001]='dy/expdata/10001.xlsx'
        conf['datasets']['dy']['xlsx'][10002]='dy/expdata/10002.xlsx'
        #------------------------------------------------------------------------------------------------------------------
        data['dy'] = dyREAD().load_data_sets('dy')  
        
        ##--charge asymmetry 
        conf['datasets']['wzrv']={}
        conf['datasets']['wzrv']['filters']=[]
        conf['datasets']['wzrv']['xlsx']={}
        #------------------------------------------------------------------------------------------------------------------
        conf['datasets']['wzrv']['xlsx'][2000]='wzrv/expdata/2000.xlsx'
        conf['datasets']['wzrv']['xlsx'][2003]='wzrv/expdata/2003.xlsx'
        conf['datasets']['wzrv']['xlsx'][2006]='wzrv/expdata/2006.xlsx'
        conf['datasets']['wzrv']['xlsx'][2007]='wzrv/expdata/2007.xlsx'
        #conf['datasets']['wzrv']['xlsx'][2008]='wzrv/expdata/2008.xlsx'  #--ATLAS 2011 w/ correlated uncertainties
        conf['datasets']['wzrv']['xlsx'][2009]='wzrv/expdata/2009.xlsx'
        conf['datasets']['wzrv']['xlsx'][2010]='wzrv/expdata/2010.xlsx'
        conf['datasets']['wzrv']['xlsx'][2011]='wzrv/expdata/2011.xlsx'
        conf['datasets']['wzrv']['xlsx'][2012]='wzrv/expdata/2012.xlsx'
        conf['datasets']['wzrv']['xlsx'][2013]='wzrv/expdata/2013.xlsx'
        conf['datasets']['wzrv']['xlsx'][2014]='wzrv/expdata/2014.xlsx'
        conf['datasets']['wzrv']['xlsx'][2015]='wzrv/expdata/2015.xlsx'  #--ATLAS 2011 w/ uncorrelated uncertainties
        #------------------------------------------------------------------------------------------------------------------
        data['wzrv'] = wzrvREAD().load_data_sets('wzrv')  
        
        ##--W asymmetry 
        conf['datasets']['wasym']={}
        conf['datasets']['wasym']['filters']=[]
        conf['datasets']['wasym']['xlsx']={}
        #------------------------------------------------------------------------------------------------------------------
        conf['datasets']['wasym']['xlsx'][1000]='wasym/expdata/1000.xlsx'
        conf['datasets']['wasym']['xlsx'][1001]='wasym/expdata/1001.xlsx'
        #------------------------------------------------------------------------------------------------------------------
        data['wasym'] = wasymREAD().load_data_sets('wasym')  
        
        ##--W asymmetry 
        conf['datasets']['zrap']={}
        conf['datasets']['zrap']['filters']=[]
        conf['datasets']['zrap']['xlsx']={}
        #------------------------------------------------------------------------------------------------------------------
        conf['datasets']['zrap']['xlsx'][1000]='zrap/expdata/1000.xlsx'
        conf['datasets']['zrap']['xlsx'][1001]='zrap/expdata/1001.xlsx'
        #------------------------------------------------------------------------------------------------------------------
        data['zrap'] = zrapREAD().load_data_sets('zrap')

    if pol==True:
        conf['datasets']['pidis']={}
        #------------------------------------------------------------------------------------------------------------------
        conf['datasets']['pidis']['filters']=[]
        #------------------------------------------------------------------------------------------------------------------
        conf['datasets']['pidis']['filters'].append("Q2>1.3**2") 
        conf['datasets']['pidis']['filters'].append("W2>10.0") 
        #------------------------------------------------------------------------------------------------------------------
        conf['datasets']['pidis']['xlsx']={}
        #---------------------------------------------------------------------------------------------------------------------------
        conf['datasets']['pidis']['xlsx'][10002]='pidis/expdata/10002.xlsx' # 10002 | proton   | A1   | COMPASS         |          |
        conf['datasets']['pidis']['xlsx'][10003]='pidis/expdata/10003.xlsx' # 10003 | proton   | A1   | COMPASS         |          |
        conf['datasets']['pidis']['xlsx'][10004]='pidis/expdata/10004.xlsx' # 10004 | proton   | A1   | EMC             |          |
        conf['datasets']['pidis']['xlsx'][10007]='pidis/expdata/10007.xlsx' # 10007 | proton   | Apa  | HERMES          |          |
        conf['datasets']['pidis']['xlsx'][10008]='pidis/expdata/10008.xlsx' # 10008 | proton   | A2   | HERMES          |          |
        conf['datasets']['pidis']['xlsx'][10017]='pidis/expdata/10017.xlsx' # 10017 | proton   | Apa  | JLabHB(EG1DVCS) |          |
        conf['datasets']['pidis']['xlsx'][10022]='pidis/expdata/10022.xlsx' # 10022 | proton   | Apa  | SLAC(E143)      |          |
        conf['datasets']['pidis']['xlsx'][10023]='pidis/expdata/10023.xlsx' # 10023 | proton   | Ape  | SLAC(E143)      |          |
        conf['datasets']['pidis']['xlsx'][10028]='pidis/expdata/10028.xlsx' # 10028 | proton   | Ape  | SLAC(E155)      |          |
        conf['datasets']['pidis']['xlsx'][10029]='pidis/expdata/10029.xlsx' # 10029 | proton   | Apa  | SLAC(E155)      |          |
        conf['datasets']['pidis']['xlsx'][10031]='pidis/expdata/10031.xlsx' # 10031 | proton   | Atpe | SLAC(E155x)     |          |
        conf['datasets']['pidis']['xlsx'][10032]='pidis/expdata/10032.xlsx' # 10032 | proton   | Apa  | SLACE80E130     |          |
        conf['datasets']['pidis']['xlsx'][10035]='pidis/expdata/10035.xlsx' # 10035 | proton   | A1   | SMC             |          |
        conf['datasets']['pidis']['xlsx'][10036]='pidis/expdata/10036.xlsx' # 10036 | proton   | A1   | SMC             |          |
        conf['datasets']['pidis']['xlsx'][10041]='pidis/expdata/10041.xlsx' # 10041 | proton   | Apa  | JLabHB(EG1b)    | E =1 GeV |
        conf['datasets']['pidis']['xlsx'][10042]='pidis/expdata/10042.xlsx' # 10042 | proton   | Apa  | JLabHB(EG1b)    | E =2 GeV |
        conf['datasets']['pidis']['xlsx'][10043]='pidis/expdata/10043.xlsx' # 10043 | proton   | Apa  | JLabHB(EG1b)    | E =4 GeV |
        conf['datasets']['pidis']['xlsx'][10044]='pidis/expdata/10044.xlsx' # 10044 | proton   | Apa  | JLabHB(EG1b)    | E =5 GeV |
        conf['datasets']['pidis']['xlsx'][10005]='pidis/expdata/10005.xlsx' # 10005 | neutron  | A1   | HERMES          |          |
        #---------------------------------------------------------------------------------------------------------------------------
        conf['datasets']['pidis']['xlsx'][10001]='pidis/expdata/10001.xlsx' # 10001 | deuteron | A1   | COMPASS         |          |
        conf['datasets']['pidis']['xlsx'][10006]='pidis/expdata/10006.xlsx' # 10006 | deuteron | Apa  | HERMES          |          |
        conf['datasets']['pidis']['xlsx'][10016]='pidis/expdata/10016.xlsx' # 10016 | deuteron | Apa  | JLabHB(EG1DVCS) |          |
        conf['datasets']['pidis']['xlsx'][10020]='pidis/expdata/10020.xlsx' # 10020 | deuteron | Ape  | SLAC(E143)      |          |
        conf['datasets']['pidis']['xlsx'][10021]='pidis/expdata/10021.xlsx' # 10021 | deuteron | Apa  | SLAC(E143)      |          |
        conf['datasets']['pidis']['xlsx'][10026]='pidis/expdata/10026.xlsx' # 10026 | deuteron | Ape  | SLAC(E155)      |          |
        conf['datasets']['pidis']['xlsx'][10027]='pidis/expdata/10027.xlsx' # 10027 | deuteron | Apa  | SLAC(E155)      |          |
        conf['datasets']['pidis']['xlsx'][10030]='pidis/expdata/10030.xlsx' # 10030 | deuteron | Atpe | SLAC(E155x)     |          |
        conf['datasets']['pidis']['xlsx'][10033]='pidis/expdata/10033.xlsx' # 10033 | deuteron | A1   | SMC             |          |
        conf['datasets']['pidis']['xlsx'][10034]='pidis/expdata/10034.xlsx' # 10034 | deuteron | A1   | SMC             |          |
        conf['datasets']['pidis']['xlsx'][10037]='pidis/expdata/10037.xlsx' # 10037 | deuteron | Apa  | JLabHB(EG1b)    | E =1 GeV |
        conf['datasets']['pidis']['xlsx'][10038]='pidis/expdata/10038.xlsx' # 10038 | deuteron | Apa  | JLabHB(EG1b)    | E =2 GeV |
        conf['datasets']['pidis']['xlsx'][10039]='pidis/expdata/10039.xlsx' # 10039 | deuteron | Apa  | JLabHB(EG1b)    | E =4 GeV |
        conf['datasets']['pidis']['xlsx'][10040]='pidis/expdata/10040.xlsx' # 10040 | deuteron | Apa  | JLabHB(EG1b)    | E =5 GeV |
        #---------------------------------------------------------------------------------------------------------------------------
        conf['datasets']['pidis']['xlsx'][10009]='pidis/expdata/10009.xlsx' # 10009 | helium   | Apa  | JLabHA(E01-012) | < cuts  |
        conf['datasets']['pidis']['xlsx'][10010]='pidis/expdata/10010.xlsx' # 10010 | helium   | Apa  | JLabHA(E06-014) |          |
        conf['datasets']['pidis']['xlsx'][10011]='pidis/expdata/10011.xlsx' # 10011 | helium   | Ape  | JLabHA(E06-014) |          |
        conf['datasets']['pidis']['xlsx'][10012]='pidis/expdata/10012.xlsx' # 10012 | helium   | Apa  | JLabHA(E97-103) | < cuts  |
        conf['datasets']['pidis']['xlsx'][10013]='pidis/expdata/10013.xlsx' # 10013 | helium   | Ape  | JLabHA(E97-103) | < cuts  |
        conf['datasets']['pidis']['xlsx'][10014]='pidis/expdata/10014.xlsx' # 10014 | helium   | Apa  | JLabHA(E99-117) |          |
        conf['datasets']['pidis']['xlsx'][10015]='pidis/expdata/10015.xlsx' # 10015 | helium   | Ape  | JLabHA(E99-117) |          |
        conf['datasets']['pidis']['xlsx'][10018]='pidis/expdata/10018.xlsx' # 10018 | helium   | A1   | SLAC(E142)      |          |
        conf['datasets']['pidis']['xlsx'][10019]='pidis/expdata/10019.xlsx' # 10019 | helium   | A2   | SLAC(E142)      |          |
        conf['datasets']['pidis']['xlsx'][10024]='pidis/expdata/10024.xlsx' # 10024 | helium   | Ape  | SLAC(E154)      |          |
        conf['datasets']['pidis']['xlsx'][10025]='pidis/expdata/10025.xlsx' # 10025 | helium   | Apa  | SLAC(E154)      |          |
        #---------------------------------------------------------------------------------------------------------------------------
        conf['datasets']['pidis']['xlsx'][90001]='EIC/expdata/90001.xlsx' 
        conf['datasets']['pidis']['xlsx'][90002]='EIC/expdata/90002.xlsx' 
        #---------------------------------------------------------------------------------------------------------------------------
        data['pidis'] = pidisREAD().load_data_sets('pidis')

        ##--charge asymmetry 
        conf['datasets']['wzrv']={}
        conf['datasets']['wzrv']['filters']=[]
        conf['datasets']['wzrv']['xlsx']={}
        #------------------------------------------------------------------------------------------------------------------
        conf['datasets']['wzrv']['xlsx'][1000]='wzrv/expdata/1000.xlsx'
        conf['datasets']['wzrv']['xlsx'][1001]='wzrv/expdata/1001.xlsx'
        #------------------------------------------------------------------------------------------------------------------
        data['wzrv'] = wzrvREAD().load_data_sets('wzrv')  

        ##--PJET
        conf['datasets']['pjet'] = {}
        conf['datasets']['pjet']['filters'] = []
        conf['datasets']['pjet']['filters'].append("pT>10.0")
        conf['datasets']['pjet']['xlsx'] = {}
        conf['datasets']['pjet']['xlsx'][20001] = 'pjets/expdata/20001.xlsx' ## STAR 2006 paper on 2003 and 2004 data
        conf['datasets']['pjet']['xlsx'][20002] = 'pjets/expdata/20002.xlsx' ## STAR 2012 paper on 2005 data
        conf['datasets']['pjet']['xlsx'][20003] = 'pjets/expdata/20003.xlsx' ## STAR 2012 paper on 2006 data
        conf['datasets']['pjet']['xlsx'][20004] = 'pjets/expdata/20004.xlsx' ## STAR 2015 paper on 2009 data
        conf['datasets']['pjet']['xlsx'][20005] = 'pjets/expdata/20005.xlsx' ## PHENIX 2011 paper on 2005 data
        conf['datasets']['pjet']['xlsx'][20006] = 'pjets/expdata/20006.xlsx' ## STAR 2019 paper on 2012 data
        conf['pjet_qr_fit'] = {'method': 'fixed', 'f_scale': 1.0, 'r_scale': 1.0}
        data['pjet'] = pjetREAD().load_data_sets('pjet')  


    return data

def plot_kin_upol(wdir,data):
    s = 35

    nrows,ncols=1,1
    fig = py.figure(figsize=(ncols*14,nrows*8))
    ax=py.subplot(nrows,ncols,1)

    divider = make_axes_locatable(ax)
    axL = divider.append_axes("right",size=6,pad=0,sharey=ax)
    axL.set_xlim(0.1,0.9)
    axL.spines['left'].set_visible(False)
    axL.yaxis.set_ticks_position('right')
    py.setp(axL.get_xticklabels(),visible=True)

    ax.spines['right'].set_visible(False)

    hand = {}
    for exp in data:
        hand[exp] = {}
        for idx in data[exp]:
            X,Q2 = get_kin(exp,data[exp][idx])
            X1,  X2  = [], []
            Q21, Q22 = [], []
            for i in range(len(X)):
                if X[i] < 0.1:
                    X1.append(X[i])
                    Q21.append(Q2[i])
                else:
                    X2.append(X[i])
                    Q22.append(Q2[i])
            label = None
            if exp == 'idis':
                if idx==10016:   marker,color,label  = '^','black',    'BCDMS'
                elif idx==10017: marker,color        = '^','black'
                elif idx==10020: marker,color,label  = '+','goldenrod','NMC'
                elif idx==10021: marker,color        = '+','goldenrod'
                elif idx==10010: marker,color,label  = 'v','blue',     'SLAC'
                elif idx==10011: marker,color        = 'v','blue'
                elif idx==10026: marker,color,label  = 'o','green',    'HERA'
                elif idx==10027: marker,color        = 'o','green'
                elif idx==10028: marker,color        = 'o','green'
                elif idx==10029: marker,color        = 'o','green'
                elif idx==10030: marker,color        = 'o','green'
                elif idx==10031: marker,color        = 'o','green'
                elif idx==10032: marker,color        = 'o','green'
                elif idx==10033: marker,color,label  = 's','orange',   'JLab BONuS'
                elif idx==10002: marker,color,label  = 'x','red',      'JLab Hall C'
                elif idx==10003: marker,color        = 'x','red'
                else: continue
            if exp == 'dy':
                if idx == 10001: marker,color,label  = 'D','magenta','FNAL E866'
            if exp == 'wasym':
                if idx == 1000:  marker,color,label  = 'p','maroon','CDF/D0'
            if exp == 'zrap':
                marker,color,label = 'p', 'maroon', None
            if exp == 'wzrv':
                if idx == 2000: marker,color       = 'p','maroon'
                if idx == 2003: marker,color       = 'p','maroon'
                if idx == 2006: marker,color       = 'p','maroon'
                if idx == 2007: marker,color,label = '*','darkcyan','ATLAS/CMS'
                if idx == 2009: marker,color       = '*','darkcyan'
                if idx == 2010: marker,color       = '*','darkcyan'
                if idx == 2011: marker,color       = '*','darkcyan'
                if idx == 2012: marker,color       = '*','darkcyan'
                if idx == 2013: marker,color       = '*','darkcyan'
                if idx == 2014: marker,color       = '*','darkcyan'
                if idx == 2015: marker,color       = '*','darkcyan'

            ax .scatter(X1,Q21,c=color,label=label,s=s,marker=marker)
            hand[label] = axL.scatter(X2,Q22,c=color,s=s,marker=marker)


    #--Plot cuts
    x = np.linspace(0.1,0.9,100)
    W2cut10_p=np.zeros(len(x))
    W2cut10_d=np.zeros(len(x))
    W2cut3_p=np.zeros(len(x))
    W2cut3_d=np.zeros(len(x))
    Q2cut=np.ones(len(x))*1.3**2

    for i in range(len(x)):
        W2cut10_p[i]=(10.0-(0.938)**2)*(x[i]/(1-x[i]))
        W2cut10_d[i]=(10.0-(1.8756)**2)*(x[i]/(1-x[i]))
        W2cut3_p[i]=(3.0-(0.938)**2)*(x[i]/(1-x[i]))
        W2cut3_d[i]=(3.0-(1.8756)**2)*(x[i]/(1-x[i]))

    hand['W2=10'] ,= axL.plot(x,W2cut10_p,'k--')
    hand['W2=3']  ,= axL.plot(x,W2cut3_p,c='k')

    ax.axvline(0.1,color='black',ls=':',alpha=0.5)

    ax .tick_params(axis='both',which='both',top=True,right=False,direction='in',labelsize=30)
    axL.tick_params(axis='both',which='both',top=True,right=True,labelright=False,direction='in',labelsize=30)

    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_xlim(2e-5,0.1)
    ax.set_ylim(1,10e4)
    ax. set_xticks([1e-4,1e-3,1e-2])
    ax. set_xticklabels([r'$10^{-4}$',r'$10^{-3}$',r'$10^{-2}$'])
    axL.set_xticks([0.1,0.3,0.5,0.7])

    axL.set_xlabel(r'\boldmath$x$',size=40)
    axL.xaxis.set_label_coords(0.95,0.00)
    ax.set_ylabel(r'\boldmath$Q^2$' + '  ' + r'\textbf{\textrm{(GeV}}' + r'\boldmath$^2)$', size=40)

    handles,labels = [], []
    handles.append(hand['BCDMS'])
    handles.append(hand['NMC'])
    handles.append(hand['SLAC'])
    handles.append(hand['JLab BONuS'])
    handles.append(hand['JLab Hall C'])
    handles.append(hand['HERA'])
    handles.append(hand['FNAL E866'])
    handles.append(hand['CDF/D0'])
    handles.append(hand['ATLAS/CMS'])
    handles.append(hand['W2=10'])
    handles.append(hand['W2=3'])
    labels.append(r'\textbf{\textrm{BCDMS}}')
    labels.append(r'\textbf{\textrm{NMC}}')
    labels.append(r'\textbf{\textrm{SLAC}}')
    labels.append(r'\textbf{\textrm{JLab BONuS}}')
    labels.append(r'\textbf{\textrm{JLab Hall C}}')
    labels.append(r'\textbf{\textrm{HERA}}')
    labels.append(r'\textbf{\textrm{FNAL E866}}')
    labels.append(r'\textbf{\textrm{CDF/D0}}')
    labels.append(r'\textbf{\textrm{ATLAS/CMS}}')
    labels.append(r'\boldmath$W^2 = 10$' + ' ' + r'\textbf{\textrm{GeV}}' + r'\boldmath$^2$')
    labels.append(r'\boldmath$W^2 = 3$' + '  ' + r'\textbf{\textrm{GeV}}' + r'\boldmath$^2$')
    ax.legend(handles,labels,loc='upper left',fontsize=20,frameon=False, handlelength = 1.0, handletextpad = 0.1)

    py.tight_layout()
    filename='%s/gallery/kinematics-upol'%wdir
    filename+='.png'

    py.savefig(filename)
    print 'Saving figure to %s'%filename 
 
def plot_kin_pol(wdir,data):

    nrows,ncols=1,1
    fig = py.figure(figsize=(ncols*14,nrows*8))
    ax=py.subplot(nrows,ncols,1)

    divider = make_axes_locatable(ax)
    axL = divider.append_axes("right",size=6,pad=0,sharey=ax)
    axL.spines['left'].set_visible(False)
    axL.yaxis.set_ticks_position('right')
    py.setp(axL.get_xticklabels(),visible=True)

    ax.spines['right'].set_visible(False)

    hand = {}
    for exp in data:
        hand[exp] = {}
        for idx in data[exp]:
            X,Q2 = get_kin(exp,data[exp][idx])
            X1,  X2  = [], []
            Q21, Q22 = [], []
            for i in range(len(X)):
                if X[i] < 0.1:
                    X1.append(X[i])
                    Q21.append(Q2[i])
                else:
                    X2.append(X[i])
                    Q22.append(Q2[i])
            label = None
            if exp == 'pidis':
                if idx==10001:   marker,color,label = 'o','darkcyan', 'COMPASS'    
                elif idx==10002: marker,color       = 'o','darkcyan'    
                elif idx==10003: marker,color       = 'o','darkcyan'    
                elif idx==10004: marker,color,label = 's','gray',  'EMC'
                elif idx==10033: marker,color,label = '*','magenta',  'SMC'
                elif idx==10034: marker,color       = '*','magenta'
                elif idx==10035: marker,color       = '*','magenta'
                elif idx==10036: marker,color       = '*','magenta'
                elif idx==10006: marker,color,label = 'v','purple', 'HERMES'
                elif idx==10007: marker,color       = 'v','purple'
                elif idx==10008: marker,color       = 'v','purple'
                elif idx==10018: marker,color,label = '^','goldenrod', 'SLAC'
                elif idx==10019: marker,color       = '^','goldenrod'
                elif idx==10020: marker,color       = '^','goldenrod'
                elif idx==10021: marker,color       = '^','goldenrod'
                elif idx==10022: marker,color       = '^','goldenrod'
                elif idx==10023: marker,color       = '^','goldenrod'
                elif idx==10024: marker,color       = '^','goldenrod'
                elif idx==10025: marker,color       = '^','goldenrod'
                elif idx==10026: marker,color       = '^','goldenrod'
                elif idx==10027: marker,color       = '^','goldenrod'
                elif idx==10028: marker,color       = '^','goldenrod'
                elif idx==10029: marker,color       = '^','goldenrod'
                elif idx==10030: marker,color       = '^','goldenrod'
                elif idx==10031: marker,color       = '^','goldenrod'
                elif idx==10032: marker,color       = '^','goldenrod'
                elif idx==90001: marker,color,label = 'o','red', 'EIC p'
                elif idx==90002: marker,color,label = 'o','darkgreen', 'EIC A'
                else: continue
                s=35

            elif exp=='pjet':
                if   idx==20001:   marker,color,label = 'v', 'blue', 'RHIC jets'
                elif idx==20002:   marker,color       = 'v', 'blue' 
                elif idx==20003:   marker,color       = 'v', 'blue' 
                elif idx==20004:   marker,color       = 'v', 'blue' 
                elif idx==20006:   marker,color       = 'v', 'blue' 
                elif idx==20005:   marker,color,label = 'v', 'blue', 'RHIC jets' 
                s=50

            else: continue

            if exp=='pidis' and idx==90002: s,facecolors,width=80,'none',2.0
            else:                             facecolors,width=color, 1.0

            ax .scatter(X1,Q21,label=label,s=s,marker=marker,facecolors=facecolors,edgecolors=color,linewidth=width)
            hand[label] = axL.scatter(X2,Q22,s=s,marker=marker,facecolors=facecolors,edgecolors=color,linewidth=width)

    #--Plot cuts
    x1 = np.linspace(1e-3,1e-1,100)
    x2 = np.linspace(0.1,0.9,100)
    M2 = 0.938**2

    W2cut1 = [(10-M2)*x/(1-x) for x in x1]
    W2cut2 = [(10-M2)*x/(1-x) for x in x2]

    hand['cut'] ,= ax.plot(x1,W2cut1,'k--')
    axL             .plot(x2,W2cut2,'k--')

    ax.axvline(0.1,color='black',ls=':',alpha=0.5)

    ax .tick_params(axis='both',which='both',top=True,right=False,direction='in',labelsize=30)
    axL.tick_params(axis='both',which='both',top=True,right=True,labelright=False,direction='in',labelsize=30)

    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_xlim(1e-4,0.1)
    axL.set_xlim(0.1,0.7)
    ax.set_ylim(1.0,5e3)
    ax. set_xticks([1e-3,1e-2])
    ax. set_xticklabels([r'$10^{-3}$',r'$10^{-2}$'])
    axL.set_xticks([0.1,0.3,0.5])

    axL.set_xlabel(r'\boldmath$x$',size=40)
    axL.xaxis.set_label_coords(0.95,0.00)
    ax.set_ylabel(r'\boldmath$Q^2/p_T^2~(\rm{GeV}^2)$', size=40)

    handles,labels = [],[]
    handles.append(hand['EMC'])
    handles.append(hand['SMC'])
    handles.append(hand['COMPASS'])
    handles.append(hand['HERMES'])
    handles.append(hand['SLAC'])
    handles.append(hand['RHIC jets'])
    handles.append(hand['EIC p'])
    handles.append(hand['EIC A'])
    #handles.append(hand['cut'])
    labels.append(r'\textbf{\textrm{EMC}}')
    labels.append(r'\textbf{\textrm{SMC}}')
    labels.append(r'\textbf{\textrm{COMPASS}}')
    labels.append(r'\textbf{\textrm{HERMES}}')
    labels.append(r'\textbf{\textrm{SLAC}}')
    labels.append(r'\textbf{\textrm{RHIC jets}}')
    labels.append(r'\textbf{\textrm{EIC (p)}}')
    labels.append(r'\textbf{\textrm{EIC (d,$^3$He)}}')
    #labels.append(r'\boldmath$W^2=10~\rm{GeV}^2$')
    ax.legend(handles,labels,loc='upper left',fontsize=26,frameon=False, handlelength = 1.0, handletextpad = 0.1, ncol=1, columnspacing=0.5)
    #ax.legend(handles,labels,loc=(-0.02,0.30),fontsize=26,frameon=False, handlelength = 1.0, handletextpad = 0.1)

    py.tight_layout()
    filename='%s/gallery/kinematics-pol'%wdir
    filename+='.png'

    py.savefig(filename)
    print 'Saving figure to %s'%filename 





#--plot residuals
def plot_res(wdir,kc,norm=True):

    nrows,ncols=4,1
    fig = py.figure(figsize=(ncols*20,nrows*3))
    ax11=py.subplot(nrows,ncols,1)
    ax21=py.subplot(nrows,ncols,2)
    ax31=py.subplot(nrows,ncols,3)

    load_config('%s/input.py'%wdir)
    istep=core.get_istep()
    predictions = load('%s/data/predictions-%d.dat'%(wdir,istep))

    replicas=core.get_replicas(wdir)
    core.mod_conf(istep,replicas[0]) #--set conf as specified in istep   

    jar=load('%s/data/jar-%d.dat'%(wdir,istep))
    replicas=jar['replicas']

    data = predictions['reactions']
  
    cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc)

    #--get theory by seperating solutions and taking mean
    for exp in data:
        for idx in data[exp]:
            predictions = copy.copy(data[exp][idx]['prediction-rep'])
            for ic in range(nc):
                predictions_ic = [predictions[i] for i in range(len(predictions)) if cluster[i] == ic]
                data[exp][idx]['thy-%d'%ic]  = np.mean(predictions_ic, axis = 0)
                data[exp][idx]['dthy-%d'%ic] = np.std(predictions_ic, axis=0)

    res,std,X,Q2,N = {},{},{},{},{}

    for exp in data:
        N[exp] = 0
        for idx in data[exp]:
            if exp == 'idis':
                if idx==10016:   key  = 'BCDMS'
                elif idx==10017: key  = 'BCDMS'
                elif idx==10020: key  = 'NMC'  
                elif idx==10021: key  = 'NMC' 
                elif idx==10010: key  = 'SLAC' 
                elif idx==10011: key  = 'SLAC'
                elif idx==10026: key  = 'HERA' 
                elif idx==10027: key  = 'HERA'
                elif idx==10028: key  = 'HERA'
                elif idx==10029: key  = 'HERA'
                elif idx==10030: key  = 'HERA'
                elif idx==10031: key  = 'HERA'
                elif idx==10032: key  = 'HERA'
                elif idx==10033: key  = 'JLab BONuS'
                elif idx==10002: key  = 'JLab Hall C'
                elif idx==10003: key  = 'JLab Hall C'
                else: continue
            elif exp == 'dy':    key  = 'FNAL E866'
            elif exp == 'wasym': key  = 'CDF/D0'
            elif exp == 'zrap':  key  = 'CDF/D0'
            elif exp == 'wzrv':
                if idx==2000:    key  = 'CDF/D0' 
                elif idx==2003:  key  = 'CDF/D0' 
                elif idx==2006:  key  = 'CDF/D0'
                else:            key  = 'ATLAS/CMS' 
           
            if key not in res: res[key] = [] 
            if key not in std: std[key] = [] 
            if key not in X:   X[key]   = [] 
            if key not in Q2:  Q2[key]  = [] 
            if key not in N:   N[key]   = 0

            x,q2 = get_kin(exp,data[exp][idx])
            value = data[exp][idx]['value']
            thy   = data[exp][idx]['thy-0']
            dthy  = data[exp][idx]['dthy-0']
            alpha = data[exp][idx]['alpha']
            res[key].extend((value-thy)/alpha)
            std[key].extend(dthy/alpha)
            X[key]  .extend(x)
            Q2[key] .extend(q2)
            N[key] += len(value)

    keys = ['BCDMS','NMC','SLAC','JLab BONuS','JLab Hall C', 'HERA', 'FNAL E866', 'CDF/D0', 'ATLAS/CMS']
    cnt = {}
    Ntot = 4352
    n = 0
    k = 0
    resX  = copy.deepcopy(res) 
    resQ2 = copy.deepcopy(res)
    for key in keys:
        if norm:
            n = Ntot/9.0
            cnt[key] = np.linspace(n*k,n*(k+1),N[key])
            k += 1
        else:
            cnt[key] = np.array([(i + n) for i in range(N[key])])
            n += N[key]

        #--sort from smallest residual to largest
        ares = np.abs(res[key])
        z    = sorted(zip(ares,res[key]))
        res[key] = np.array([z[i][1] for i in range(len(z))])
        z    = sorted(zip(ares,std[key]))
        std[key] = np.array([z[i][1] for i in range(len(z))])

        #--sort using X
        z    = sorted(zip(X[key],resX[key]))
        resX[key] = np.array([z[i][1] for i in range(len(z))])
        X[key]    = sorted(X[key])

        #--sort using Q2
        z    = sorted(zip(Q2[key],resQ2[key]))
        resQ2[key] = np.array([z[i][1] for i in range(len(z))])
        Q2[key]    = sorted(Q2[key])

    hand = {}
    for key in keys:
        if key == 'BCDMS':       color = 'black'
        if key == 'NMC':         color = 'goldenrod'
        if key == 'HERA':        color = 'green'
        if key == 'JLab BONuS':  color = 'orange'
        if key == 'JLab Hall C': color = 'red'
        if key == 'SLAC':        color = 'blue'
        if key == 'FNAL E866':   color = 'magenta'
        if key == 'CDF/D0':      color = 'maroon'
        if key == 'ATLAS/CMS':   color = 'darkcyan'
        #--plot per experiment
        pres = np.array([res[key][i] for i in range(len(res[key])) if res[key][i] >= 0])
        nres = np.array([res[key][i] for i in range(len(res[key])) if res[key][i] <  0])
        pstd = np.array([std[key][i] for i in range(len(res[key])) if res[key][i] >= 0])
        nstd = np.array([std[key][i] for i in range(len(res[key])) if res[key][i] <  0])
        pcnt = np.array([cnt[key][i] for i in range(len(res[key])) if res[key][i] >= 0])
        ncnt = np.array([cnt[key][i] for i in range(len(res[key])) if res[key][i] <  0])
        #hand[key] ,= ax11.plot(cnt[key],res[key],marker='o',ms=2,color=color,linestyle='none')
        hand[key] ,= ax11.plot(pcnt,pres,color=color)
        hand[key] ,= ax11.plot(ncnt,nres,color=color)
        #pup   = pres + pstd
        #pdown = pres - pstd
        #nup   = nres + nstd
        #ndown = nres - nstd
        #ax11.fill_between(pcnt,pdown,pup,color='gold')
        #ax11.fill_between(ncnt,ndown,nup,color='gold')
        if norm:
            vline1 = cnt[key][0] + Ntot/9.0*0.68 
            vline2 = cnt[key][0] + Ntot/9.0*0.95 
        else:
            vline1 = cnt[key][0] + int(np.round(len(cnt[key])*0.68))
            vline2 = cnt[key][0] + int(np.round(len(cnt[key])*0.95))
        ax11.axvline(vline1,0,1,ls='--',color='black', alpha = 0.8)
        ax11.axvline(vline2,0,1,ls=':', color='black', alpha = 0.5)
        #--plot by X
        ax21.plot(cnt[key],resX[key],marker='o',ms=2,color=color,linestyle='none')
        #--plot by Q2
        ax31.plot(cnt[key],resQ2[key],marker='o',ms=2,color=color,linestyle='none')


    #ax.text(4200, 0.2, r'\textbf{\textrm{W/Z}}', size=30,color='white',clip_on = False)

    ax11.set_xlim(-30,Ntot+30)
    ax21.set_xlim(-30,Ntot+30)
    ax31.set_xlim(-30,Ntot+30)

    for ax in [ax11,ax21,ax31]:
        ax.set_ylim(-3,3)
        ax.axhline(0,0,1 ,color='black',ls='-'  ,alpha=1.0)
        ax.axhline(1,0,1 ,color='black',ls='--' ,alpha=0.8)
        ax.axhline(-1,0,1,color='black',ls='--' ,alpha=0.8)
        ax.axhline(2,0,1 ,color='black',ls=':'  ,alpha=0.5)
        ax.axhline(-2,0,1,color='black',ls=':'  ,alpha=0.5)
        ax.set_yticks([-2,-1,0,1,2])
        ax.set_yticklabels([r'$-2$',r'$-1$',r'$0$',r'$1$',r'$2$'])

    ax11.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=30,labelbottom=False)
    ax21.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=30,labelbottom=False)
    ax31.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=30,labelbottom=False)

    ax11.set_xlabel(r'\textbf{\textrm{Ordered by size}}', size=30)
    ax21.set_xlabel(r'\textbf{\textrm{Ordered by}}' + ' ' + r'\boldmath$x$', size=30)
    ax31.set_xlabel(r'\textbf{\textrm{Ordered by}}' + ' ' + r'\boldmath$Q^2$', size=30)

    #ax21.set_ylabel(r'\textbf{\textrm{residuals}}', size=30)
    fig.suptitle(r'\textbf{\textrm{Residuals}}', size=30)

    #ax11.text(0.00, 0.00, r'\textbf{\textrm{point}}' ,size=30 ,clip_on=False)
    #ax21.text(0.00, 0.00, r'\boldmath$x$'            ,size=30 ,clip_on=False)
    #ax31.text(0.00, 0.00, r'\boldmath$Q^2$'          ,size=30 ,clip_on=False)

    handles = [hand['BCDMS'],hand['NMC'],hand['SLAC'],hand['JLab BONuS'],hand['JLab Hall C'],hand['HERA'],hand['FNAL E866'],hand['CDF/D0'],hand['ATLAS/CMS']]
    label1  = r'\textbf{\textrm{BCDMS}}'
    label2  = r'\textbf{\textrm{NMC}}'
    label3  = r'\textbf{\textrm{SLAC}}'
    label4  = r'\textbf{\textrm{JLab BONuS}}'
    label5  = r'\textbf{\textrm{JLab Hall C}}'
    label6  = r'\textbf{\textrm{HERA}}'
    label7  = r'\textbf{\textrm{FNAL E866}}'
    label8  = r'\textbf{\textrm{CDF/D0}}'
    label9  = r'\textbf{\textrm{ATLAS/CMS}}'
    lables = [label1,label2,label3,label4,label5,label6,label7,label8,label9]
    ax31.legend(handles,lables,loc=(0,-0.8),fontsize=30,frameon=False, handlelength = 1.0, handletextpad = 0.1,ncol = 5,columnspacing=0.9,markerscale=3.0)
    py.tight_layout()
    py.subplots_adjust(hspace=0.2,top=0.95)
    filename='%s/gallery/data-res'%wdir
    filename+='.png'

    py.savefig(filename)
    print 'Saving figure to %s'%filename



