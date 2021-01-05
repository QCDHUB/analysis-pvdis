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

#--from parlib
from analysis.parlib  import params

#--from simlib
from analysis.simlib  import pvdis_sim
from analysis.simlib  import stf_sim

#--primary working directory
wdir=sys.argv[1]

#########################
##--Simulation for structure functions
#########################
tar   = 'h'
force = False

#stf_sim.stf(wdir,tar=tar,force=force)

#########################
##--Simulation for PVDIS
#########################
#--'e' for polarized electron, 'had' for polarized hadron
kind  = 'had'
#--choose target: 'p', 'd', or 'h'
tar   = 'p'
#--choose systematic errors (always choose 'mod')
est   = 'mod'
#--choose to use mean or mean +- std of replicas
central   = 'max'
#--if True, force predictions to be regenerated
force = False
#--if None, default to 100fb-1 for proton, 10fb-1 for deuteron and helium.
#--can choose instead, for example, lum = '500:fb-1'
lum   = None

#FILT = []
#FILT.append(('ppdf','g1 N', 0.0, 'less'))
#inspect.get_msr_inspected(wdir,limit=2.0,FILT=FILT)
pvdis_sim.pvdis(wdir,kind=kind,tar=tar,est=est,central=central,lum=lum,force=force)




