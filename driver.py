#!/usr/bin/env python
import os,sys
import kmeanconf as kc

#--from corelib
from analysis.corelib import core, inspect, predict, classifier, optpriors, jar, mlsamples, summary

#--from qpdlib
from analysis.qpdlib import pdf
from analysis.qpdlib import ppdf

#--from obslib
from analysis.obslib  import sin2w
from analysis.obslib  import pvdis
from analysis.obslib  import kin
from analysis.obslib  import SU23

#--from parlib
from analysis.parlib  import params

#--from simlib
from analysis.simlib  import pvdis_sim
from analysis.simlib  import stf_sim

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
color2 = 'darkcyan'
color3 = 'green'

label1 = None 
label2 = None 
label3 = None
 
label1 = r'\textbf{\textrm{JAM}}'
label2 = r'\textbf{\textrm{No EIC}}'

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
name = ''
#name = '-LHC-compare'

#--maximum number of replicas to plot
nrep = None
#nrep = 50

#--mode: 0 for all replicas, 1 for mean and std
mode = 0

######################
##--Initial Processing
######################
FILT = []
#FILT.append(('dv1 c',-25,'less'))
#FILT.append(('g1 a',-0.5,'less'))
#FILT.append(('uv1 b', 0.1,'less'))
#FILT.append(('s2wMZ',0.235,'greater'))
#FILT.append(('ppdf','g1 N',   '<', 0.0))
#FILT.append(('ppdf','uv1 b',  '<', 0.1))
#FILT.append(('ppdf','dv1 N', '>', 1.5))

inspect.get_msr_inspected(wdir,limit=2.0,FILT=FILT)
predict.get_predictions(wdir,force=False)
classifier.gen_labels(wdir,kc)
jar.gen_jar_file(wdir,kc)
summary.print_summary(wdir,kc)


#kin.plot(wdir,True)

###################
##--Optimize priors
###################

#optpriors.gen_priors(wdir,kc,10)

########################
##--Plot sin2w
########################

#sin2w.plot_sin2w(PLOT,kc,mode=1,name=name,nrep=nrep)

###################
#--Plot proton pdfs
###################
SETS = []

#pdf.gen_xf(wdir,Q2)         
#pdf.plot_xf(PLOT,kc,kind=0,mode=mode,name=name,SETS=SETS)

###########################
##--Parameter distributions
###########################
hist=False

#params.plot_params(wdir,'pdf',kc,hist)
#params.plot_params(wdir,'eweak',kc,hist)

####################
##--Observable plots
####################

#pvdis.plot_obs(wdir,kc,'e','p')
#pvdis.plot_obs(wdir,kc,'e','d')
#pvdis.plot_obs(wdir,kc,'had','p')

#pvdis.compare(PLOT,kc,'e','p')
#pvdis.compare(PLOT,kc,'e','d')
#pvdis.compare(PLOT,kc,'had','p')

SU23.plot_obs(wdir,kc)

##---------------------------------------------------------------
##--Polarized
##---------------------------------------------------------------


########################
#--Polarized proton pdfs
########################
PSETS = []

ppdf.gen_xf(wdir,Q2=Q2)         
ppdf.plot_xf(PLOT,kc,mode=0,name='',PSETS=PSETS)

#--moments
#ppdf.gen_moments(wdir,Q2=Q2)         
#ppdf.plot_moments(PLOT,kc,mode=1)

###########################
##--Parameter distributions
###########################

params.plot_params(wdir,'ppdf',kc,hist=hist)




