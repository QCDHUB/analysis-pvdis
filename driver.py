#!/usr/bin/env python
import os,sys
import kmeanconf as kc

#--from corelib
from analysis.corelib import core, inspect, predict, classifier, optpriors, jar, mlsamples, summary

#--from qpdlib
from analysis.qpdlib import pdf
from analysis.qpdlib import ppdf

#--from obslib
from analysis.obslib  import stf
from analysis.obslib  import off
from analysis.obslib  import ht

from analysis.obslib  import sin2w

from analysis.obslib  import idis
from analysis.obslib  import dy
from analysis.obslib  import wasym
from analysis.obslib  import zrap
from analysis.obslib  import wzrv
from analysis.obslib  import pvdis
#from analysis.obslib  import AL
from analysis.obslib import data

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

#########################
##--Simulation for structure functions
#########################
tar   = 'h'
force = False

stf_sim.stf(wdir,tar=tar,force=force)

#########################
##--Simulation for PVDIS
#########################
kind  = 'had'
tar   = 'p'
est   = 'mod'
lum   = '100:fb-1'
force = False

#pvdis_sim.pvdis(wdir,kind=kind,tar=tar,est=est,lum=lum,force=force)


######################
##--Initial Processing
######################
FILT = []
#FILT.append(('dv1 b',5.6,'greater'))

#inspect.get_msr_inspected(wdir,limit=2.0,FILT=FILT)
#predict.get_predictions(wdir,force=False)
#classifier.gen_labels(wdir,kc)
#jar.gen_jar_file(wdir,kc)
#summary.print_summary(wdir,kc)

###################
##--Optimize priors
###################

#optpriors.gen_priors(wdir,kc,10)

###################
##--Data generation
###################

#stf.gen_stf(wdir,Q2)
#stf.gen_CCstf(wdir,Q2)

########################
##--Plot dis metrics
########################
compare = False

#stf.plot_stf(wdir,Q2,kc,mode,name=name)
#stf.plot_rat(PLOT,kc,mode,name=name,nrep=nrep)
#stf.plot_CCstf(wdir,Q2,kc,mode,name=name)
#off.plot_off(PLOT,kc,mode,iso=True,name=name,nrep=nrep,compare=compare)
#ht.plot_ht(PLOT,kc,mode,name=name,nrep=nrep)

########################
##--Plot sin2w
########################

#sin2w.plot_sin2w(PLOT,kc,mode=0,name=name,nrep=nrep)

###################
#--Plot proton pdfs
###################
SETS = []
#SETS.append('CJ15')
#SETS.append('JAM19')
#SETS.append('ABMP16')
#SETS.append('NNPDF')

#pdf.gen_xf(wdir,Q2)         
#pdf.plot_xf(PLOT,kc,mode,name=name,SETS=SETS)                

###########################
##--Parameter distributions
###########################
hist=True

#params.plot_params(wdir,'pdf',kc,hist)
#params.plot_params(wdir,'ht4',kc,hist)
#params.plot_params(wdir,'off',kc,hist)

####################
##--Observable plots
####################

#idis.plot_obs(wdir,kc,plot_HERA=True)
#dy.plot_obs(wdir,kc,ratio=ratio)
#zrap.plot_zrap(wdir)
#wasym.plot_wasym(wdir,kc)
#wzrv.plot_wzrv(wdir)
#pvdis.plot_obs(wdir,kc,'e')
#pvdis.plot_obs(wdir,kc,'had')


############################
##--Plot all data points
############################

#data.plot_data()

##---------------------------------------------------------------
##--Polarized
##---------------------------------------------------------------


########################
#--Polarized proton pdfs
########################
PSETS = []

#ppdf.gen_xf(wdir,Q2=Q2)         
#ppdf.plot_xf(PLOT,kc,mode=0,name='',PSETS=PSETS)

########################
#--polarized observables
########################
    
##AL.plot_A_L(wdir,kc)

###########################
##--Parameter distributions
###########################

#params.plot_params(wdir,'ppdf',kc,hist=hist)




