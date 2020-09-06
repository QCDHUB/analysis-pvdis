#!/usr/bin/env python

import sys,os
import numpy as np

#--matplotlib
import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import cm
import pylab as py

#--from local
from analysis.corelib import core

#--from tools
from tools.tools     import load,save,checkdir,lprint
from tools.config    import conf,load_config

#--from fitpack
from obslib.idis.reader    import READER as idisREAD
from obslib.dy.reader      import READER as dyREAD
from obslib.wasym.reader   import READER as wasymREAD
from obslib.zrap.reader    import READER as zrapREAD
from obslib.wzrv.reader    import READER as wzrvREAD
from qcdlib import aux

conf['aux']=aux.AUX()

def load_data():
    conf['datasets']={}
    conf['datasets']['idis']={}
    conf['datasets']['idis']['xlsx']={}
    conf['datasets']['idis']['xlsx'][10010] = 'idis/expdata/10010.xlsx'  
    conf['datasets']['idis']['xlsx'][10011] = 'idis/expdata/10011.xlsx'
    conf['datasets']['idis']['xlsx'][10016] = 'idis/expdata/10016.xlsx'
    conf['datasets']['idis']['xlsx'][10017] = 'idis/expdata/10017.xlsx'
    conf['datasets']['idis']['xlsx'][10020] = 'idis/expdata/10020.xlsx'
    conf['datasets']['idis']['xlsx'][10021] = 'idis/expdata/10021.xlsx'
    conf['datasets']['idis']['xlsx'][10026] = 'idis/expdata/10026.xlsx'
    conf['datasets']['idis']['xlsx'][10027] = 'idis/expdata/10027.xlsx'
    conf['datasets']['idis']['xlsx'][10028] = 'idis/expdata/10028.xlsx'
    conf['datasets']['idis']['xlsx'][10029] = 'idis/expdata/10029.xlsx'
    conf['datasets']['idis']['xlsx'][10030] = 'idis/expdata/10030.xlsx'
    conf['datasets']['idis']['xlsx'][10031] = 'idis/expdata/10031.xlsx'
    conf['datasets']['idis']['xlsx'][10032] = 'idis/expdata/10032.xlsx'
    conf['datasets']['idis']['xlsx'][10002] = 'idis/expdata/10002.xlsx'
    conf['datasets']['idis']['xlsx'][10003] = 'idis/expdata/10003.xlsx'
    conf['datasets']['idis']['xlsx'][10033] = 'idis/expdata/10033.xlsx'
    conf['datasets']['idis']['filters']=[]
    conf['datasets']['idis']['filters'].append("Q2>1.3**2")
    conf['datasets']['idis']['filters'].append("W2>4.0")

    idis=idisREAD().load_data_sets('idis')

    conf['datasets']={}
    conf['datasets']['dy']={}
    conf['datasets']['dy']['xlsx']={}
    conf['datasets']['dy']['xlsx'][10001] = 'dy/expdata/10001.xlsx'  
    conf['datasets']['dy']['xlsx'][10002] = 'dy/expdata/10002.xlsx'
    conf['datasets']['dy']['filters']=[]
    conf['datasets']['dy']['filters'].append("Q2>36")

    dy=dyREAD().load_data_sets('dy')

    conf['datasets']={}
    conf['datasets']['wasym']={}
    conf['datasets']['wasym']['xlsx']={}
    conf['datasets']['wasym']['xlsx'][1000] = 'wasym/expdata/1000.xlsx'  
    conf['datasets']['wasym']['xlsx'][1001] = 'wasym/expdata/1001.xlsx'

    wasym=wasymREAD().load_data_sets('wasym')

    conf['datasets']={}
    conf['datasets']['zrap']={}
    conf['datasets']['zrap']['xlsx']={}
    conf['datasets']['zrap']['xlsx'][1000] = 'zrap/expdata/1000.xlsx'  
    conf['datasets']['zrap']['xlsx'][1001] = 'zrap/expdata/1001.xlsx'

    zrap=zrapREAD().load_data_sets('zrap')

    conf['datasets']={}
    conf['datasets']['wzrv']={}
    conf['datasets']['wzrv']['xlsx']={}
    conf['datasets']['wzrv']['xlsx'][2000] = 'wzrv/expdata/2000.xlsx'  
    conf['datasets']['wzrv']['xlsx'][2003] = 'wzrv/expdata/2003.xlsx'
    conf['datasets']['wzrv']['xlsx'][2006] = 'wzrv/expdata/2006.xlsx'
    conf['datasets']['wzrv']['xlsx'][2007] = 'wzrv/expdata/2007.xlsx'
    conf['datasets']['wzrv']['xlsx'][2009] = 'wzrv/expdata/2009.xlsx'
    conf['datasets']['wzrv']['xlsx'][2010] = 'wzrv/expdata/2010.xlsx'
    conf['datasets']['wzrv']['xlsx'][2011] = 'wzrv/expdata/2011.xlsx'
    conf['datasets']['wzrv']['xlsx'][2012] = 'wzrv/expdata/2012.xlsx'
    conf['datasets']['wzrv']['xlsx'][2013] = 'wzrv/expdata/2013.xlsx'
    conf['datasets']['wzrv']['xlsx'][2014] = 'wzrv/expdata/2014.xlsx'
    conf['datasets']['wzrv']['xlsx'][2015] = 'wzrv/expdata/2015.xlsx'

    wzrv=wzrvREAD().load_data_sets('wzrv')






    return idis, dy, wasym, zrap, wzrv

def plot_data():
  #--Plot all data
  s = 20

  idis,dy,wasym,zrap,wzrv=load_data()

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

  #--plot DIS
  for idx in idis:
      X = idis[idx]['X']
      Q2= idis[idx]['Q2']
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
      if idx==10016: label,color=r'\textrm{BCDMS}','black'
      elif idx==10017: color='black'
      elif idx==10020: label,color=r'\textrm{NMC}','goldenrod'
      elif idx==10021: color='goldenrod'
      elif idx==10010: label,color=r'\textrm{SLAC}','blue'
      elif idx==10011: color='blue'
      elif idx==10026: label,color=r'\textrm{HERA}','green'
      elif idx==10027: color='green'
      elif idx==10028: color='green'
      elif idx==10029: color='green'
      elif idx==10030: color='green'
      elif idx==10031: color='green'
      elif idx==10032: color='green'
      elif idx==10033: label,color=r'\textrm{BONUS}','orange'
      elif idx==10002: label,color=r'\textrm{JLab}','red'
      elif idx==10003: color='red'
      else: continue

      ax .scatter(X1,Q21,c=color,label=label,s=s)
      axL.scatter(X2,Q22,c=color,label=label,s=s)

  #--plot DY
  for idx in dy:
      Y = dy[idx]['Y']
      tau = dy[idx]['tau']
      X = 2*np.sqrt(tau)*np.sinh(Y)
      Q2= dy[idx]['Q2']
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
      if idx == 10001: label = r'\textrm{Fermilab (DY)}'
      color = 'magenta'
      ax .scatter(X1,Q21,c=color,label=label,s=s)
      axL.scatter(X2,Q22,c=color,label=label,s=s)

  #--plot wasym
  for idx in wasym:
      Y = wasym[idx]['Y']
      Q2  = 80.398**2*np.ones(len(Y))
      S   = wasym[idx]['S']
      tau = Q2/S
      X = 2*np.sqrt(tau)*np.sinh(Y)
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
      if idx == 1000: label = r'\textrm{Tevatron (W/Z/lep)}'
      color = 'maroon'
      ax .scatter(X1,Q21,c=color,label=label,s=s)
      axL.scatter(X2,Q22,c=color,label=label,s=s)

  #--plot zrap
  for idx in zrap:
      Y = zrap[idx]['Y']
      Q2  = 91.1876**2*np.ones(len(Y))
      S   = zrap[idx]['S']
      tau = Q2/S
      X = 2*np.sqrt(tau)*np.sinh(Y)
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
      color = 'maroon'
      ax .scatter(X1,Q21,c=color,label=label,s=s)
      axL.scatter(X2,Q22,c=color,label=label,s=s)

  #--plot wzrv
  for idx in wzrv:
      if 'eta' in wzrv[idx]:
          Y = wzrv[idx]['eta']
      else:
          Y = (wzrv[idx]['eta_min'] + wzrv[idx]['eta_max'])/2.0
      Q2  = 80.398**2*np.ones(len(Y))
      S   = wzrv[idx]['cms']**2
      tau = Q2/S
      X = 2*np.sqrt(tau)*np.sinh(Y)
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
      if idx == 2000: color = 'maroon'
      if idx == 2003: color = 'maroon'
      if idx == 2006: color = 'maroon'
      if idx == 2007: label,color = r'\textrm{LHC (lep)}','darkcyan'
      if idx == 2009: color = 'darkcyan'
      if idx == 2010: color = 'darkcyan'
      if idx == 2011: color = 'darkcyan'
      if idx == 2012: color = 'darkcyan'
      if idx == 2013: color = 'darkcyan'
      if idx == 2014: color = 'darkcyan'
      if idx == 2015: color = 'darkcyan'
      ax .scatter(X1,Q21,c=color,label=label,s=s)
      axL.scatter(X2,Q22,c=color,label=label,s=s)

  #--Plot cuts
  x = np.linspace(0.1,0.9,100)
  W2cut10_p=np.zeros(len(x))
  W2cut10_d=np.zeros(len(x))
  W2cut4_p=np.zeros(len(x))
  W2cut4_d=np.zeros(len(x))
  Q2cut=np.ones(len(x))*1.3**2

  for i in range(len(x)):
      W2cut10_p[i]=(10.0-(0.938)**2)*(x[i]/(1-x[i]))
      W2cut10_d[i]=(10.0-(1.8756)**2)*(x[i]/(1-x[i]))
      W2cut4_p[i]=(4.0-(0.938)**2)*(x[i]/(1-x[i]))
      W2cut4_d[i]=(4.0-(1.8756)**2)*(x[i]/(1-x[i]))

  axL.plot(x,W2cut10_p,'k--')#,label=r'$W^2=10$ $GeV^2$')
  axL.plot(x,W2cut4_p,c='k')#, label=r'$W^2=4$ $GeV^2$')
  ax .plot([],[], 'k--')#, label=r'$W^2=10$ $GeV^2$')
  ax .plot([],[], c='k')#, label=r'$W^2=4$ $GeV^2$')

  ax.axvline(0.1,color='black',ls=':',alpha=0.5)

  ax.legend(loc='upper left',fontsize=20,frameon=False)
  ax .tick_params(axis='both',which='both',top=True,right=False,direction='in',labelsize=20)
  axL.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=20)

  ax.set_xscale('log')
  ax.set_yscale('log')

  ax.set_xlim(2e-5,0.1)
  ax.set_ylim(1,10e4)
  ax. set_xticks([1e-4,1e-3,1e-2])
  ax. set_xticklabels([r'$10^{-4}$',r'$10^{-3}$',r'$10^{-2}$'])
  axL.set_xticks([0.1,0.3,0.5,0.7,0.9])

  ax.set_xlabel(r'$x$',size=30)
  ax.xaxis.set_label_coords(1,-0.1)
  ax.set_ylabel(r'$Q^2~(GeV^2)$',size=30)

  py.tight_layout()
  filename='data'
  filename+='.png'

  py.savefig(filename)
  print 'Saving figure to %s'%filename 


if __name__ == "__main__":

  plot_data()




