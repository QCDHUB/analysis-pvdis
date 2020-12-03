#!/usr/bin/env python
import os,sys
import kmeanconf as kc
import matplotlib
matplotlib.use('Agg')
import pylab as py

#--from corelib
from analysis.corelib import core, inspect, predict, classifier, optpriors, jar, mlsamples, summary

#--from qpdlib
from analysis.qpdlib import ppdf

wdir  = 'results/pidis0'
wdir2 = 'results/pidis1'


####################
##--Plotting options
####################

#--plot multiple steps on the same plot (wdir, Q2, color, style, label, alpha)
Q21    = 10
Q22    = 10

color1 = 'red'
color2 = 'red'

label1 = None 
label2 = None 
 

ls1    = '-'
ls2    = '-'

alpha1 = 0.5
alpha2 = 0.2

PLOT = []
PLOT.append((wdir,Q21,color1,ls1,label1,alpha1))

PLOT.append((wdir2,Q22,color2,ls2,label2,alpha2))


########################
#--Polarized proton pdfs
########################
PSETS = []

nrows,ncols=1,2
fig = py.figure(figsize=(ncols*8,nrows*5))
_ax11 = py.subplot(nrows,ncols,1) 
_ax12 = py.subplot(nrows,ncols,2) 

ax11 = ppdf.plot_xf               (PLOT,kc,kind=1,_ax=_ax11)    
ax12 = ppdf.plot_moments_std_ratio(PLOT,kc,mode=1,_ax=_ax12)    

ax12.tick_params(labelleft=False)
ax12.set_xticks([1e-3,1e-2,1e-1])

py.tight_layout()
py.subplots_adjust(wspace=0)

filename = '%s/gallery/ppdfs-combined'%PLOT[0][0]
filename += '.png'
print('Saving figures to %s'%filename)
py.savefig(filename)




