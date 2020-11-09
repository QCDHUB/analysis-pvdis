#!/usr/bin/env python
import os,sys
import kmeanconf as kc
#--from corelib
from analysis.corelib import core, inspect, predict, classifier, optpriors, jar, mlsamples, summary
#--from obslib
from analysis.obslib  import sin2w

#--primary working directory
wdir=sys.argv[1]

#--look for extra working directories
try: wdir2 = sys.argv[2]
except: wdir2 = None
try: wdir3 = sys.argv[3]
except: wdir3 = None


####################
##--Plotting options
####################

#--plot multiple steps on the same plot (wdir, Q2, color, style, label, alpha)
Q21    = 10
Q22    = 10
Q23    = 10

color1 = 'yellow'
color2 = 'red'
color3 = 'green'

label1 = r'\textbf{\textrm{+EIC d}}'
label2 = r'\textbf{\textrm{+EIC p}}'
label3 = r'\textbf{\textrm{+p,d}}'

ls1    = '-'
ls2    = '-'
ls3    = '-'

alpha1 = 0.9
alpha2 = 0.9
alpha3 = 0.2

PLOT = []
PLOT.append((wdir,Q21,color1,ls1,label1,alpha1))

if wdir2 != None: PLOT.append((wdir2,Q22,color2,ls2,label2,alpha2))
if wdir3 != None: PLOT.append((wdir3,Q23,color3,ls3,label3,alpha3))

Q2 = Q21

#--name to append at end of file
name = ''
name = '-compare'

########################
##--Plot sin2w
########################

sin2w.plot_sin2w(PLOT,kc,mode=1,name=name)


