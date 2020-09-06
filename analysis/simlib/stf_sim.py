import os,sys
import pandas as pd
import numpy as np
from subprocess import Popen, PIPE
from scipy.integrate import quad

#--matplotlib
import matplotlib
matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
#matplotlib.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
matplotlib.rc('text',usetex=True)
import pylab  as py
from matplotlib.lines import Line2D

import lhapdf

#--from analysis
from analysis.corelib import core, predict

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

def stf(wdir,tar='p',force=True):

    #--get unpolarized structure functions and appropriate indices
    stf =['F2g','FLg']
    idxs=[900,901]

    #--gamma/Z channel
    stf.extend(['F2gZ','FLgZ','F3gZ'])
    idxs.extend([902,903,904])
    
    #--Z channel
    stf.extend(['F2Z','FLZ','F3Z'])
    idxs.extend([905,906,907])
    
    #--all channels
    stf.extend(['F2','FL','F3'])
    idxs.extend([908,909,910])
    
    #--charged current only for proton 
    if tar=='p':  
        #--W-
        stf.extend(['W2-','WL-','W3-'])
        idxs.extend([930,931,932])
        
        #--W+
        stf.extend(['W2+','WL+','W3+'])
        idxs.extend([940,941,942])

    #--generate data files
    for i in range(len(stf)): 
        gen_stf_xlsx(wdir,idxs[i],tar,stf[i])

    #--modify conf with new data files
    conf = gen_conf(wdir,idxs,tar)

    #--get predictions on new data files if not already done
    print('Generating predictions...')
    name = 'stfs-%s'%tar
    predict.get_predictions(wdir,force=force,mod_conf=conf,name=name)

    #--update tables
    update_tabs(wdir,idxs,tar)

    #--generate lhapdf info and data files
    gen_lhapdf_info_file(wdir,idxs,tar)
    gen_lhapdf_dat_file(wdir,idxs,tar)

def gen_stf_xlsx(wdir,idx,tar,obs):
    checkdir('%s/sim'%wdir)

    #-- the kinem. var.
    data={_:[] for _ in ['col','target','X','Q2','obs','value']}

    #--get specific points from data file
    X,Q2=get_xQ2_grid()

    for x in X:
        for q2 in Q2:
            data['col'].append('JAM4EIC')
            data['X'].append(x)
            data['Q2'].append(q2)
            data['target'].append(tar)
            data['obs'].append(obs)
            data['value'].append(0.0)

    df=pd.DataFrame(data)
    filename = '%s/sim/stf-%s-%s.xlsx'%(wdir,tar,idx)
    df.to_excel(filename, index=False)
    print('Generating xlsx file and saving to %s'%filename)

def get_xQ2_grid():

    Q2=[1.30000E+00,1.50159E+00,1.75516E+00,2.07810E+00\
            ,2.49495E+00,3.04086E+00,3.76715E+00,4.50000E+00\
            ,4.75000E+00,6.23113E+00,8.37423E+00,1.15549E+01\
            ,1.64076E+01,2.40380E+01,3.64361E+01,5.73145E+01\
            ,9.38707E+01,1.60654E+02,2.88438E+02,5.45587E+02\
            ,1.09231E+03,2.32646E+03,5.30043E+03,1.29956E+04\
            ,3.45140E+04,1.00000E+05]

    X=[1.00000E-06,1.28121E-06,1.64152E-06,2.10317E-06\
           ,2.69463E-06,3.45242E-06,4.42329E-06,5.66715E-06\
           ,7.26076E-06,9.30241E-06,1.19180E-05,1.52689E-05\
           ,1.95617E-05,2.50609E-05,3.21053E-05,4.11287E-05\
           ,5.26863E-05,6.74889E-05,8.64459E-05,1.10720E-04\
           ,1.41800E-04,1.81585E-04,2.32503E-04,2.97652E-04\
           ,3.80981E-04,4.87518E-04,6.26039E-04,8.00452E-04\
           ,1.02297E-03,1.30657E-03,1.66759E-03,2.12729E-03\
           ,2.71054E-03,3.44865E-03,4.37927E-03,5.54908E-03\
           ,7.01192E-03,8.83064E-03,1.10763E-02,1.38266E-02\
           ,1.71641E-02,2.11717E-02,2.59364E-02,3.15062E-02\
           ,3.79623E-02,4.53425E-02,5.36750E-02,6.29705E-02\
           ,7.32221E-02,8.44039E-02,9.64793E-02,1.09332E-01\
           ,1.23067E-01,1.37507E-01,1.52639E-01,1.68416E-01\
           ,1.84794E-01,2.01731E-01,2.19016E-01,2.36948E-01\
           ,2.55242E-01,2.73927E-01,2.92954E-01,3.12340E-01\
           ,3.32036E-01,3.52019E-01,3.72282E-01,3.92772E-01\
           ,4.13533E-01,4.34326E-01,4.55495E-01,4.76836E-01\
           ,4.98342E-01,5.20006E-01,5.41818E-01,5.63773E-01\
           ,5.85861E-01,6.08077E-01,6.30459E-01,6.52800E-01\
           ,6.75387E-01,6.98063E-01,7.20830E-01,7.43683E-01\
           ,7.66623E-01,7.89636E-01,8.12791E-01,8.35940E-01\
           ,8.59175E-01,8.82485E-01,9.05866E-01,9.29311E-01\
           ,9.52817E-01,9.76387E-01,1.00000E+00]

    return X,Q2

def gen_conf(wdir,idxs,tar):

    print('Modifying config with new data files...')

    load_config('%s/input.py'%wdir)
    istep=core.get_istep()
    conf['steps'][istep]['datasets'] = {}
    conf['steps'][istep]['datasets']['idis']=[]
    conf['datasets']['idis']['filters']=[]

    for idx in idxs:
        conf['datasets']['idis']['xlsx'][idx]='./%s/sim/stf-%s-%s.xlsx'%(wdir,tar,idx)
        conf['steps'][istep]['datasets']['idis'].append(idx)

    #--get sample data file for X, Q2 values 
    fn   = ['./%s/sim/stf-%s-%s.xlsx'%(wdir,tar,idxs[0])]

    conf['idis grid'] = {}
    conf['idis grid']['overwrite'] = True
    conf['idis grid']['xlsx']  = fn
    
    return conf

def update_tabs(wdir,idxs,tar):

    istep=core.get_istep()
    data=load('%s/data/predictions-%s-stfs-%s.dat'%(wdir,istep,tar))

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

    tabs = data['reactions']['idis']

    #--delete unnecessary data
    for idx in tabs:
        tab=data['reactions']['idis'][idx]
        for k in blist:
            try: del tab[k]
            except: continue

        #--save mean value
        tab['value']=np.mean(tab['prediction-rep'],axis=0)
  
        #--save individual replicas
        for i in range(len(tab['prediction-rep'])):
            tab['value%s'%(i+1)] = tab['prediction-rep'][i]

        del tab['prediction-rep']

        df=pd.DataFrame(tab)
        filename = '%s/sim/stf-%s-%s.xlsx'%(wdir,tar,idx)
        df.to_excel(filename, index=False)
        print('Updating xlsx file and saving to %s'%filename)

def gen_lhapdf_info_file(wdir,idxs,tar):

    dirname = 'JAMSTF-%s'%tar
    info = {}
    info['<description>'] = 'Unpolarized STF simulation for EIC'
    info['<index>'] = '0'
    info['<authors>'] = 'JAM Collaboration'
    info['<reference>'] = ''
    info['<particle>'] = '%s'%tar

    #--get tables
    X,Q2,table,replicas=get_tables(wdir,idxs,tar)

    #--get flav string
    flavs=''
    for idx in idxs: flavs+='%d, '%idx
    flavs=flavs.rstrip(',')

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
    lines.append('Flavors:         [%s]'%flavs)
    lines.append('OrderQCD:        1')
    lines.append('FlavorScheme:    <flav scheme>')
    lines.append('NumFlavors:      %d'%len(idxs))
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
    checkdir('%s/lhapdf/%s'%(wdir,dirname))
    tab=open('%s/lhapdf/%s/%s.info'%(wdir,dirname,dirname),'w')
    tab.writelines(lines)
    tab.close()
    print('Saving lhapdf info file to %s/lhapdf/%s/%s.info'%(wdir,dirname,dirname))

def gen_lhapdf_dat_file(wdir,idxs,tar):

    dirname = 'JAMSTF-%s'%tar
    #--get tables
    X,Q2,central,replicas=get_tables(wdir,idxs,tar)
    nx=len(X)
    nQ2=len(Q2)
    nrep = len(replicas[idxs[0]])

    L = nx*nQ2
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
    for idx in idxs: flavs+='%d '%idx
    lines.append(flavs)

    for i in range(L):
        line=''
        for iflav in idxs:
            line+=('%10.5e '%central[iflav][i]).upper()
        lines.append(line)
    lines.append('---')
    lines=[l+'\n' for l in lines]
    if central: idx=str(0).zfill(4)
    else:       idx=str(0).zfill(4)
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
        for idx in idxs: flavs+='%d '%idx
        lines.append(flavs)

        for i in range(L):
            line=''
            for iflav in idxs:
                line+=('%10.5e '%replicas[iflav][j][i]).upper()
            lines.append(line)
        lines.append('---')
        lines=[l+'\n' for l in lines]
        l = len(str(j+1))
        idx=str(0).zfill(4-l)+str((j+1))

        checkdir('%s/lhapdf/%s'%(wdir,dirname))
        tab=open('%s/lhapdf/%s/%s_%s.dat'%(wdir,dirname,dirname,idx),'w')
        tab.writelines(lines)
        tab.close()

    print('Saving lhapdf data files inside %s/lhapdf/%s'%(wdir,dirname))

def get_tables(wdir,idxs,tar):
    central = {}
    replicas= {}
    for idx in idxs:
        replicas[idx] = []
        tab=pd.read_excel('%s/sim/stf-%s-%s.xlsx'%(wdir,tar,idx))
        tab=tab.to_dict(orient='list')
        central[idx]=tab['value']
        _replicas = {}
        for key in tab:
            if key[:5] != 'value': continue
            if key     == 'value': continue
            _replicas[key] = tab[key]
        for i in range(len(_replicas)):
            replicas[idx].append(_replicas['value%s'%(i+1)])

    X,Q2=get_xQ2_grid()

    return X,Q2,central,replicas












