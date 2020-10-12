import sys, os, time
import numpy as np
import copy
from subprocess import Popen, PIPE, STDOUT

import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['text.latex.preview']=True
import pylab as py

from scipy.integrate import quad
from scipy.integrate import cumtrapz

## from fitpack tools
from tools.tools     import load, save, checkdir, lprint
from tools.config    import conf, load_config

## from fitpack fitlib
from fitlib.resman import RESMAN

## from fitpack analysis
from analysis.corelib import core
from analysis.corelib import classifier


flavors = []
flavors.append('up')
flavors.append('dp')
flavors.append('sp')
flavors.append('g')

def gen_xf(wdir,Q2 = 1.27**2):
    load_config('%s/input.py' % wdir)
    istep = core.get_istep()

    replicas = core.get_replicas(wdir)
    names    = core.get_replicas_names(wdir)
    ## 'conf' will be modified for each replica individually later in the loop over 'replicas'
    ## the reason for doing this is that 'fix parameters' has to be set correctly for each replica

    if 'ppdf' not in conf['steps'][istep]['active distributions']:
        print('ppdf-proton not in active distribution')
        return

    resman = RESMAN(nworkers = 1, parallel = False, datasets = False)
    parman = resman.parman
    parman.order = replicas[0]['order'][istep]

    ppdf = conf['ppdf']

    ## setup kinematics
    X = 10.0 ** np.linspace(-6, -1, 100)
    X = np.append(X, np.linspace(0.1, 0.99, 100))
    if Q2 == None: Q2 = conf['Q20']
    print('\ngenerating polarized pdf-proton from %s at Q2 = %f' % (wdir, Q2))

    ## compute XF for all replicas
    XF = {}
    n_replicas = len(replicas)
    for i in range(n_replicas):
        lprint('%d/%d' % (i + 1, n_replicas))

        core.mod_conf(istep, replicas[i])
        parman.set_new_params(replicas[i]['params'][istep], initial = True)

        for flavor in flavors:
            if flavor not in XF: XF[flavor] = []
            if flavor == 'up':
                func = lambda x: ppdf.get_xF(x, Q2, 'u') + ppdf.get_xF(x, Q2, 'ub')
            elif flavor == 'dp':
                func = lambda x: ppdf.get_xF(x, Q2, 'd') + ppdf.get_xF(x, Q2, 'db')
            elif flavor == 'sp':
                func = lambda x: ppdf.get_xF(x, Q2, 's') + ppdf.get_xF(x, Q2, 'sb')
            else:
                func = lambda x: ppdf.get_xF(x, Q2, flavor)

            XF[flavor].append([func(x) for x in X])

            #if flavor=='g':
            #    if func(1e-3) > 0.3: print names[i]
            #    if func(1e-3) < -0.2: print names[i]


    print
    checkdir('%s/data' % wdir)
    if Q2 == conf['Q20']:
        save({'X': X, 'Q2': Q2, 'XF': XF}, '%s/data/ppdf-%d.dat' % (wdir, istep))
    else:
        save({'X': X, 'Q2': Q2, 'XF': XF}, '%s/data/ppdf-%d-Q2=%d.dat' % (wdir, istep, int(Q2)))
        
def plot_xf_main(PLOT,kc,mode=0,name='',PSETS=[],cmap=False):
  #--mode 0: plot each replica
  #--mode 1: plot average and standard deviation of replicas 

  #--get PPDF sets for comparison
  #for SET in PSETS:
  #    if SET=='CJ15':   CJ15   = QPDCALC('CJ15nlo',ismc=False) 
  #    if SET=='JAM19':  JAM19  = QPDCALC('JAM19PDF_proton_nlo',ismc=True)
  #    if SET=='ABMP16': ABMP16 = QPDCALC('ABMP16_3_nlo',ismc=False)
  #    if SET=='CSKK':   CSKK   = QPDCALC('CSKK_nnlo_EIG',ismc=False)
  #    if SET=='NNPDF':  NNPDF  = QPDCALC('NNPDF31_nlo_as_0118',ismc=False)
  #    if SET=='MMHT':   MMHT   = QPDCALC('MMHT2014nlo68cl',ismc=False)

  nrows,ncols=2,2
  fig = py.figure(figsize=(ncols*6,nrows*4))
  ax11=py.subplot(nrows,ncols,1)
  ax12=py.subplot(nrows,ncols,2)
  ax21=py.subplot(nrows,ncols,3)
  ax22=py.subplot(nrows,ncols,4)

  filename = '%s/gallery/ppdfs'%PLOT[0][0]

  filename += name

  j = 0
  for plot in PLOT:

      wdir, Q2, color, style, label = plot[0], plot[1], plot[2], plot[3], plot[4]
      load_config('%s/input.py'%wdir)
      istep=core.get_istep()

      if Q2==1.27**2: data=load('%s/data/ppdf-%d.dat'%(wdir,istep))
      else: data=load('%s/data/ppdf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))

      replicas=core.get_replicas(wdir)
      #--colormap of chi2
      if cmap: colors = classifier.get_cmap(wdir,'cool',len(replicas))
      else:
          cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc) 
          best_cluster=cluster_order[0]

      X=data['X']

      for flav in data['XF']:
          mean = np.mean(data['XF'][flav],axis=0)
          std = np.std(data['XF'][flav],axis=0)

          if flav=='up': ax = ax11
          if flav=='dp': ax = ax12
          if flav=='sp': ax = ax21
          if flav=='g' : ax = ax22

          #--plot each replica
          if mode==0:
              for i in range(len(data['XF'][flav])):
                  #--if plotting one step, use clusters
                  if cmap: color = colors[i]
                  else:
                      if len(PLOT) == 1: color = colors[cluster[i]]
                  ax.plot(X,data['XF'][flav][i],color=color,alpha=0.5)
        
          #--plot average and standard deviation
          if mode==1:
              ax.plot(X,mean,style,label=label,color=color)
              ax.fill_between(X,mean-std,mean+std,color=color,alpha=0.2)

          #--plot other PPDF sets
          #if j==0:
          #    for SET in SETS:
          #        _set,_label = None,None
          #        if SET=='CJ15':  
          #            _set,_color,alpha=CJ15,'gray', 0.3
          #            if flav=='uv': _label = 'CJ15'
          #        if SET=='JAM19': 
          #            _set,_color,alpha=JAM19,'magenta',0.5
          #            if flav=='uv': _label = 'JAM19'
          #        if SET=='ABMP16': 
          #            _set,_color,alpha=ABMP16,'blue',0.5
          #            if flav=='d/u': _label = 'ABMP16'
          #        if SET=='CSKK':
          #            _set,_color,alpha=CSKK,'green',0.3
          #            if flav=='d/u': _label = 'CSKK'
          #        if SET=='NNPDF':
          #            _set,_color,alpha=NNPDF,'yellow',0.5
          #            if flav=='g': _label = 'NNPDF3.1'
          #        if SET=='MMHT':
          #            _set,_color,alpha=MMHT,'pink',0.5
          #            if flav=='g': _label = 'MMHT14'
          #        pdf = _set.get_xpdf(flav,X,Q2)
          #        ax.fill_between(X,pdf['xfmin'], pdf['xfmax'],label=_label,color=_color,alpha=alpha)

          #    if flav=='uv':  ax.legend(loc='upper left' ,fontsize=20,frameon=False)
          #    if flav=='d/u': ax.legend(loc='upper right',fontsize=20,frameon=False)
          #    if flav=='g':   ax.legend(loc='upper right',fontsize=20,frameon=False)

      j+=1


  for ax in [ax11,ax12,ax21,ax22]:
        ax.set_xlim(1e-4,1)
        ax.semilogx()
          
        ax.tick_params(axis='both', which='both', top=True, right=True, direction='in',labelsize=20)
        #ax.set_xticks([0.01,0.1,0.5,0.8])
        #ax.set_xticklabels([r'$0.01$',r'$0.1$',r'$0.5$',r'$0.8$'])

  ax11.set_ylim(0.0,0.5)   ,ax11.set_yticks([0,0.1,0.2,0.3,0.4,0.5])
  ax12.set_ylim(-0.2,0.0)  ,ax12.set_yticks([0,-0.05,-0.10,-0.15,-0.20])
  ax21.set_ylim(-0.10,0.05),ax21.set_yticks([-0.08,-0.04,0.00,0.04])
  ax22.set_ylim(-0.2,0.4)  ,ax22.set_yticks([-0.2,0,0.2,0.4])

  ax21.axhline(0,color='k',linestyle=':')
  ax22.axhline(0,color='k',linestyle=':')

  #ax11.set_ylabel(r'$xf(x)$',size=25)
  #ax21.set_ylabel(r'$xf(x)$',size=25)
  ax21.set_xlabel(r'$x$',size=25)
  ax22.set_xlabel(r'$x$',size=25)   

  ax11.text(0.3,0.5,r'\boldmath{$x \Delta u^+$}', transform=ax11.transAxes,size=25)

  if Q2 == 1.27**2: ax22.text(0.05,0.05,r'$Q^2 = m_c^2$',              transform=ax22.transAxes,size=30)
  else:             ax22.text(0.05,0.05,r'$Q^2 = %s ~ \rm{GeV^2}$'%Q2, transform=ax22.transAxes,size=30)

  ax12.text(0.2,0.3,r'\boldmath{$x \Delta d^+$}', transform=ax12.transAxes,size=25)

  ax21.text(0.1,0.1,r'\boldmath{$x \Delta s^+$}', transform=ax21.transAxes,size=25)

  ax22.text(0.1,0.85,r'\boldmath{$x \Delta g$}',  transform=ax22.transAxes,size=25)

 
  py.tight_layout()

  filename+='.png'

  checkdir('%s/gallery'%wdir)
  py.savefig(filename)
  print 'Saving figure to %s'%filename

def plot_xf_strange(PLOT,kc,mode=0,name=''):
  #--mode 0: plot each replica
  #--mode 1: plot average and standard deviation of replicas 

  nrows,ncols=1,1
  fig = py.figure(figsize=(ncols*6,nrows*4))
  ax11=py.subplot(nrows,ncols,1)

  filename = '%s/gallery/ppdfs-strange'%PLOT[0][0]

  filename += name

  j = 0
  for plot in PLOT:

      wdir, Q2, color, style, label = plot[0], plot[1], plot[2], plot[3], plot[4]
      load_config('%s/input.py'%wdir)
      istep=core.get_istep()

      if Q2==1.27**2: data=load('%s/data/ppdf-%d.dat'%(wdir,istep))
      else: data=load('%s/data/ppdf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))

      replicas=core.get_replicas(wdir)
      cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc) 
      best_cluster=cluster_order[0]

      X=data['X']

      for flav in data['XF']:
          mean = np.mean(data['XF'][flav],axis=0)
          std = np.std(data['XF'][flav],axis=0)

          if flav=='sp': ax = ax11
          else: continue

          #--plot each replica
          if mode==0:
              for i in range(len(data['XF'][flav])):
                  #--if plotting one step, use clusters
                  if len(PLOT) == 1: color = colors[cluster[i]]
                  ax.plot(X,data['XF'][flav][i],color=color,alpha=0.5)
        
          #--plot average and standard deviation
          if mode==1:
              ax.plot(X,mean,style,label=label,color=color)
              ax.fill_between(X,mean-std,mean+std,color=color,alpha=0.2)

      j+=1


  for ax in [ax11]:
        ax.set_xlim(1e-4,1)
        ax.semilogx()
          
        ax.tick_params(axis='both', which='both', top=True, right=True, direction='in',labelsize=20)
        #ax.set_xticks([0.01,0.1,0.5,0.8])
        #ax.set_xticklabels([r'$0.01$',r'$0.1$',r'$0.5$',r'$0.8$'])

  ax11.set_ylim(-0.10,0.05),ax11.set_yticks([-0.08,-0.04,0.00,0.04])

  ax11.axhline(0,color='k',linestyle=':')

  ax11.set_ylabel(r'$xf(x)$',size=30)
  ax11.set_xlabel(r'$x$',size=30)

  ax11.text(0.05,0.05,r'\boldmath{$x \Delta s^+$}', transform=ax11.transAxes,size=25)

 
  py.tight_layout()

  filename+='.png'

  checkdir('%s/gallery'%wdir)
  py.savefig(filename)
  print 'Saving figure to %s'%filename

def plot_xf_std_ratio(PLOT,kc,name=''):
  #--mode 0: plot each replica
  #--mode 1: plot average and standard deviation of replicas 

  nrows,ncols=1,1
  fig = py.figure(figsize=(ncols*7,nrows*4))
  ax11=py.subplot(nrows,ncols,1)

  filename = '%s/gallery/ppdfs-std-ratio'%PLOT[0][0]

  filename += name

  #--first PLOT entry is no EIC
  #--further PLOT entries are EIC

  j = 0

  #--get denominator
  wdir, Q2, color, style, label, alpha = PLOT[0][0], PLOT[0][1], PLOT[0][2], PLOT[0][3], PLOT[0][4], PLOT[0][5]
  load_config('%s/input.py'%wdir)
  istep=core.get_istep()
  #--load data if it exists
  try:
      if Q2==1.27**2: data=load('%s/data/ppdf-%d.dat'%(wdir,istep))
      else: data=load('%s/data/ppdf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
  #--generate data and then load it if it does not exist
  except:
      gen_xf(wdir,Q2)
      if Q2==1.27**2: data=load('%s/data/ppdf-%d.dat'%(wdir,istep))
      else: data=load('%s/data/ppdf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
      
  replicas=core.get_replicas(wdir)
  cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc) 
  best_cluster=cluster_order[0]

  X=data['X']

  denom = {}
  for flav in data['XF']:
      denom[flav] = np.std(data['XF'][flav],axis=0)

  for plot in PLOT:
      j+=1
      if j == 1: continue

      wdir, Q2, color, style, label, alpha = plot[0], plot[1], plot[2], plot[3], plot[4], plot[5]
      load_config('%s/input.py'%wdir)
      istep=core.get_istep()

      #--load data if it exists
      try:
          if Q2==1.27**2: data=load('%s/data/ppdf-%d.dat'%(wdir,istep))
          else: data=load('%s/data/ppdf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
      #--generate data and then load it if it does not exist
      except:
          gen_xf(wdir,Q2)
          if Q2==1.27**2: data=load('%s/data/ppdf-%d.dat'%(wdir,istep))
          else: data=load('%s/data/ppdf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
          
      replicas=core.get_replicas(wdir)
      cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc) 
      best_cluster=cluster_order[0]

      X=data['X']
      X1 = data['X'][:100]
      X2 = data['X'][100:]

      for flav in ['up','dp','sp','g']:
          std = np.std(data['XF'][flav],axis=0)

          if   flav=='up': color,label = 'red'        ,r'\boldmath$\Delta u^+$' 
          elif flav=='dp': color,label = 'blue'       ,r'\boldmath$\Delta d^+$' 
          elif flav=='sp': color,label = 'green'      ,r'\boldmath$\Delta s^+$' 
          elif flav=='g':  color,label = 'orange'     ,r'\boldmath$\Delta g$' 
          else: continue

          #--plot std over denom
          ax11.plot(X,std/denom[flav],style,color=color,label=label,lw=5)

  for ax in [ax11]:
        ax.set_xlim(1e-4,0.5)
        ax.semilogx()
          
        ax.tick_params(axis='both', which='major', top=True, right=True, direction='in',labelsize=25,length=5  ,width=1.5)
        ax.tick_params(axis='both', which='minor', top=True, right=True, direction='in',labelsize=25,length=2.5,width=1.5)
        ax.set_ylim(0,1.2) ,ax.set_yticks([0.2,0.4,0.6,0.8,1.0])

  ax11.axhline(1.0,alpha=0.5,ls='--',color='black')
  ax11.set_xlabel(r'\boldmath$x$'    ,size=30)
  ax11.text(0.55,0.25,r'\boldmath$\sigma^{\rm{EIC}}/\sigma$',transform=ax11.transAxes,size=40)

  if Q2 == 1.27**2: ax11.text(0.55,0.05,r'$Q^2 = m_c^2$',              transform=ax11.transAxes,size=30)
  else:             ax11.text(0.55,0.05,r'$Q^2 = %s ~ \rm{GeV^2}$'%Q2, transform=ax11.transAxes,size=30)

  ax11.xaxis.set_label_coords(1.0,0.0)

  ax11.legend(loc='lower left', fontsize = 18, frameon = 0, handletextpad = 0.3, handlelength = 1.0 ,ncol=2, columnspacing = 1.0)
  py.tight_layout()

  filename+='.png'

  checkdir('%s/gallery'%wdir)
  py.savefig(filename)
  print 'Saving figure to %s'%filename

def plot_xf(PLOT,kc,kind=0,mode=0,name='',PSETS=[],cmap=False):

    if kind == 0:
        plot_xf_main(PLOT,kc,mode,name,PSETS,cmap)
        plot_xf_strange(PLOT,kc,mode,name)
    if kind == 1:
        plot_xf_std_ratio(PLOT,kc,name)

moments = []
moments.append('Sigma')
moments.append('G') 
        
def gen_moments(wdir,Q2 = 1.27**2):
    load_config('%s/input.py' % wdir)
    istep = core.get_istep()

    replicas = core.get_replicas(wdir)
    ## 'conf' will be modified for each replica individually later in the loop over 'replicas'
    ## the reason for doing this is that 'fix parameters' has to be set correctly for each replica

    if 'ppdf' not in conf['steps'][istep]['active distributions']:
        print('ppdf-proton not in active distribution')
        return

    resman = RESMAN(nworkers = 1, parallel = False, datasets = False)
    parman = resman.parman
    parman.order = replicas[0]['order'][istep]

    ppdf = conf['ppdf']

    ## setup kinematics
    X = 10.0 ** np.linspace(-6, -1, 100)
    X = np.append(X, np.linspace(0.1, 0.99, 100))
    if Q2 == None: Q2 = conf['Q20']
    print('\ngenerating polarized pdf-proton from %s at Q2 = %f' % (wdir, Q2))

    ## compute XF for all replicas
    MOM = {}
    n_replicas = len(replicas)
    for i in range(n_replicas):
        lprint('%d/%d' % (i + 1, n_replicas))

        core.mod_conf(istep, replicas[i])
        parman.set_new_params(replicas[i]['params'][istep], initial = True)

        for moment in moments:
            if moment not in MOM: MOM[moment] = []
            if moment == 'Sigma':
                func = lambda x: ppdf.get_xF(x, Q2, 'u')/x + ppdf.get_xF(x, Q2, 'ub')/x\
                               + ppdf.get_xF(x, Q2, 'd')/x + ppdf.get_xF(x, Q2, 'db')/x\
                               + ppdf.get_xF(x, Q2, 's')/x + ppdf.get_xF(x, Q2, 'sb')/x 
            elif moment == 'G':
                func = lambda x: ppdf.get_xF(x, Q2, 'g')/x

            #--Gaussian quadrature
            npts = 99
            z,w = np.polynomial.legendre.leggauss(npts) 
            jac    = lambda x: 0.5*(1 - x)
            xeval  = lambda x: 0.5*((1 - x)*z + x + 1)
            moms   = np.zeros(len(X))
            for j in range(len(X)):
                x = X[j]
                _func   = np.array([func(xeval(x)[i]) for i in range(len(z))])
                moms[j] = np.sum(w*jac(x)*_func)

            MOM[moment].append(moms)
  
            #--scipy.cumtrapz
            #_func = [func(x) for x in X]
            #mom = np.array(cumtrapz(_func,X,initial=0.0))
            #mom_max = mom[-1]
            #moms = mom_max - mom
            #exact = np.array([quad(func,x,1.0)[0] for x in X])
            #percent = np.abs((moms-exact)/exact)*100


            #--scipy.quad
            #MOM[moment].append([quad(func,x,1.0)[0] for x in X])


    print
    checkdir('%s/data' % wdir)
    if Q2 == conf['Q20']:
        save({'X': X, 'Q2': Q2, 'MOM': MOM}, '%s/data/ppdf-moments-%d.dat' % (wdir, istep))
    else:
        save({'X': X, 'Q2': Q2, 'MOM': MOM}, '%s/data/ppdf-moments-%d-Q2=%d.dat' % (wdir, istep, int(Q2)))
        
def plot_moments(PLOT,kc,mode=0,name=''):
  #--mode 0: plot each replica
  #--mode 1: plot average and standard deviation of replicas 

  nrows,ncols=4,1
  fig = py.figure(figsize=(ncols*7,nrows*1.5))
  ax11=py.subplot(nrows,ncols,(1,3))
  ax21=py.subplot(nrows,ncols,4)

  filename = '%s/gallery/ppdf-moments'%PLOT[0][0]

  filename += name

  j = 0
  thy_plot = {}
  thy_band = {}
  for plot in PLOT:

      wdir, Q2, color, style, label = plot[0], plot[1], plot[2], plot[3], plot[4]
      load_config('%s/input.py'%wdir)
      istep=core.get_istep()

      if Q2==1.27**2: data=load('%s/data/ppdf-moments-%d.dat'%(wdir,istep))
      else: data=load('%s/data/ppdf-moments-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))

      replicas=core.get_replicas(wdir)

      X=data['X']
      for mom in ['G','Sigma']:
          mean = np.mean(data['MOM'][mom],axis=0)
          std = np.std(data['MOM'][mom],axis=0)

          if j == 0:
              if mom=='Sigma': color,alpha = 'orange',0.3
              if mom=='G':     color,alpha = 'cyan'  ,0.3
          if j == 1:
              if mom=='Sigma': color,alpha = 'red'   ,1.0
              if mom=='G':     color,alpha = 'blue'  ,1.0
          ax = ax11 

          #--plot each replica
          if mode==0:
              for i in range(len(data['MOM'][mom])):
                  ax.plot(X,data['MOM'][mom][i],color=color,alpha=0.5)
        
          #--plot average and standard deviation
          if mode==1:
              thy_band[(j,mom)]  = ax.fill_between(X,mean-std,mean+std,color=color,alpha=alpha)

      j+=1


  for ax in [ax11]:
        ax.set_xlim(1e-4,1)
        ax.semilogx()
          
        ax.tick_params(axis='both', which='both', top=True, right=True, labelbottom=False, direction='in',labelsize=25)
        ax.set_xticks([1e-4,1e-3,1e-2,1e-1])
        #ax.set_xticklabels([r'$0.01$',r'$0.1$',r'$0.5$',r'$0.8$'])

  ax11.set_ylim(0.0,0.65)   ,ax11.set_yticks([0.1,0.2,0.3,0.4,0.5,0.6])

  if Q2 == 1.27**2: ax11.text(0.55,0.85,r'$Q^2 = m_c^2$',              transform=ax11.transAxes,size=30)
  else:             ax11.text(0.55,0.85,r'$Q^2 = %s ~ \rm{GeV^2}$'%Q2, transform=ax11.transAxes,size=30)

  handles = []
  handles.append(thy_band[(0,'Sigma')])
  handles.append(thy_band[(0,'G')])
  handles.append(thy_band[(1,'Sigma')])
  handles.append(thy_band[(1,'G')])

  labels = []
  labels.append(r'\boldmath$\Delta \Sigma$')
  labels.append(r'\boldmath$\Delta G$')
  #labels.append(r'\boldmath$\Delta \Sigma~\rm{(EIC~A_{PV}^p)}$')
  #labels.append(r'\boldmath$\Delta G~\rm{(EIC~A_{PV}^p)}$')
  labels.append(r'\boldmath$\Delta \Sigma~\rm{(EIC)}$')
  labels.append(r'\boldmath$\Delta G~\rm{(EIC)}$')
  ax11.legend(handles,labels,loc='lower left', fontsize = 18, frameon = 0, handletextpad = 0.3, handlelength = 1.0, ncol = 2, columnspacing = 1.0)


  #--plot ratio of EIC/no EIC standard deviations
  #--get denominator
  wdir, Q2, color, style, label, alpha = PLOT[0][0], PLOT[0][1], PLOT[0][2], PLOT[0][3], PLOT[0][4], PLOT[0][5]
  load_config('%s/input.py'%wdir)
  istep=core.get_istep()
  if Q2==1.27**2: data=load('%s/data/ppdf-moments-%d.dat'%(wdir,istep))
  else: data=load('%s/data/ppdf-moments-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
      
  replicas=core.get_replicas(wdir)
  cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc) 
  best_cluster=cluster_order[0]

  X=data['X']

  denom = {}
  for mom in data['MOM']:
      denom[mom] = np.std(data['MOM'][mom],axis=0)

  j = 0
  hand = {}
  for plot in PLOT:
      j+=1
      if j == 1: continue

      wdir, Q2, color, style, label, alpha = plot[0], plot[1], plot[2], plot[3], plot[4], plot[5]
      load_config('%s/input.py'%wdir)
      istep=core.get_istep()

      if Q2==1.27**2: data=load('%s/data/ppdf-moments-%d.dat'%(wdir,istep))
      else: data=load('%s/data/ppdf-moments-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
          
      replicas=core.get_replicas(wdir)
      cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc) 
      best_cluster=cluster_order[0]

      X=data['X']

      for mom in ['G','Sigma']:
          std = np.std(data['MOM'][mom],axis=0)

          if mom=='Sigma': color = 'red' 
          if mom=='G':     color = 'blue'
          ax = ax21 

          hand[mom] ,= ax.plot(X,std/denom[mom],color=color,lw=5)

  for ax in [ax21]:
        ax.set_xlim(1e-4,1)
        ax.semilogx()
          
        ax.tick_params(axis='both', which='both', top=True, right=True, direction='in',labelsize=25)
        ax.set_xticks([1e-4,1e-3,1e-2,1e-1])
        #ax.set_xticklabels([r'$0.01$',r'$0.1$',r'$0.5$',r'$0.8$'])
 
  ax21.set_xlabel(r'\boldmath$x_{\rm{min}}$'    ,size=30)
  ax21.xaxis.set_label_coords(0.95,0.0)

  ax21.set_ylim(0,1.0)
  ax21.set_yticks([0.2,0.4,0.6,0.8])
  #ax21.set_yticklabels([r'$0.2$',r'$0.4$',r'$0.6$',r'$0.8$'])

  ax21.text(0.55,0.15,r'\boldmath$\sigma^{\rm{EIC}}/\sigma$', transform=ax21.transAxes,size=40)

  handles = []
  handles.append(hand['Sigma'])
  handles.append(hand['G'])

  labels = []
  labels.append(r'\boldmath$\Delta \Sigma$')
  labels.append(r'\boldmath$\Delta G$')

  ax21.legend(handles,labels,loc='lower left', fontsize = 18, frameon = 0, handletextpad = 0.3, handlelength = 1.0, ncol = 2, columnspacing = 1.0)

  py.tight_layout()
  py.subplots_adjust(hspace=0)

  filename+='.png'

  checkdir('%s/gallery'%wdir)
  py.savefig(filename)
  print 'Saving figure to %s'%filename
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
