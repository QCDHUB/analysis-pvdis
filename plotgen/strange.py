#!/usr/bin/env python
import os,sys
import kmeanconf as kc

#--from corelib
from analysis.corelib import core, inspect, predict, classifier, optpriors, jar, mlsamples, summary

#--from qpdlib
from analysis.qpdlib import pdf

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

color1 = 'red'
color2 = 'red'
color3 = 'green'

label1 = None 
label2 = None 
label3 = None
 
label1 = r'\textbf{\textrm{Moderate}}'
label2 = r'\textbf{\textrm{No EIC}}'
label3 = r'\textbf{\textrm{No EIC}}'

ls1    = '-'
ls2    = '-'
ls3    = '-'

alpha1 = 0.5
alpha2 = 0.2
alpha3 = 0.2

PLOT = []
PLOT.append((wdir,Q21,color1,ls1,label1,alpha1))

if wdir2 != None: PLOT.append((wdir2,Q22,color2,ls2,label2,alpha2))
if wdir3 != None: PLOT.append((wdir3,Q23,color3,ls3,label3,alpha3))

Q2 = Q21

#--name to append at end of file
#name = ''
name = '-combined-'

#--maximum number of replicas to plot
nrep = None
#nrep = 50

#--mode: 0 for all replicas, 1 for mean and std
mode = 0


###################
#--Plot proton pdfs
###################
SETS = []
#SETS.append('CJ15')
#SETS.append('JAM19')
#SETS.append('ABMP16')
#SETS.append('NNPDF')

#pdf.gen_xf(wdir,Q2)         
pdf.plot_xf(PLOT,kc,kind=1,mode=mode,name=name,SETS=SETS)                




