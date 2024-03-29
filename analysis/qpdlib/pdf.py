import sys,os
import numpy as np

#--matplotlib
import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import cm
matplotlib.rcParams['text.latex.preview']=True
import pylab as py

#--from scipy stack 
from scipy.integrate import quad

#--from tools
from tools.tools     import load,save,checkdir,lprint
from tools.config    import conf,load_config

#--from fitlib
from fitlib.resman import RESMAN

#--from local
from qpdcalc import QPDCALC
from analysis.corelib import core
from analysis.corelib import classifier

FLAV=[]
FLAV.append('g')
FLAV.append('uv')
FLAV.append('dv')
FLAV.append('d/u')
FLAV.append('db')
FLAV.append('ub')
FLAV.append('db+ub')
FLAV.append('db-ub')
FLAV.append('s')
FLAV.append('sb')
FLAV.append('s+sb')
FLAV.append('s-sb')
FLAV.append('Rs')

def gen_xf(wdir,Q2):
    
    print('\ngenerating pdf at Q2 = %s from %s'%(Q2,wdir))
    load_config('%s/input.py'%wdir)
    istep=core.get_istep()
    replicas=core.get_replicas(wdir)
    core.mod_conf(istep,replicas[0]) #--set conf as specified in istep   

    if 'pdf' not in conf['steps'][istep]['active distributions']:
        if 'pdf' not in conf['steps'][istep]['passive distributions']:
                print('pdf is not an active or passive distribution')
                return 

    resman=RESMAN(nworkers=1,parallel=False,datasets=False)
    parman=resman.parman
    parman.order=replicas[0]['order'][istep]

    jar=load('%s/data/jar-%d.dat'%(wdir,istep))
    replicas=jar['replicas']

    pdf=conf['pdf']
    #--setup kinematics
    X=10**np.linspace(-6,-1,100)
    X=np.append(X,np.linspace(0.1,0.99,100))

    pdf.evolve(Q2)

    #--compute XF for all replicas        
    XF={}
    cnt=0
    for par in replicas:
        cnt+=1
        lprint('%d/%d'%(cnt,len(replicas)))

        parman.set_new_params(par,initial=True)

        for flav in FLAV:
            if flav not in XF:  XF[flav]=[]
            if flav=='uv':
                 func=lambda x: pdf.get_xF(x,Q2,'uv')
            elif flav=='dv':
                 func=lambda x: pdf.get_xF(x,Q2,'dv')
            elif flav=='d/u':
                 func=lambda x: pdf.get_xF(x,Q2,'d')/pdf.get_xF(x,Q2,'u')
            elif flav=='db+ub':
                 func=lambda x: pdf.get_xF(x,Q2,'db') + pdf.get_xF(x,Q2,'ub')
            elif flav=='db-ub':
                 func=lambda x: pdf.get_xF(x,Q2,'db') - pdf.get_xF(x,Q2,'ub')
            elif flav=='s+sb':
                 func=lambda x: pdf.get_xF(x,Q2,'s') + pdf.get_xF(x,Q2,'sb')
            elif flav=='s-sb':
                 func=lambda x: pdf.get_xF(x,Q2,'s') - pdf.get_xF(x,Q2,'sb')
            elif flav=='Rs':
                 func=lambda x: (pdf.get_xF(x,Q2,'s') + pdf.get_xF(x,Q2,'sb'))\
                                /(pdf.get_xF(x,Q2,'db') + pdf.get_xF(x,Q2,'ub'))
            else:
                 func=lambda x: pdf.get_xF(x,Q2,flav) 

            XF[flav].append(np.array([func(x) for x in X]))

    print     
    checkdir('%s/data'%wdir)
    if Q2==1.27**2: filename='%s/data/pdf-%d.dat'%(wdir,istep)
    else:filename='%s/data/pdf-%d-Q2=%d.dat'%(wdir,istep,int(Q2))

    save({'X':X,'Q2':Q2,'XF':XF},filename)
    print 'Saving data to %s'%filename

def plot_xf_main(PLOT,kc,mode=0,name='',SETS=[],nrep=None):
  #--mode 0: plot each replica
  #--mode 1: plot average and standard deviation of replicas 

  nrows,ncols=3,2
  fig = py.figure(figsize=(ncols*7,nrows*4))
  ax11=py.subplot(nrows,ncols,1)
  ax12=py.subplot(nrows,ncols,2)
  ax21=py.subplot(nrows,ncols,3)
  ax22=py.subplot(nrows,ncols,4)
  ax31=py.subplot(nrows,ncols,5)
  ax32=py.subplot(nrows,ncols,6)

  #--get PDF sets for comparison
  for SET in SETS:
      if SET=='CJ15':   CJ15   = QPDCALC('CJ15nlo',ismc=False) 
      if SET=='JAM19':  JAM19  = QPDCALC('JAM19PDF_proton_nlo',ismc=True,central_only=False)
      if SET=='ABMP16': ABMP16 = QPDCALC('ABMP16_3_nlo',ismc=False)
      if SET=='CSKK':   CSKK   = QPDCALC('CSKK_nnlo_EIG',ismc=False)
      if SET=='NNPDF':  NNPDF  = QPDCALC('NNPDF31_nlo_as_0118',ismc=True,central_only=False)
      if SET=='MMHT':   MMHT   = QPDCALC('MMHT2014nlo68cl',ismc=False)

  if len(SETS) > 0: ax11.plot([],[],label=r'\textrm{JAM20}',color='red')

  filename = '%s/gallery/pdfs'%PLOT[0][0]
  if mode==1: filename += '-bands'

  filename += name

  j = 0
  for plot in PLOT:

      wdir, Q2, color, style, label, alpha = plot[0], plot[1], plot[2], plot[3], plot[4], plot[5]
      load_config('%s/input.py'%wdir)
      istep=core.get_istep()

      #--load data if it exists
      try:
          if Q2==1.27**2: data=load('%s/data/pdf-%d.dat'%(wdir,istep))
          else: data=load('%s/data/pdf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
      #--generate data and then load it if it does not exist
      except:
          gen_xf(wdir,Q2)
          if Q2==1.27**2: data=load('%s/data/pdf-%d.dat'%(wdir,istep))
          else: data=load('%s/data/pdf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
          
      replicas=core.get_replicas(wdir)
      cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc) 
      best_cluster=cluster_order[0]

      X=data['X']
      X1 = data['X'][:100]
      X2 = data['X'][100:]


      ax11.plot([],[],label=label,color=color)
      for flav in data['XF']:
          mean = np.mean(data['XF'][flav],axis=0)
          std = np.std(data['XF'][flav],axis=0)

          if flav=='uv' or flav=='dv': ax = ax11
          elif flav=='d/u':            ax = ax12
          elif flav=='db+ub':          ax = ax21
          elif flav=='db-ub':          ax = ax22
          elif flav=='g':              ax = ax31
          elif flav=='s+sb':           ax = ax32
          else: continue

          #--plot each replica
          if mode==0:
              for i in range(len(data['XF'][flav])):
                  #--stop at nrep replicas
                  if nrep != None and i > nrep: break

                  #--if plotting one step, use clusters
                  if len(PLOT) == 1: color = colors[cluster[i]]

                  if flav=='g': data['XF'][flav][i] /= 10.0

                  ax.plot(X,data['XF'][flav][i],color=color,alpha=alpha)
        
          #--plot average and standard deviation
          if mode==1:
              if flav=='g':
                  mean /= 10.0
                  std  /= 10.0

              ax.plot(X,mean,style,label=label,color=color)
              ax.fill_between(X,mean-std,mean+std,color=color,alpha=0.5)

          #--plot other PDF sets
          if j==0:
              for SET in SETS:
                  _set,_label = None,None
                  if SET=='CJ15':  
                      _set,_color,_alpha=CJ15,'gray', 0.3
                      if flav=='uv': _label = r'\textrm{CJ15}'
                  if SET=='JAM19': 
                      _set,_color,_alpha=JAM19,'magenta',0.5
                      if flav=='d/u': _label = r'\textrm{JAM19}'
                  if SET=='ABMP16': 
                      _set,_color,_alpha=ABMP16,'blue',0.5
                      if flav=='d/u': _label = r'\textrm{ABMP16}'
                  if SET=='CSKK':
                      _set,_color,_alpha=CSKK,'green',0.3
                      if flav=='g': _label = r'\textrm{CSKK}'
                  if SET=='NNPDF':
                      _set,_color,_alpha=NNPDF,'yellow',0.5
                      if flav=='uv': _label = r'\textrm{NNPDF3.1}'
                  if SET=='MMHT':
                      _set,_color,_alpha=MMHT,'pink',0.5
                      if flav=='g': _label = r'\textrm{MMHT14}'
                  pdf = _set.get_xpdf(flav,X,Q2)

                  if flav=='g':
                      pdf['xfmin'] /= 10.0
                      pdf['xfmax'] /= 10.0

                  ax.fill_between(X,pdf['xfmin'],pdf['xfmax'],label=_label,color=_color,alpha=_alpha)

              if flav=='uv':  ax.legend(loc='upper left' ,fontsize=20,frameon=False)
              if flav=='d/u': ax.legend(loc='upper right',fontsize=20,frameon=False)
              if flav=='g':   ax.legend(loc='upper right',fontsize=20,frameon=False)

      j+=1


  if len(PLOT) > 1: ax11.legend(loc='upper left',fontsize=25,frameon=False)

  for ax in [ax11,ax21,ax22,ax31,ax32]:
        ax.set_xlim(1e-4,1)
        ax.semilogx()
          
        ax.tick_params(axis='both', which='major', top=True, right=True, direction='in',labelsize=25,length=5  ,width=1.5)
        ax.tick_params(axis='both', which='minor', top=True, right=True, direction='in',labelsize=25,length=2.5,width=1.5)
        #ax.set_xticks([0.01,0.1,1])
        #ax.set_xticklabels([r'$0.01$',r'$0.1$',r'$1$'])

  for ax in [ax12]:
      ax.tick_params(axis='both', which='major', top=True, right=True, direction='in',labelsize=25,length=5  ,width=1.5)
      ax.tick_params(axis='both', which='minor', top=True, right=True, direction='in',labelsize=25,length=2.5,width=1.5)
      ax.set_xticks([0,0.2,0.4,0.6,0.8])
      ax.set_xticklabels([r'$0$',r'$0.2$',r'$0.4$',r'$0.6$',r'$0.8$'])

  ax12.set_xlim(0,0.9)

  ax11.set_ylim(0,0.8)     ,ax11.set_yticks([0,0.2,0.4,0.6,0.8])
  ax12.set_ylim(0,1.0)     ,ax12.set_yticks([0,0.2,0.4,0.6,0.8,1.0])
  ax21.set_ylim(-0.05,1.8) #,ax21.set_yticks([0,0.2,0.4,0.6])
  ax22.set_ylim(-0.06,0.08),ax22.set_yticks([-0.04,0,0.04,0.08])
  ax31.set_ylim(0,1.2)     #,ax31.set_yticks([0,0.2,0.4,0.6])
  ax32.set_ylim(0,1.5)     #,ax32.set_yticks([0,0.2,0.4,0.6,0.8])

  ax31.set_xlabel(r'\boldmath$x$'    ,size=30)
  ax32.set_xlabel(r'\boldmath$x$'    ,size=30)   

  ax11.text(0.87,0.70 ,r'\boldmath{$xu_{v}$}', transform=ax11.transAxes,size=25)
  ax11.text(0.75,0.20 ,r'\boldmath{$xd_{v}$}', transform=ax11.transAxes,size=25)
  ax12.text(0.2,0.3,r'\boldmath{$d/u$}', transform=ax12.transAxes,size=25)
  ax21.text(0.7,0.8,r'\boldmath{$x(\bar{d}+\bar{u})$}', transform=ax21.transAxes,size=25)
  ax22.text(0.1,0.85,r'\boldmath{$x(\bar{d}-\bar{u})$}', transform=ax22.transAxes,size=25)
  ax31.text(0.6,0.5,r'\boldmath{$xg/10$}', transform=ax31.transAxes,size=25)
  ax32.text(0.7,0.8,r'\boldmath{$x(s+\bar{s})$}', transform=ax32.transAxes,size=25)

  ax21.axhline(0,ls='--',color='black',alpha=0.5)
  ax22.axhline(0,ls='--',color='black',alpha=0.5)
 
  if Q2 == 1.27**2: ax12.text(0.25,0.75,r'$Q^2 = m_c^2$',              transform=ax12.transAxes,size=30)
  else:             ax12.text(0.15,0.75,r'$Q^2 = %s ~ \rm{GeV^2}$'%Q2, transform=ax12.transAxes,size=30)

  py.tight_layout()

  filename+='.png'

  checkdir('%s/gallery'%wdir)
  py.savefig(filename)
  print 'Saving figure to %s'%filename

def plot_xf_strange(PLOT,kc,mode=0,name='',SETS=[],nrep=None):
  #--mode 0: plot each replica
  #--mode 1: plot average and standard deviation of replicas 

  nrows,ncols=1,1
  fig = py.figure(figsize=(ncols*7,nrows*4))
  ax11=py.subplot(nrows,ncols,1)

  filename = '%s/gallery/pdfs-strange'%PLOT[0][0]
  if mode==1: filename += '-bands'

  filename += name

  j = 0
  for plot in PLOT:

      wdir, Q2, color, style, label, alpha = plot[0], plot[1], plot[2], plot[3], plot[4], plot[5]
      load_config('%s/input.py'%wdir)
      istep=core.get_istep()

      #--load data if it exists
      try:
          if Q2==1.27**2: data=load('%s/data/pdf-%d.dat'%(wdir,istep))
          else: data=load('%s/data/pdf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
      #--generate data and then load it if it does not exist
      except:
          gen_xf(wdir,Q2)
          if Q2==1.27**2: data=load('%s/data/pdf-%d.dat'%(wdir,istep))
          else: data=load('%s/data/pdf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
          
      replicas=core.get_replicas(wdir)
      cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc) 
      best_cluster=cluster_order[0]

      X=data['X']
      X1 = data['X'][:100]
      X2 = data['X'][100:]


      ax11.plot([],[],label=label,color=color)
      for flav in data['XF']:
          mean = np.mean(data['XF'][flav],axis=0)
          std = np.std(data['XF'][flav],axis=0)

          if flav=='s+sb':           ax = ax11
          else: continue

          #--plot each replica
          if mode==0:
              for i in range(len(data['XF'][flav])):
                  #--stop at nrep replicas
                  if nrep != None and i > nrep: break

                  #--if plotting one step, use clusters
                  if len(PLOT) == 1: color = colors[cluster[i]]

                  ax.plot(X,data['XF'][flav][i],color=color,alpha=alpha)
        
          #--plot average and standard deviation
          if mode==1:
              ax.plot(X,mean,style,label=label,color=color)
              ax.fill_between(X,mean-std,mean+std,color=color,alpha=0.5)

      j+=1


  if len(PLOT) > 1: ax11.legend(loc='upper left',fontsize=25,frameon=False)

  for ax in [ax11]:
        ax.set_xlim(1e-4,1)
        ax.semilogx()
          
        ax.tick_params(axis='both', which='major', top=True, right=True, direction='in',labelsize=25,length=5  ,width=1.5)
        ax.tick_params(axis='both', which='minor', top=True, right=True, direction='in',labelsize=25,length=2.5,width=1.5)
        #ax.set_xticks([0.01,0.1,1])
        #ax.set_xticklabels([r'$0.01$',r'$0.1$',r'$1$'])

  #ax11.set_ylabel(r'\boldmath$xf(x)$',size=30)
  ax11.set_xlabel(r'\boldmath$x$'    ,size=30)

  ax11.set_ylim(0,1.5)    ,ax11.set_yticks([0,0.5,1.0,1.5])

  ax11.text(0.7,0.8,r'\boldmath{$x(s+\bar{s})$}', transform=ax11.transAxes,size=25)

  if Q2 == 1.27**2: ax11.text(0.05,0.05,r'$Q^2 = m_c^2$',              transform=ax11.transAxes,size=30)
  else:             ax11.text(0.05,0.05,r'$Q^2 = %s ~ \rm{GeV^2}$'%Q2, transform=ax11.transAxes,size=30)

  py.tight_layout()

  filename+='.png'

  checkdir('%s/gallery'%wdir)
  py.savefig(filename)
  print 'Saving figure to %s'%filename

def plot_xf_std_ratio(PLOT,kc,name=''):

  nrows,ncols=1,1
  fig = py.figure(figsize=(ncols*7,nrows*4))
  ax11=py.subplot(nrows,ncols,1)

  filename = '%s/gallery/pdfs-std-ratio'%PLOT[0][0]

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
      if Q2==1.27**2: data=load('%s/data/pdf-%d.dat'%(wdir,istep))
      else: data=load('%s/data/pdf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
  #--generate data and then load it if it does not exist
  except:
      gen_xf(wdir,Q2)
      if Q2==1.27**2: data=load('%s/data/pdf-%d.dat'%(wdir,istep))
      else: data=load('%s/data/pdf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
      
  replicas=core.get_replicas(wdir)
  cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc) 
  best_cluster=cluster_order[0]

  X=data['X']

  denom = {}
  for flav in data['XF']:
      denom[flav] = np.std(data['XF'][flav],axis=0)

  hand = {}
  for plot in PLOT:
      j+=1
      if j == 1: continue

      wdir, Q2, color, style, label, alpha = plot[0], plot[1], plot[2], plot[3], plot[4], plot[5]
      load_config('%s/input.py'%wdir)
      istep=core.get_istep()

      #--load data if it exists
      try:
          if Q2==1.27**2: data=load('%s/data/pdf-%d.dat'%(wdir,istep))
          else: data=load('%s/data/pdf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
      #--generate data and then load it if it does not exist
      except:
          gen_xf(wdir,Q2)
          if Q2==1.27**2: data=load('%s/data/pdf-%d.dat'%(wdir,istep))
          else: data=load('%s/data/pdf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
          
      replicas=core.get_replicas(wdir)
      cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc) 
      best_cluster=cluster_order[0]

      X=data['X']

      for flav in data['XF']:
          mean = np.mean(data['XF'][flav],axis=0)
          std = np.std(data['XF'][flav],axis=0)

          if flav=='uv':      color,ls = 'yellow', '--' 
          elif flav=='dv':    color,ls = 'orange', '--'  
          elif flav=='db+ub': color,ls = 'blue'  , '-' 
          elif flav=='db-ub': color,ls = 'green' , '--' 
          elif flav=='g':     color,ls = 'cyan'  , ':'
          elif flav=='s+sb':  color,ls = 'red'   , '-'
          else: continue
          ax = ax11

          #--plot std over denom
          hand[flav] ,= ax.plot(X,std/denom[flav],style,color=color,lw=5, ls=ls)

  for ax in [ax11]:
        ax.set_xlim(1e-4,0.5)
        ax.semilogx()
          
        ax.tick_params(axis='both', which='major', top=True, right=True, direction='in',labelsize=25,length=5  ,width=1.5)
        ax.tick_params(axis='both', which='minor', top=True, right=True, direction='in',labelsize=25,length=2.5,width=1.5)
        #ax.set_xticks([0.01,0.1,1])
        #ax.set_xticklabels([r'$0.01$',r'$0.1$',r'$1$'])

  ax11.axhline(1.0,alpha=0.5,ls='--',color='black')

  ax11.set_ylim(0,1.2) ,ax11.set_yticks([0.2,0.4,0.6,0.8,1.0])

  ax11.text(0.02,0.05,r'\boldmath$\delta^{\rm{EIC}}/\delta$',transform=ax11.transAxes,size=40)
  ax11.text(0.02,0.25,r'\textrm{\textbf{JAM}}'              ,transform=ax11.transAxes,size=40)
  ax11.set_xlabel(r'\boldmath$x$'    ,size=30)
  ax11.xaxis.set_label_coords(0.95,0.00)

  #if Q2 == 1.27**2: ax11.text(0.05,0.05,r'$Q^2 = m_c^2$',              transform=ax11.transAxes,size=30)
  #else:             ax11.text(0.05,0.05,r'$Q^2 = %s ~ \rm{GeV^2}$'%Q2, transform=ax11.transAxes,size=30)

  handles = []
  handles.append(hand['uv'])
  handles.append(hand['dv'])
  handles.append(hand['db+ub'])
  handles.append(hand['db-ub'])
  handles.append(hand['s+sb'])
  handles.append(hand['g'])

  labels = []
  labels.append(r'\boldmath$u_v$')
  labels.append(r'\boldmath$d_v$')
  labels.append(r'\boldmath$\bar{d} + \bar{u}$')
  labels.append(r'\boldmath$\bar{d} - \bar{u}$')
  labels.append(r'\boldmath$s + \bar{s}$')
  labels.append(r'\boldmath$g$')

  ax11.legend(handles,labels,loc='lower right', fontsize = 20, frameon = 0, handletextpad = 0.3, handlelength = 1.0, ncol = 3, columnspacing = 1.0)
  py.tight_layout()

  filename+='.png'

  checkdir('%s/gallery'%wdir)
  py.savefig(filename)
  print 'Saving figure to %s'%filename

def plot_xf_strange_compare(PLOT,kc,name=''):
  #--mode 0: plot each replica
  #--mode 1: plot average and standard deviation of replicas 

  nrows,ncols=1,1
  fig = py.figure(figsize=(ncols*7,nrows*4))
  ax11=py.subplot(nrows,ncols,1)

  filename = '%s/gallery/pdfs-strange-compare'%PLOT[0][0]

  filename += name

  j = 0
  hand = {}
  for plot in PLOT:

      wdir, Q2, color, style, label, alpha = plot[0], plot[1], plot[2], plot[3], plot[4], plot[5]
      load_config('%s/input.py'%wdir)
      istep=core.get_istep()

      #--load data if it exists
      try:
          if Q2==1.27**2: data=load('%s/data/pdf-%d.dat'%(wdir,istep))
          else: data=load('%s/data/pdf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
      #--generate data and then load it if it does not exist
      except:
          gen_xf(wdir,Q2)
          if Q2==1.27**2: data=load('%s/data/pdf-%d.dat'%(wdir,istep))
          else: data=load('%s/data/pdf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
          
      replicas=core.get_replicas(wdir)
      cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc) 
      best_cluster=cluster_order[0]

      X=data['X']

      for flav in data['XF']:
          mean = np.mean(data['XF'][flav],axis=0)
          std = np.std(data['XF'][flav],axis=0)

          if j==0: color,alpha='yellow',0.9
          if j==1: color,alpha='red'   ,0.9

          if flav=='s+sb': ax = ax11
          else: continue

          hand[j] = ax.fill_between(X,mean-std,mean+std,color=color,alpha=alpha)

      j+=1


  for ax in [ax11]:
        ax.set_xlim(1e-4,1)
        ax.semilogx()
          
        ax.tick_params(axis='both', which='major', top=True, right=True, direction='in',labelsize=25,length=5  ,width=1.5)
        ax.tick_params(axis='both', which='minor', top=True, right=True, direction='in',labelsize=25,length=2.5,width=1.5)
        ax.set_xticks([1e-4,1e-3,1e-2,1e-1])

  ax11.set_xlabel(r'\boldmath$x$'    ,size=30)
  ax11.xaxis.set_label_coords(0.95,0.00)


  ax11.set_ylim(0,1.6)    ,ax11.set_yticks([0.5,1.0,1.5])

  ax11.text(0.2,0.8,r'\boldmath{$x(s+\bar{s})$}', transform=ax11.transAxes,size=40)

  if Q2 == 1.27**2: ax11.text(0.05,0.05,r'$Q^2 = m_c^2$',              transform=ax11.transAxes,size=30)
  else:             ax11.text(0.05,0.05,r'$Q^2 = %s ~ \rm{GeV^2}$'%Q2, transform=ax11.transAxes,size=30)

  handles = []
  handles.append(hand[0])
  handles.append(hand[1])

  labels = []
  labels.append(r'\textrm{\textbf{JAM}}')
  labels.append(r'\textrm{\textbf{+EIC}}')

  ax11.legend(handles,labels,loc='upper right', fontsize = 20, frameon = 0, handletextpad = 0.3, handlelength = 1.0)
  py.tight_layout()

  filename+='.png'

  checkdir('%s/gallery'%wdir)
  py.savefig(filename)
  print 'Saving figure to %s'%filename

def plot_xf(PLOT,kc,kind=0,mode=0,name='',SETS=[],nrep=None):

    if kind==0:
        plot_xf_main(PLOT,kc,mode=0,name='',SETS=[],nrep=None)
        plot_xf_strange(PLOT,kc,mode=0,name='',SETS=[],nrep=None)
    if kind==1:
        plot_xf_std_ratio(PLOT,kc,name='')
        plot_xf_strange_compare(PLOT,kc,name='')




