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
from qpdcalc import QPDCALC
from analysis.corelib import core
from analysis.corelib import classifier

def plot_xf_strange_ratio(PLOT,kc,name='',nrep=None):

  nrows,ncols=1,1
  fig = py.figure(figsize=(ncols*7,nrows*4))
  ax11=py.subplot(nrows,ncols,1)

  filename = '%s/gallery/pdfs-strange'%PLOT[0][0]
  if mode==1: filename += '-bands'

  filename += name

  #--first entry is unpolarized
  plot = PLOT[0]
  wdir, Q2, color, style, label, alpha = plot[0], plot[1], plot[2], plot[3], plot[4], plot[5]
  load_config('%s/input.py'%wdir)
  istep=core.get_istep()

  if Q2==1.27**2: data=load('%s/data/pdf-%d.dat'%(wdir,istep))
  else: data=load('%s/data/pdf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
      
  replicas=core.get_replicas(wdir)
  cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc) 
  best_cluster=cluster_order[0]

  X=data['X']
  X1 = data['X'][:100]
  X2 = data['X'][100:]

  for flav in data['XF']:
      if flav=='s+sb':
          u     = data['XF'][flav]
          umean = np.mean(data['XF'][flav],axis=0)
          ustd  = np.std(data['XF'][flav],axis=0)

      else: continue

  #--second entry is polarized
  plot = PLOT[1]
  wdir, Q2, color, style, label, alpha = plot[0], plot[1], plot[2], plot[3], plot[4], plot[5]
  load_config('%s/input.py'%wdir)
  istep=core.get_istep()

  if Q2==1.27**2: data=load('%s/data/ppdf-%d.dat'%(wdir,istep))
  else: data=load('%s/data/ppdf-%d-Q2=%d.dat'%(wdir,istep,int(Q2)))
      
  replicas=core.get_replicas(wdir)
  cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc) 
  best_cluster=cluster_order[0]

  X=data['X']
  X1 = data['X'][:100]
  X2 = data['X'][100:]

  for flav in data['XF']:
      if flav=='sp':
          p     = data['XF'][flav]
          pmean = np.mean(data['XF'][flav],axis=0)
          pstd  = np.std(data['XF'][flav],axis=0)


  ax.plot(X,mean,style,label=label,color=color)
  ax.fill_between(X,mean-std,mean+std,color=color,alpha=0.5)

  for ax in [ax11]:
        ax.set_xlim(1e-4,1)
        ax.semilogx()
          
        ax.tick_params(axis='both', which='major', top=True, right=True, direction='in',labelsize=25,length=5  ,width=1.5)
        ax.tick_params(axis='both', which='minor', top=True, right=True, direction='in',labelsize=25,length=2.5,width=1.5)
        #ax.set_xticks([0.01,0.1,1])
        #ax.set_xticklabels([r'$0.01$',r'$0.1$',r'$1$'])

  ax11.set_ylabel(r'\boldmath$\delta s/s$',size=30)
  ax11.set_xlabel(r'\boldmath$x$'    ,size=30)

  #ax11.set_ylim(0,1.5)    ,ax11.set_yticks([0,0.5,1.0,1.5])

  ax11.set_ylabel(r'$xf(x)$',size=30)
  ax11.set_xlabel(r'$x$'    ,size=30)

  ax11.text(0.7,0.8,r'\boldmath{$x(s+\bar{s})$}', transform=ax11.transAxes,size=25)

  if Q2 == 1.27**2: ax11.text(0.05,0.05,r'$Q^2 = m_c^2$',              transform=ax11.transAxes,size=30)
  else:             ax11.text(0.05,0.05,r'$Q^2 = %s ~ \rm{GeV^2}$'%Q2, transform=ax11.transAxes,size=30)

  py.tight_layout()

  filename+='.png'

  checkdir('%s/gallery'%wdir)
  py.savefig(filename)
  print 'Saving figure to %s'%filename

def plot_xf(PLOT,kc,name='',nrep=None):

    plot_xf_strange_ratio(PLOT,kc,name='',nrep=None)




