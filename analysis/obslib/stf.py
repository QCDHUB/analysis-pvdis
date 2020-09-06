import sys,os
import numpy as np

#--matplotlib
import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import cm
import pylab as py
import lhapdf

#--from scipy stack 
from scipy.integrate import quad

#--from tools
from tools.tools     import load,save,checkdir,lprint
from tools.config    import conf,load_config

#--from fitlib
from fitlib.resman import RESMAN

#--from local
from analysis.corelib import core
from analysis.corelib import classifier


#--unpolarized NC

def gen_stf(wdir,Q2,TAR=['p','n','d'],STF=['F2','FL','F3']):
   
    _STF = {}
    for tar in TAR:
        _STF[tar] = []
        for stf in STF:
            _STF[tar].append(stf)

    print('\ngenerating STF from %s'%(wdir))
    load_config('%s/input.py'%wdir)
    istep=core.get_istep()
    replicas=core.get_replicas(wdir)
    core.mod_conf(istep,replicas[0]) #--set conf as specified in istep   

    if 'pdf' not in conf['steps'][istep]['active distributions']:
        if 'pdf' not in conf['steps'][istep]['passive distributions']:
                print('pdf is not an active or passive distribution')
                return 

    conf['idis grid'] = 'prediction'
    conf['datasets']['idis'] = {_:{} for _ in ['xlsx','norm']}
    resman=RESMAN(nworkers=1,parallel=False,datasets=False)
    parman=resman.parman
    resman.setup_idis()
    idis  = resman.idis_thy
    idis.data['p'] = {}
    idis.data['n'] = {}
    idis.data['d'] = {}
    for tar in TAR:
        for stf in _STF[tar]:
            idis.data[tar][stf] = np.zeros(idis.X.size)

    parman.order=replicas[0]['order'][istep]

    jar=load('%s/data/jar-%d.dat'%(wdir,istep))
    replicas=jar['replicas']

    pdf=conf['pdf']
    #--setup kinematics
    X=10**np.linspace(-4,-1,100)
    X=np.append(X,np.linspace(0.1,0.99,100))


    #--compute X*STF for all replicas        
    XF={}
    cnt=0
    for par in replicas:
        cnt+=1
        lprint('%d/%d'%(cnt,len(replicas)))

        parman.set_new_params(par,initial=True)
        pdf.evolve(Q2)
        idis._update()

        for tar in TAR:
            if tar not in XF: XF[tar] = {}
            for stf in _STF[tar]:
                if stf not in XF[tar]:  XF[tar][stf]=[]
                xf = X*idis.get_stf(X,Q2,stf=stf,tar=tar)
                XF[tar][stf].append(xf)

    print     
    checkdir('%s/data'%wdir)
    if Q2==1.27**2: filename='%s/data/stf-%d.dat'%(wdir,istep)
    else:filename='%s/data/stf-%d-Q2=%d.dat'%(wdir,istep,int(Q2))

    save({'X':X,'Q2':Q2,'XF':XF},filename)
    print 'Saving data to %s'%filename

def plot_stf(wdir,Q2,kc,mode=0,name=''):
  #--mode 0: plot each replica
  #--mode 1: plot average and standard deviation of replicas 

  nrows,ncols=1,3
  fig = py.figure(figsize=(ncols*7,nrows*4))
  ax11=py.subplot(nrows,ncols,1)
  ax12=py.subplot(nrows,ncols,2)
  ax13=py.subplot(nrows,ncols,3)

  filename = '%s/gallery/stfs'%wdir
  if mode==1: filename += '-bands'

  filename += name

  load_config('%s/input.py'%wdir)
  istep=core.get_istep()

  #--load data if it exists
  try:
      if Q2==1.27**2: data=load('%s/data/stf-%d.dat'%(wdir,istep))
      else: data=load('%s/data/stf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
  #--generate data and then load it if it does not exist
  except:
      gen_stf(wdir,Q2)
      if Q2==1.27**2: data=load('%s/data/stf-%d.dat'%(wdir,istep))
      else: data=load('%s/data/stf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
      
  cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc) 
  best_cluster=cluster_order[0]

  X  = data['X']

  for tar in data['XF']:
      for stf in data['XF'][tar]:
          mean = np.mean(data['XF'][tar][stf],axis=0)
          std = np.std(data['XF'][tar][stf],axis=0)

          if tar=='p': color='red'
          if tar=='n': color='green'
          if tar=='d': color='blue'

          label = None
          if stf =='F2': ax,label = ax11,r'\boldmath$xF_2^{(%s)}$'%tar
          if stf =='FL': ax,label = ax12,r'\boldmath$xF_L^{(%s)}$'%tar
          if stf =='F3': ax,label = ax13,r'\boldmath$xF_3^{(%s)}$'%tar

          ax.plot([],[],label=label,color=color)

          #--plot each replica
          if mode==0:
              for i in range(len(data['XF'][tar][stf])):
                  ax.plot(X,data['XF'][tar][stf][i],color=color,alpha=0.1)
    
          #--plot average and standard deviation
          if mode==1:
              ax.plot(X,mean,color=color)
              ax.fill_between(X,mean-std,mean+std,color=color,alpha=0.5)


  for ax in [ax11,ax12,ax13]:
        ax.set_xlim(1e-4,1)
        ax.semilogx()
          
        ax.tick_params(axis='both', which='both', top=True, right=True, direction='in',labelsize=20)
        ax.set_xticks([0.0001,0.001,0.01,0.1,1])
        ax.set_xticklabels([r'$10^{-4}$',r'$10^{-3}$',r'$10^{-2}$',r'$10^{-1}$',r'$1$'])

  ax11.legend(loc='upper left',fontsize=20,frameon=False)
  ax12.legend(loc='upper left',fontsize=20,frameon=False)
  ax13.legend(loc='upper left',fontsize=20,frameon=False)

  ax11.set_ylim(0,0.1)      #,ax11.set_yticks([0,0.2,0.4,0.6,0.8])
  ax12.set_ylim(0,0.004)    #,ax12.set_yticks([0,0.2,0.4,0.6,0.8,1.0])
  ax13.set_ylim(0,0.0004)   #,ax13.set_yticks([0,0.2,0.4,0.6])

  ax11.set_ylabel(r'$xF$',size=35)
  ax11.set_xlabel(r'$x$' ,size=35)
  ax12.set_xlabel(r'$x$' ,size=35)   
  ax13.set_xlabel(r'$x$' ,size=35)   

  if Q2 == 1.27**2: ax11.text(0.40,0.85,r'\boldmath{$Q^2 = m_c^2$}',       transform=ax11.transAxes,size=30)
  else:             ax11.text(0.40,0.85,r'\boldmath{$Q^2 = %s~GeV^2$}'%Q2, transform=ax11.transAxes,size=25)

  py.tight_layout()

  filename+='.png'

  checkdir('%s/gallery'%wdir)
  py.savefig(filename)
  print 'Saving figure to %s'%filename

def plot_rat(PLOT,kc,mode=0,name='',nrep=None):

  #--plot F2D/F2N ratio and F2n/F2p ratio
  #--mode 0: plot each replica
  #--mode 1: plot average and standard deviation of replicas 

  nrows,ncols=1,2
  fig = py.figure(figsize=(ncols*6,nrows*4))
  ax11=py.subplot(nrows,ncols,1)
  ax12=py.subplot(nrows,ncols,2)

  wdir = PLOT[0][0]
  filename = '%s/gallery/stf_rat'%wdir
  if mode==1: filename += '-bands'

  filename += name
      
  replicas=core.get_replicas(wdir)



  for plot in PLOT:

      wdir,Q2,color,style,label,alpha = plot[0],plot[1],plot[2],plot[3],plot[4],plot[5]
      load_config('%s/input.py'%wdir)
      istep=core.get_istep()

      #--load data if it exists
      try:
          if Q2==1.27**2: data=load('%s/data/stf-%d.dat'%(wdir,istep))
          else: data=load('%s/data/stf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
      #--generate data and then load it if it does not exist
      except:
          gen_stf(wdir,Q2)
          if Q2==1.27**2: data=load('%s/data/stf-%d.dat'%(wdir,istep))
          else: data=load('%s/data/stf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))

      cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc) 
      best_cluster=cluster_order[0]

      X  = data['X']

      F2d = np.array(data['XF']['d']['F2'])
      F2p = np.array(data['XF']['p']['F2'])
      F2n = np.array(data['XF']['n']['F2'])

      ratDN = 2*F2d/(F2p+F2n)
      ratnp = F2n/F2p

      meanDN = np.mean(ratDN,axis=0)
      stdDN  =  np.std(ratDN,axis=0)
      meannp = np.mean(ratnp,axis=0)
      stdnp  =  np.std(ratnp,axis=0)

      #--plot each replica
      if mode==0:
          for i in range(len(ratDN)):
              if nrep != None and i >= nrep: break
              ax11.plot(X,ratDN[i],color=color,alpha=0.1)
              ax12.plot(X,ratnp[i],color=color,alpha=0.1)
      
      #--plot average and standard deviation
      if mode==1:
          ax11.plot(X,meanDN,style,label=label,color=color)
          ax11.fill_between(X,meanDN-stdDN,meanDN+stdDN,color=color,alpha=0.5)
          ax12.plot(X,meannp,style,label=label,color=color)
          ax12.fill_between(X,meannp-stdnp,meannp+stdnp,color=color,alpha=0.5)


  for ax in [ax11,ax12]:
        ax.set_xlim(0,1)
          
        ax.tick_params(axis='both', which='both', top=True, right=True, direction='in',labelsize=20)
        ax.set_xticks([0,0.2,0.4,0.6,0.8,1])

  ax11.legend(loc='upper left',fontsize=20,frameon=False)

  ax11.axhline(1,0,1,ls='--',color='black',alpha=0.5)

  ax11.set_ylim(0.97,1.08) ,ax11.set_yticks([0.98,1,1.02,1.04,1.06,1.08])
  ax12.set_ylim(0.00,1.00) ,ax12.set_yticks([0,0.2,0.4,0.6,0.8,1])

  ax11.set_ylabel(r'$F_2^D/F_2^N$',size=30)
  ax12.set_ylabel(r'$F_2^n/F_2^p$',size=30)
  ax11.set_xlabel(r'$x$'          ,size=30)
  ax12.set_xlabel(r'$x$'          ,size=30)

  if Q2 == 1.27**2: ax11.text(0.1,0.8,r'\boldmath{$Q^2 = m_c^2$}',       transform=ax11.transAxes,size=30)
  else:             ax11.text(0.1,0.8,r'\boldmath{$Q^2 = %s~GeV^2$}'%Q2, transform=ax11.transAxes,size=25)

  py.tight_layout()

  filename+='.png'

  checkdir('%s/gallery'%wdir)
  py.savefig(filename)
  print 'Saving figure to %s'%filename



#--unpolarized CC

def gen_CCstf(wdir,Q2,TAR=['p'],STF=['W2+','WL+','W3+','W2-','WL-','W3-']):
   
    _STF = {}
    for tar in TAR:
        _STF[tar] = []
        for stf in STF:
            _STF[tar].append(stf)

    print('\ngenerating CC STF from %s'%(wdir))
    load_config('%s/input.py'%wdir)
    istep=core.get_istep()
    replicas=core.get_replicas(wdir)
    core.mod_conf(istep,replicas[0]) #--set conf as specified in istep   

    if 'pdf' not in conf['steps'][istep]['active distributions']:
        if 'pdf' not in conf['steps'][istep]['passive distributions']:
                print('pdf is not an active or passive distribution')
                return 

    conf['idis grid'] = 'prediction'
    conf['datasets']['idis'] = {_:{} for _ in ['xlsx','norm']}
    resman=RESMAN(nworkers=1,parallel=False,datasets=False)
    parman=resman.parman
    resman.setup_idis()
    idis  = resman.idis_thy

    idis.data['p'] = {}
    idis.data['n'] = {}
    idis.data['d'] = {}
    for tar in TAR:
        for stf in _STF[tar]:
            idis.data[tar][stf] = np.zeros(idis.X.size)

    parman.order=replicas[0]['order'][istep]

    jar=load('%s/data/jar-%d.dat'%(wdir,istep))
    replicas=jar['replicas']

    pdf=conf['pdf']
    #--setup kinematics
    X=10**np.linspace(-4,-1,100)
    X=np.append(X,np.linspace(0.1,0.99,100))


    #--compute X*STF for all replicas        
    XF={}
    cnt=0
    for par in replicas:
        cnt+=1
        lprint('%d/%d'%(cnt,len(replicas)))

        parman.set_new_params(par,initial=True)
        pdf.evolve(Q2)
        idis._update()

        for tar in TAR:
            if tar not in XF: XF[tar] = {}
            for stf in _STF[tar]:
                if stf not in XF[tar]:  XF[tar][stf]=[]
                xf = X*idis.get_stf(X,Q2,stf=stf,tar=tar)
                XF[tar][stf].append(xf)

    print     
    checkdir('%s/data'%wdir)
    if Q2==1.27**2: filename='%s/data/CCstf-%d.dat'%(wdir,istep)
    else:filename='%s/data/CCstf-%d-Q2=%d.dat'%(wdir,istep,int(Q2))

    save({'X':X,'Q2':Q2,'XF':XF},filename)
    print 'Saving data to %s'%filename

def plot_CCstf(wdir,Q2,kc,mode=0,name=''):
  #--mode 0: plot each replica
  #--mode 1: plot average and standard deviation of replicas 

  nrows,ncols=1,3
  fig = py.figure(figsize=(ncols*7,nrows*4))
  ax11=py.subplot(nrows,ncols,1)
  ax12=py.subplot(nrows,ncols,2)
  ax13=py.subplot(nrows,ncols,3)

  filename = '%s/gallery/CCstfs'%wdir
  if mode==1: filename += '-bands'

  filename += name

  load_config('%s/input.py'%wdir)
  istep=core.get_istep()

  #--load data if it exists
  try:
      if Q2==1.27**2: data=load('%s/data/CCstf-%d.dat'%(wdir,istep))
      else: data=load('%s/data/CCstf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
  #--generate data and then load it if it does not exist
  except:
      gen_stf(wdir,Q2)
      if Q2==1.27**2: data=load('%s/data/CCstf-%d.dat'%(wdir,istep))
      else: data=load('%s/data/stf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
      
  cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc) 
  best_cluster=cluster_order[0]

  X  = data['X']

  for tar in data['XF']:
      for stf in data['XF'][tar]:
          mean = np.mean(data['XF'][tar][stf],axis=0)
          std = np.std(data['XF'][tar][stf],axis=0)

          if stf[-1]=='+': color='red'
          if stf[-1]=='-': color='blue'

          label = None
          if stf =='W2+': ax,label = ax11,r'\boldmath$xW_2^{+(%s)}$'%tar
          if stf =='WL+': ax,label = ax12,r'\boldmath$xW_L^{+(%s)}$'%tar
          if stf =='W3+': ax,label = ax13,r'\boldmath$xW_3^{+(%s)}$'%tar
          if stf =='W2-': ax,label = ax11,r'\boldmath$xW_2^{-(%s)}$'%tar
          if stf =='WL-': ax,label = ax12,r'\boldmath$xW_L^{-(%s)}$'%tar
          if stf =='W3-': ax,label = ax13,r'\boldmath$xW_3^{-(%s)}$'%tar

          ax.plot([],[],label=label,color=color)

          #--plot each replica
          if mode==0:
              for i in range(len(data['XF'][tar][stf])):
                  ax.plot(X,data['XF'][tar][stf][i],color=color,alpha=0.1)
    
          #--plot average and standard deviation
          if mode==1:
              ax.plot(X,mean,color=color)
              ax.fill_between(X,mean-std,mean+std,color=color,alpha=0.5)


  for ax in [ax11,ax12,ax13]:
        ax.set_xlim(1e-4,1)
        ax.semilogx()
          
        ax.tick_params(axis='both', which='both', top=True, right=True, direction='in',labelsize=20)
        ax.set_xticks([0.0001,0.001,0.01,0.1,1])
        ax.set_xticklabels([r'$10^{-4}$',r'$10^{-3}$',r'$10^{-2}$',r'$10^{-1}$',r'$1$'])


  ax13.axhline(0,0,1,ls='--',color='black',alpha=0.5)

  ax11.legend(loc='upper left',fontsize=20,frameon=False)
  ax12.legend(loc='upper left',fontsize=20,frameon=False)
  ax13.legend(loc='upper left',fontsize=20,frameon=False)

  ax11.set_ylim(0,0.4)      #,ax11.set_yticks([0,0.2,0.4,0.6,0.8])
  ax12.set_ylim(0,0.015)    #,ax12.set_yticks([0,0.2,0.4,0.6,0.8,1.0])
  ax13.set_ylim(-1.0,2.0)   #,ax13.set_yticks([0,0.2,0.4,0.6])

  ax11.set_ylabel(r'$xF$',size=35)
  ax11.set_xlabel(r'$x$' ,size=35)
  ax12.set_xlabel(r'$x$' ,size=35)   
  ax13.set_xlabel(r'$x$' ,size=35)   

  if Q2 == 1.27**2: ax11.text(0.40,0.85,r'\boldmath{$Q^2 = m_c^2$}',       transform=ax11.transAxes,size=30)
  else:             ax11.text(0.40,0.85,r'\boldmath{$Q^2 = %s~GeV^2$}'%Q2, transform=ax11.transAxes,size=25)

  py.tight_layout()

  filename+='.png'

  checkdir('%s/gallery'%wdir)
  py.savefig(filename)
  print 'Saving figure to %s'%filename



#--polarized

def gen_pstf(wdir,Q2,TAR=['p','n','d','h'],STF=['g1','g2']):
   
    _STF = {}
    for tar in TAR:
        _STF[tar] = []
        for stf in STF:
            _STF[tar].append(stf)

    print('\ngenerating PSTF from %s'%(wdir))
    load_config('%s/input.py'%wdir)
    istep=core.get_istep()
    replicas=core.get_replicas(wdir)
    core.mod_conf(istep,replicas[0]) #--set conf as specified in istep   

    if 'ppdf' not in conf['steps'][istep]['active distributions']:
        if 'ppdf' not in conf['steps'][istep]['passive distributions']:
                print('ppdf is not an active or passive distribution')
                return 

    conf['pidis grid'] = 'prediction'
    conf['datasets']['idis']  = {_:{} for _ in ['xlsx','norm']}
    conf['datasets']['pidis'] = {_:{} for _ in ['xlsx','norm']}
    resman=RESMAN(nworkers=1,parallel=False,datasets=False)
    parman=resman.parman
    resman.setup_idis()
    conf['idis'] = resman.idis_thy
    resman.setup_pidis()
    pidis = resman.pidis_thy
    pidis.data['p'] = {}
    pidis.data['n'] = {}
    pidis.data['d'] = {}
    pidis.data['h'] = {}
    for tar in TAR:
        for stf in _STF[tar]:
            pidis.data[tar][stf] = np.zeros(pidis.X.size)

    parman.order=replicas[0]['order'][istep]

    jar=load('%s/data/jar-%d.dat'%(wdir,istep))
    replicas=jar['replicas']

    ppdf=conf['ppdf']
    #--setup kinematics
    X=10**np.linspace(-4,-1,100)
    X=np.append(X,np.linspace(0.1,0.99,100))


    #--compute X*STF for all replicas        
    XF={}
    cnt=0
    for par in replicas:
        cnt+=1
        lprint('%d/%d'%(cnt,len(replicas)))

        parman.set_new_params(par,initial=True)
        ppdf.evolve(Q2)
        pidis._update()

        for tar in TAR:
            if tar not in XF: XF[tar] = {}
            for stf in _STF[tar]:
                if stf not in XF[tar]:  XF[tar][stf]=[]
                xf = X*pidis.get_stf(X,Q2,stf=stf,tar=tar)
                XF[tar][stf].append(xf)

    print     
    checkdir('%s/data'%wdir)
    if Q2==1.27**2: filename='%s/data/pstf-%d.dat'%(wdir,istep)
    else:filename='%s/data/pstf-%d-Q2=%d.dat'%(wdir,istep,int(Q2))

    save({'X':X,'Q2':Q2,'XF':XF},filename)
    print 'Saving data to %s'%filename

def plot_pstf(wdir,Q2,kc,mode=0,name=''):
  #--mode 0: plot each replica
  #--mode 1: plot average and standard deviation of replicas 

  nrows,ncols=1,2
  fig = py.figure(figsize=(ncols*7,nrows*4))
  ax11=py.subplot(nrows,ncols,1)
  ax12=py.subplot(nrows,ncols,2)

  filename = '%s/gallery/pstfs'%wdir
  if mode==1: filename += '-bands'

  filename += name

  load_config('%s/input.py'%wdir)
  istep=core.get_istep()

  #--load data if it exists
  try:
      if Q2==1.27**2: data=load('%s/data/pstf-%d.dat'%(wdir,istep))
      else: data=load('%s/data/pstf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
  #--generate data and then load it if it does not exist
  except:
      gen_stf(wdir,Q2)
      if Q2==1.27**2: data=load('%s/data/pstf-%d.dat'%(wdir,istep))
      else: data=load('%s/data/pstf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
      
  cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc) 
  best_cluster=cluster_order[0]

  X  = data['X']

  for tar in data['XF']:
      for stf in data['XF'][tar]:
          mean = np.mean(data['XF'][tar][stf],axis=0)
          std = np.std(data['XF'][tar][stf],axis=0)

          if tar=='p': color='red'
          if tar=='n': color='green'
          if tar=='d': color='blue'
          if tar=='h': color='magenta'

          label = None
          if stf =='g1': ax,label = ax11,r'\boldmath$xg_1^{(%s)}$'%tar
          if stf =='g2': ax,label = ax12,r'\boldmath$xg_2^{(%s)}$'%tar

          ax.plot([],[],label=label,color=color)

          #--plot each replica
          if mode==0:
              for i in range(len(data['XF'][tar][stf])):
                  ax.plot(X,data['XF'][tar][stf][i],color=color,alpha=0.1)
    
          #--plot average and standard deviation
          if mode==1:
              ax.plot(X,mean,style,label=label,color=color)
              ax.fill_between(X,mean-std,mean+std,color=color,alpha=0.5)


  for ax in [ax11,ax12]:
        ax.set_xlim(1e-4,1)
        ax.semilogx()
          
        ax.tick_params(axis='both', which='both', top=True, right=True, direction='in',labelsize=20)
        ax.set_xticks([0.0001,0.001,0.01,0.1,1])
        ax.set_xticklabels([r'$10^{-4}$',r'$10^{-3}$',r'$10^{-2}$',r'$10^{-1}$',r'$1$'])
        ax.axhline(0,0,1,ls='--',color='black',alpha=0.5)

  ax11.legend(loc='upper left',fontsize=15,frameon=False)
  ax12.legend(loc='lower left',fontsize=15,frameon=False)

  ax11.set_ylim(-0.03,0.075)      #,ax11.set_yticks([0,0.2,0.4,0.6,0.8])
  ax12.set_ylim(-0.05,0.03)      #,ax12.set_yticks([0,0.2,0.4,0.6,0.8,1.0])

  ax11.set_ylabel(r'$xF$',size=35)
  ax11.set_xlabel(r'$x$' ,size=35)
  ax12.set_xlabel(r'$x$' ,size=35)   

  if Q2 == 1.27**2: ax11.text(0.40,0.85,r'\boldmath{$Q^2 = m_c^2$}',       transform=ax11.transAxes,size=30)
  else:             ax11.text(0.40,0.85,r'\boldmath{$Q^2 = %s~GeV^2$}'%Q2, transform=ax11.transAxes,size=25)

  py.tight_layout()

  filename+='.png'

  checkdir('%s/gallery'%wdir)
  py.savefig(filename)
  print 'Saving figure to %s'%filename


