import os
conf={}

#--fitting setups
conf['bootstrap']=True
conf['flat par']=True
conf['ftol']=1e-8

#--setups for DGLAP
conf['dglap mode']='truncated'
conf['alphaSmode']='backward'
conf['order'] = 'NLO'
conf['Q20']   = 1.27**2

#--setups for IDIS (given with each step for convenience) 
#conf['tmc']   = False
#conf['ht']    = False
#conf['offshell'] = False

conf['nuc']   = True

#--datasets

conf['datasets']={}

#--lepton-hadron reactions

Q2cut=1.3**2
W2cut=3.0

##--IDIS
conf['datasets']['idis']={}
conf['datasets']['idis']['filters']=[]
conf['datasets']['idis']['filters'].append("Q2>%f"%Q2cut)
conf['datasets']['idis']['filters'].append("W2>%f"%W2cut)
conf['datasets']['idis']['xlsx']={}
#------------------------------------------------------------------------------------------------------------------
conf['datasets']['idis']['xlsx'][10010]='idis/expdata/10010.xlsx' # proton   | F2            | SLAC
conf['datasets']['idis']['xlsx'][10016]='idis/expdata/10016.xlsx' # proton   | F2            | BCDMS
conf['datasets']['idis']['xlsx'][10020]='idis/expdata/10020.xlsx' # proton   | F2            | NMC
conf['datasets']['idis']['xlsx'][10003]='idis/expdata/10003.xlsx' # proton   | sigma red     | JLab Hall C (E00-106)
conf['datasets']['idis']['xlsx'][10026]='idis/expdata/10026.xlsx' # proton   | sigma red     | HERA II NC e+ (1)
conf['datasets']['idis']['xlsx'][10027]='idis/expdata/10027.xlsx' # proton   | sigma red     | HERA II NC e+ (2)
conf['datasets']['idis']['xlsx'][10028]='idis/expdata/10028.xlsx' # proton   | sigma red     | HERA II NC e+ (3)
conf['datasets']['idis']['xlsx'][10029]='idis/expdata/10029.xlsx' # proton   | sigma red     | HERA II NC e+ (4)
conf['datasets']['idis']['xlsx'][10030]='idis/expdata/10030.xlsx' # proton   | sigma red     | HERA II NC e-
conf['datasets']['idis']['xlsx'][10031]='idis/expdata/10031.xlsx' # proton   | sigma red     | HERA II CC e+
conf['datasets']['idis']['xlsx'][10032]='idis/expdata/10032.xlsx' # proton   | sigma red     | HERA II CC e-
conf['datasets']['idis']['xlsx'][10007]='idis/expdata/10007.xlsx' # proton   | sigma red     | HERMES
#------------------------------------------------------------------------------------------------------------------
conf['datasets']['idis']['xlsx'][10011]='idis/expdata/10011.xlsx' # deuteron | F2            | SLAC
conf['datasets']['idis']['xlsx'][10017]='idis/expdata/10017.xlsx' # deuteron | F2            | BCDMS
conf['datasets']['idis']['xlsx'][10021]='idis/expdata/10021.xlsx' # d/p      | F2d/F2p       | NMC
conf['datasets']['idis']['xlsx'][10006]='idis/expdata/10006.xlsx' # deuteron | F2            | HERMES
conf['datasets']['idis']['xlsx'][10002]='idis/expdata/10002.xlsx' # deuteron | F2            | JLab Hall C (E00-106)
conf['datasets']['idis']['xlsx'][10033]='idis/expdata/10033.xlsx' # n/d      | F2n/F2d       | BONUS
#------------------------------------------------------------------------------------------------------------------
conf['datasets']['idis']['norm']={}
conf['datasets']['idis']['norm'][10002]={'value':    1.00000e+00, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['idis']['norm'][10003]={'value':    1.00000e+00, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['idis']['norm'][10010]={'value':    1.04352e+00, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['idis']['norm'][10011]={'value':    1.04141e+00, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['idis']['norm'][10016]={'value':    9.89544e-01, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['idis']['norm'][10017]={'value':    1.01306e+00, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['idis']['norm'][10020]={'value':    1.02003e+00, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['idis']['norm'][10033]={'value':    1.00000e+00, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}

#--hadron-hadron reactions

##--DY 
conf['datasets']['dy']={}
conf['datasets']['dy']['filters']=[]
conf['datasets']['dy']['filters'].append("Q2>36") 
conf['datasets']['dy']['xlsx']={}
#------------------------------------------------------------------------------------------------------------------
conf['datasets']['dy']['xlsx'][10001]='dy/expdata/10001.xlsx'
conf['datasets']['dy']['xlsx'][10002]='dy/expdata/10002.xlsx'
#------------------------------------------------------------------------------------------------------------------
conf['datasets']['dy']['norm']={}
conf['datasets']['dy']['norm'][10001]={'value':    1,'fixed':False,'min':   0.8,'max':    1.2}
conf['datasets']['dy']['norm'][10002]={'value':    1,'fixed':False,'min':   0.8,'max':    1.2}
#------------------------------------------------------------------------------------------------------------------

##--charge asymmetry 
conf['datasets']['wzrv']={}
conf['datasets']['wzrv']['filters']=[]
conf['datasets']['wzrv']['xlsx']={}
#------------------------------------------------------------------------------------------------------------------
conf['datasets']['wzrv']['xlsx'][2000]='wzrv/expdata/2000.xlsx'
conf['datasets']['wzrv']['xlsx'][2003]='wzrv/expdata/2003.xlsx'
conf['datasets']['wzrv']['xlsx'][2006]='wzrv/expdata/2006.xlsx'
conf['datasets']['wzrv']['xlsx'][2007]='wzrv/expdata/2007.xlsx'
conf['datasets']['wzrv']['xlsx'][2008]='wzrv/expdata/2008.xlsx'  #--ATLAS 2011 w/ correlated uncertainties
conf['datasets']['wzrv']['xlsx'][2009]='wzrv/expdata/2009.xlsx'
conf['datasets']['wzrv']['xlsx'][2010]='wzrv/expdata/2010.xlsx'
conf['datasets']['wzrv']['xlsx'][2011]='wzrv/expdata/2011.xlsx'
conf['datasets']['wzrv']['xlsx'][2012]='wzrv/expdata/2012.xlsx'
conf['datasets']['wzrv']['xlsx'][2013]='wzrv/expdata/2013.xlsx'
conf['datasets']['wzrv']['xlsx'][2014]='wzrv/expdata/2014.xlsx'
conf['datasets']['wzrv']['xlsx'][2015]='wzrv/expdata/2015.xlsx'  #--ATLAS 2011 w/ uncorrelated uncertainties
#------------------------------------------------------------------------------------------------------------------
conf['datasets']['wzrv']['norm']={}
#------------------------------------------------------------------------------------------------------------------

##--W asymmetry 
conf['datasets']['wasym']={}
conf['datasets']['wasym']['filters']=[]
conf['datasets']['wasym']['xlsx']={}
#------------------------------------------------------------------------------------------------------------------
conf['datasets']['wasym']['xlsx'][1000]='wasym/expdata/1000.xlsx'
conf['datasets']['wasym']['xlsx'][1001]='wasym/expdata/1001.xlsx'
#------------------------------------------------------------------------------------------------------------------
conf['datasets']['wasym']['norm']={}
#------------------------------------------------------------------------------------------------------------------

##--W asymmetry 
conf['datasets']['zrap']={}
conf['datasets']['zrap']['filters']=[]
conf['datasets']['zrap']['xlsx']={}
#------------------------------------------------------------------------------------------------------------------
conf['datasets']['zrap']['xlsx'][1000]='zrap/expdata/1000.xlsx'
conf['datasets']['zrap']['xlsx'][1001]='zrap/expdata/1001.xlsx'
#------------------------------------------------------------------------------------------------------------------
conf['datasets']['zrap']['norm']={}
#------------------------------------------------------------------------------------------------------------------


#--parameters
conf['params']={}

#--pdf parameters
conf['params']['pdf']={}

conf['params']['pdf']['g1 N']    ={'value':    3.87592e-01   , 'min':  None, 'max':  None, 'fixed': True }
conf['params']['pdf']['g1 a']    ={'value':   -6.23068169e-01, 'min':  -1.9, 'max':     1, 'fixed': False}
conf['params']['pdf']['g1 b']    ={'value':    9.25741583e+00, 'min':     0, 'max':    20, 'fixed': False}
conf['params']['pdf']['g1 c']    ={'value':    0.00000000e+00, 'min':  -100, 'max':    100, 'fixed': False}
conf['params']['pdf']['g1 d']    ={'value':    0.00000000e+00, 'min':  -100, 'max':    100, 'fixed': False}

conf['params']['pdf']['uv1 N']   ={'value':    3.47549e-01   , 'min':  None, 'max':  None, 'fixed': True }
conf['params']['pdf']['uv1 a']   ={'value':   -1.21835956e-01, 'min':  -0.9, 'max':     1, 'fixed': False}
conf['params']['pdf']['uv1 b']   ={'value':    3.20766744e+00, 'min':     0, 'max':    10, 'fixed': False}
conf['params']['pdf']['uv1 c']   ={'value':    0.00000000e+00, 'min':   -100, 'max':    100, 'fixed': False}
conf['params']['pdf']['uv1 d']   ={'value':    0.00000000e+00, 'min':   -100, 'max':    100, 'fixed': False}

conf['params']['pdf']['dv1 N']   ={'value':    1.52089e-01   , 'min':  None, 'max':  None, 'fixed': True }
conf['params']['pdf']['dv1 a']   ={'value':   -2.39874967e-01, 'min':  -0.9, 'max':     1, 'fixed': False}
conf['params']['pdf']['dv1 b']   ={'value':    3.83902620e+00, 'min':     0, 'max':    10, 'fixed': False}
conf['params']['pdf']['dv1 c']   ={'value':    0.00000000e+00, 'min':   -100, 'max':    100, 'fixed': False}
conf['params']['pdf']['dv1 d']   ={'value':    0.00000000e+00, 'min':   -100, 'max':    100, 'fixed': False}

conf['params']['pdf']['mix N']    ={'value':    0.00000000e+00   , 'min':   0.0, 'max': 1.0, 'fixed': False}
conf['params']['pdf']['mix a']    ={'value':    2.00000000e+00   , 'min':   1.0, 'max': 6.0, 'fixed': False}
#conf['params']['pdf']['mix b']    ={'value':    0.00000000e+00   , 'min':  None, 'max': None, 'fixed': True}
#conf['params']['pdf']['mix c']    ={'value':    0.00000000e+00   , 'min':  None, 'max': None, 'fixed': True}
#conf['params']['pdf']['mix d']    ={'value':    0.00000000e+00   , 'min':  None, 'max': None, 'fixed': True}

conf['params']['pdf']['db1 N']   ={'value':    3.67609928e-02, 'min':     0, 'max':     1, 'fixed': False}
conf['params']['pdf']['db1 a']   ={'value':   -8.41360631e-01, 'min':    -1, 'max':     1, 'fixed': False}
conf['params']['pdf']['db1 b']   ={'value':    5.31285539e+00, 'min':     0, 'max':    50, 'fixed': False}
conf['params']['pdf']['db1 c']   ={'value':    0.00000000e+00, 'min':   -100, 'max':    100, 'fixed': False}
conf['params']['pdf']['db1 d']   ={'value':    0.00000000e+00, 'min':   -100, 'max':    100, 'fixed': False}

conf['params']['pdf']['ub1 N']   ={'value':    1.95464789e-02, 'min':     0, 'max':     1, 'fixed': False}
conf['params']['pdf']['ub1 a']   ={'value':   -9.93659187e-01, 'min':    -1, 'max':     1, 'fixed': False}
conf['params']['pdf']['ub1 b']   ={'value':    8.38905814e+00, 'min':     0, 'max':    20, 'fixed': False}
conf['params']['pdf']['ub1 c']   ={'value':    0.00000000e+00, 'min':   -100, 'max':    100, 'fixed': False}
conf['params']['pdf']['ub1 d']   ={'value':    0.00000000e+00, 'min':   -100, 'max':    100, 'fixed': False}

conf['params']['pdf']['s1 N']    ={'value':       0.00000e+00, 'min':     0, 'max':     1, 'fixed': True }
conf['params']['pdf']['s1 a']    ={'value':    1.34706224e-01, 'min':  -0.5, 'max':     1, 'fixed': False}
conf['params']['pdf']['s1 b']    ={'value':    6.00759596e+00, 'min':     0, 'max':   100, 'fixed': False}

conf['params']['pdf']['sb1 N']   ={'value':    7.46109845e-07, 'min':     0, 'max':     1, 'fixed': False}
conf['params']['pdf']['sb1 a']   ={'value':    3.83495317e-01, 'min':  -0.9, 'max':     1, 'fixed': False}
conf['params']['pdf']['sb1 b']   ={'value':    4.61209808e+00, 'min':     0, 'max':    10, 'fixed': False}

conf['params']['pdf']['sea1 N']  ={'value':    5.71081196e-03, 'min':     0, 'max':     1, 'fixed': False}
conf['params']['pdf']['sea1 a']  ={'value':   -1.36329697e+00, 'min':  -1.9, 'max':    -1, 'fixed': False}
conf['params']['pdf']['sea1 b']  ={'value':    4.74721050e+00, 'min':     0, 'max':   100, 'fixed': False}

conf['params']['pdf']['sea2 N']  ={'value':       2.08640e-02, 'min':     0, 'max':     1, 'fixed': 'sea1 N'}
conf['params']['pdf']['sea2 a']  ={'value':      -1.500000000, 'min':  -1.9, 'max':    -1, 'fixed': 'sea1 a'}
conf['params']['pdf']['sea2 b']  ={'value':       1.00000e+01, 'min':     0, 'max':    20, 'fixed': 'sea1 b'}


#--ht params (NOTE: What's being fitted here is the (M^2/Q^2) and (m^2/Q^2) correction H. To get the correction to FX, take H/Q^2)

conf['params']['ht4']={}

conf['params']['ht4']['F2p N']  ={'value':   0.0,   'min': -30.0,  'max': 30.0, 'fixed':False}
conf['params']['ht4']['F2p a']  ={'value':   1.5,   'min':  0.0,   'max': 4,    'fixed':False}
conf['params']['ht4']['F2p b']  ={'value':   0.0,   'min':  None,  'max': None, 'fixed':True}
conf['params']['ht4']['F2p c']  ={'value':   0.0,   'min': -10.0,  'max': 10,   'fixed':True}
conf['params']['ht4']['F2p d']  ={'value':  -5.0,   'min': -10.0,  'max': -1.0, 'fixed':False}

conf['params']['ht4']['FLp N']  ={'value':   0.0,   'min': -30.0,  'max': 30.0, 'fixed':'F2p N'}
conf['params']['ht4']['FLp a']  ={'value':   1.5,   'min':  0.0,   'max': 4,    'fixed':'F2p a'}
conf['params']['ht4']['FLp b']  ={'value':   0.0,   'min':  None,  'max': None, 'fixed':'F2p b'}
conf['params']['ht4']['FLp c']  ={'value':   0.0,   'min': -10.0,  'max': 10,   'fixed':'F2p c'}
conf['params']['ht4']['FLp d']  ={'value':  -5.0,   'min': -10.0,  'max': -1.0, 'fixed':'F2p d'}

conf['params']['ht4']['F3p N']  ={'value':   0.0,   'min': -30.0,  'max': 30.0, 'fixed':'F2p N'}
conf['params']['ht4']['F3p a']  ={'value':   1.5,   'min':  0.0,   'max': 4,    'fixed':'F2p a'}
conf['params']['ht4']['F3p b']  ={'value':   0.0,   'min':  None,  'max': None, 'fixed':'F2p b'}
conf['params']['ht4']['F3p c']  ={'value':   0.0,   'min': -10.0,  'max': 10,   'fixed':'F2p c'}
conf['params']['ht4']['F3p d']  ={'value':  -5.0,   'min': -10.0,  'max': -1.0, 'fixed':'F2p d'}

#--for p != n
conf['params']['ht4']['F2n N']  ={'value':   0.0,   'min': -30.0,  'max': 30.0, 'fixed':False}
conf['params']['ht4']['F2n a']  ={'value':   1.5,   'min':  0.0,   'max': 4,    'fixed':False}
conf['params']['ht4']['F2n b']  ={'value':   0.0,   'min':  None,  'max': None, 'fixed':True}
conf['params']['ht4']['F2n c']  ={'value':   0.0,   'min': -10.0,  'max': 10,   'fixed':True}
conf['params']['ht4']['F2n d']  ={'value':  -5.0,   'min':  -10.0, 'max': -1.0, 'fixed':False}

conf['params']['ht4']['FLn N']  ={'value':   0.0,   'min': -30.0,  'max': 30.0, 'fixed':'F2n N'}
conf['params']['ht4']['FLn a']  ={'value':   1.5,   'min':  0.0,   'max': 4,    'fixed':'F2n a'}
conf['params']['ht4']['FLn b']  ={'value':   0.0,   'min':  None,  'max': None, 'fixed':'F2n b'}
conf['params']['ht4']['FLn c']  ={'value':   0.0,   'min': -10.0,  'max': 10,   'fixed':'F2n c'}
conf['params']['ht4']['FLn d']  ={'value':  -5.0,   'min':  -10.0, 'max': -1.0, 'fixed':'F2n d'}

#--for p = n
#conf['params']['ht4']['F2n N']  ={'value':   0.0,   'min': -30.0,  'max': 30.0, 'fixed':'F2p N'}
#conf['params']['ht4']['F2n a']  ={'value':   1.5,   'min':  0.0,   'max': 4,    'fixed':'F2p a'}
#conf['params']['ht4']['F2n b']  ={'value':   0.0,   'min':  None,  'max': None, 'fixed':'F2p b'}
#conf['params']['ht4']['F2n c']  ={'value':   0.0,   'min': -10.0,  'max': 10,   'fixed':'F2p c'}
#conf['params']['ht4']['F2n d']  ={'value':  -5.0,   'min':  -10.0, 'max': -1.0, 'fixed':'F2p d'}
#
#conf['params']['ht4']['FLn N']  ={'value':   0.0,   'min': -30.0,  'max': 30.0, 'fixed':'F2p N'}
#conf['params']['ht4']['FLn a']  ={'value':   1.5,   'min':  0.0,   'max': 4,    'fixed':'F2p a'}
#conf['params']['ht4']['FLn b']  ={'value':   0.0,   'min':  None,  'max': None, 'fixed':'F2p b'}
#conf['params']['ht4']['FLn c']  ={'value':   0.0,   'min': -10.0,  'max': 10,   'fixed':'F2p c'}
#conf['params']['ht4']['FLn d']  ={'value':  -5.0,   'min':  -10.0, 'max': -1.0, 'fixed':'F2p d'}

#--offshell paramaterization
conf['params']['off']={}

conf['params']['off']['F2p N']   ={'value':   0.0,   'min': -30.0, 'max': 30,   'fixed':False}
conf['params']['off']['F2p x0']  ={'value':   0.05,  'min': -1.0,  'max': 2.0,  'fixed':False}
conf['params']['off']['F2p x1']  ={'value':   0.0,   'min': None,  'max': None, 'fixed':True}

conf['params']['off']['F2n N']   ={'value':   0.0,   'min': -30.0, 'max': 30,   'fixed':'F2p N'}
conf['params']['off']['F2n x0']  ={'value':   0.05,  'min':  -1.0, 'max': 2.0,  'fixed':'F2p x0'}
conf['params']['off']['F2n x1']  ={'value':   0.0,   'min':  None, 'max': None, 'fixed':'F2p x1'}

#--steps
conf['steps']={}


#------------------------------------------------------------------------------------------------------------------
#--Starting point (W2 cut = 10)
#conf['tmc']   = False
#conf['ht']    = False
#conf['offshell'] = False
#conf['steps'][1]={}
#conf['steps'][1]['dep']=[]
#conf['steps'][1]['active distributions']=['pdf']
#conf['steps'][1]['passive distributions']=[]
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][1]['datasets']={}
#conf['steps'][1]['datasets']['idis']=[]
#conf['steps'][1]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][1]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][1]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][1]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][1]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][1]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC

#------------------------------------------------------------------------------------------------------------------
#--Add HERA (W2 cut = 10)
#conf['tmc']   = False
#conf['ht']    = False
#conf['offshell'] = False
#conf['steps'][2]={}
#conf['steps'][2]['dep']=[1]
#conf['steps'][2]['active distributions']=['pdf']
#conf['steps'][2]['passive distributions']=[]
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][2]['datasets']={}
#conf['steps'][2]['datasets']['idis']=[]
#conf['steps'][2]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][2]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][2]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][2]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][2]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][2]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][2]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][2]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][2]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][2]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][2]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][2]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][2]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-

#------------------------------------------------------------------------------------------------------------------
#--Reduce W2 cut to 4 (W2 cut = 4)
#conf['tmc']   = False
#conf['ht']    = False
#conf['offshell'] = False
#conf['steps'][3]={}
#conf['steps'][3]['dep']=[2]
#conf['steps'][3]['active distributions']=['pdf']
#conf['steps'][3]['passive distributions']=[]
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][3]['datasets']={}
#conf['steps'][3]['datasets']['idis']=[]
#conf['steps'][3]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][3]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][3]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][3]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][3]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][3]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][3]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][3]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][3]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][3]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][3]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][3]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][3]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-

#------------------------------------------------------------------------------------------------------------------
#--Add JLab (W2 cut = 4)
#conf['tmc']   = False
#conf['ht']    = False
#conf['offshell'] = False
#conf['steps'][4]={}
#conf['steps'][4]['dep']=[3]
#conf['steps'][4]['active distributions']=['pdf']
#conf['steps'][4]['passive distributions']=[]
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][4]['datasets']={}
#conf['steps'][4]['datasets']['idis']=[]
#conf['steps'][4]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][4]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][4]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][4]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][4]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][4]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][4]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][4]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][4]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][4]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][4]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][4]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][4]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
#conf['steps'][4]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
#conf['steps'][4]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
#conf['steps'][4]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS

#------------------------------------------------------------------------------------------------------------------
#--Add TMCs
#conf['tmc']   = 'AOT'
#conf['ht']    = False
#conf['offshell'] = False
#conf['steps'][5]={}
#conf['steps'][5]['dep']=[4]
#conf['steps'][5]['active distributions']=['pdf']
#conf['steps'][5]['passive distributions']=[]
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][5]['datasets']={}
#conf['steps'][5]['datasets']['idis']=[]
#conf['steps'][5]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][5]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][5]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][5]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][5]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][5]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][5]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][5]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][5]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][5]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][5]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][5]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][5]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
#conf['steps'][5]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
#conf['steps'][5]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
#conf['steps'][5]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS

#------------------------------------------------------------------------------------------------------------------
#--Add DY
#conf['tmc']   = 'AOT'
#conf['ht']    = False
#conf['offshell'] = False
#conf['steps'][6]={}
#conf['steps'][6]['dep']=[5]
#conf['steps'][6]['active distributions']=['pdf']
#conf['steps'][6]['passive distributions']=[]
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][6]['datasets']={}
#conf['steps'][6]['datasets']['idis']=[]
#conf['steps'][6]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][6]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][6]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][6]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][6]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][6]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][6]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][6]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][6]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][6]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][6]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][6]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][6]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
#conf['steps'][6]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
#conf['steps'][6]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
#conf['steps'][6]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS
#conf['steps'][6]['datasets']['dy']=[]
#conf['steps'][6]['datasets']['dy'].append(10001)
#conf['steps'][6]['datasets']['dy'].append(10002)

#------------------------------------------------------------------------------------------------------------------
#--Add OS++ (uv,dv)
#conf['tmc']   = 'AOT'
#conf['ht']    = False
#conf['offshell'] = False
#conf['params']['pdf']['uv1 c']['zero'] = True
#conf['params']['pdf']['uv1 d']['zero'] = True
#conf['params']['pdf']['dv1 c']['zero'] = True
#conf['params']['pdf']['dv1 d']['zero'] = True
#conf['steps'][7]={}
#conf['steps'][7]['dep']=[6]
#conf['steps'][7]['active distributions']=['pdf']
#conf['steps'][7]['passive distributions']=[]
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][7]['datasets']={}
#conf['steps'][7]['datasets']['idis']=[]
#conf['steps'][7]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][7]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][7]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][7]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][7]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][7]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][7]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][7]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][7]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][7]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][7]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][7]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][7]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
#conf['steps'][7]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
#conf['steps'][7]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
#conf['steps'][7]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS
#conf['steps'][7]['datasets']['dy']=[]
#conf['steps'][7]['datasets']['dy'].append(10001)
#conf['steps'][7]['datasets']['dy'].append(10002)

#------------------------------------------------------------------------------------------------------------------
#--Add OS++ (g)
#conf['tmc']   = 'AOT'
#conf['ht']    = False
#conf['offshell'] = False
#conf['params']['pdf']['g1 c']['zero'] = True
#conf['params']['pdf']['g1 d']['zero'] = True
#conf['steps'][8]={}
#conf['steps'][8]['dep']=[7]
#conf['steps'][8]['active distributions']=['pdf']
#conf['steps'][8]['passive distributions']=[]
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][8]['datasets']={}
#conf['steps'][8]['datasets']['idis']=[]
#conf['steps'][8]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][8]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][8]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][8]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][8]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][8]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][8]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][8]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][8]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][8]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][8]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][8]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][8]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
#conf['steps'][8]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
#conf['steps'][8]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
#conf['steps'][8]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS
#conf['steps'][8]['datasets']['dy']=[]
#conf['steps'][8]['datasets']['dy'].append(10001)
#conf['steps'][8]['datasets']['dy'].append(10002)

#------------------------------------------------------------------------------------------------------------------
#--Add OS++ (ub,db)
#conf['tmc']   = 'AOT'
#conf['ht']    = False
#conf['offshell'] = False
#conf['params']['pdf']['ub1 c']['zero'] = True
#conf['params']['pdf']['ub1 d']['zero'] = True
#conf['params']['pdf']['db1 c']['zero'] = True
#conf['params']['pdf']['db1 d']['zero'] = True
#conf['steps'][9]={}
#conf['steps'][9]['dep']=[8]
#conf['steps'][9]['active distributions']=['pdf']
#conf['steps'][9]['passive distributions']=[]
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][9]['datasets']={}
#conf['steps'][9]['datasets']['idis']=[]
#conf['steps'][9]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][9]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][9]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][9]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][9]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][9]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][9]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][9]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][9]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][9]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][9]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][9]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][9]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
#conf['steps'][9]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
#conf['steps'][9]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
#conf['steps'][9]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS
#conf['steps'][9]['datasets']['dy']=[]
#conf['steps'][9]['datasets']['dy'].append(10001)
#conf['steps'][9]['datasets']['dy'].append(10002)

#------------------------------------------------------------------------------------------------------------------
#--Add Z boson
#conf['tmc']   = 'AOT'
#conf['ht']    = False
#conf['offshell'] = False
#conf['steps'][10]={}
#conf['steps'][10]['dep']=[9]
#conf['steps'][10]['active distributions']=['pdf']
#conf['steps'][10]['passive distributions']=[]
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][10]['datasets']={}
#conf['steps'][10]['datasets']['idis']=[]
#conf['steps'][10]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][10]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][10]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][10]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][10]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][10]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][10]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][10]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][10]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][10]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][10]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][10]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][10]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
#conf['steps'][10]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
#conf['steps'][10]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
#conf['steps'][10]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS
#conf['steps'][10]['datasets']['dy']=[]
#conf['steps'][10]['datasets']['dy'].append(10001)
#conf['steps'][10]['datasets']['dy'].append(10002)
#conf['steps'][10]['datasets']['zrap']=[]
#conf['steps'][10]['datasets']['zrap'].append(1000)
#conf['steps'][10]['datasets']['zrap'].append(1001)

#------------------------------------------------------------------------------------------------------------------
#--Add W boson
#conf['tmc']   = 'AOT'
#conf['ht']    = False
#conf['offshell'] = False
#conf['steps'][11]={}
#conf['steps'][11]['dep']=[10]
#conf['steps'][11]['active distributions']=['pdf']
#conf['steps'][11]['passive distributions']=[]
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][11]['datasets']={}
#conf['steps'][11]['datasets']['idis']=[]
#conf['steps'][11]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][11]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][11]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][11]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][11]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][11]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][11]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][11]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][11]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][11]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][11]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][11]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][11]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
#conf['steps'][11]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
#conf['steps'][11]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
#conf['steps'][11]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS
#conf['steps'][11]['datasets']['dy']=[]
#conf['steps'][11]['datasets']['dy'].append(10001)
#conf['steps'][11]['datasets']['dy'].append(10002)
#conf['steps'][11]['datasets']['zrap']=[]
#conf['steps'][11]['datasets']['zrap'].append(1000)
#conf['steps'][11]['datasets']['zrap'].append(1001)
#conf['steps'][11]['datasets']['wasym']=[]
#conf['steps'][11]['datasets']['wasym'].append(1000)
#conf['steps'][11]['datasets']['wasym'].append(1001)

#--Add ht (mult) (p = n)
#conf['tmc']   = 'AOT'
#conf['ht']    = True
#conf['ht type'] = 'mult'
#conf['offshell'] = False
#conf['steps'][12]={}
#conf['steps'][12]['dep']=[11]
#conf['steps'][12]['active distributions']=['pdf','ht4']
#conf['steps'][12]['passive distributions']=[]
#conf['params']['ht4']['F2p N']['zero'] = True
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][12]['datasets']={}
#conf['steps'][12]['datasets']['idis']=[]
#conf['steps'][12]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][12]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][12]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][12]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][12]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][12]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][12]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][12]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][12]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][12]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][12]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][12]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][12]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
#conf['steps'][12]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
#conf['steps'][12]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
#conf['steps'][12]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS
#conf['steps'][12]['datasets']['dy']=[]
#conf['steps'][12]['datasets']['dy'].append(10001)
#conf['steps'][12]['datasets']['dy'].append(10002)
#conf['steps'][12]['datasets']['zrap']=[]
#conf['steps'][12]['datasets']['zrap'].append(1000)
#conf['steps'][12]['datasets']['zrap'].append(1001)
#conf['steps'][12]['datasets']['wasym']=[]
#conf['steps'][12]['datasets']['wasym'].append(1000)
#conf['steps'][12]['datasets']['wasym'].append(1001)

#--Add ht (mult) (p = n)
#conf['tmc']   = 'AOT'
#conf['ht']    = True
#conf['ht type'] = 'mult'
#conf['offshell'] = False
#conf['steps'][13]={}
#conf['steps'][13]['dep']=[12]
#conf['steps'][13]['active distributions']=['pdf','ht4']
#conf['steps'][13]['passive distributions']=[]
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][13]['datasets']={}
#conf['steps'][13]['datasets']['idis']=[]
#conf['steps'][13]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][13]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][13]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][13]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][13]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][13]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][13]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][13]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][13]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][13]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][13]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][13]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][13]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
#conf['steps'][13]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
#conf['steps'][13]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
#conf['steps'][13]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS
#conf['steps'][13]['datasets']['dy']=[]
#conf['steps'][13]['datasets']['dy'].append(10001)
#conf['steps'][13]['datasets']['dy'].append(10002)
#conf['steps'][13]['datasets']['zrap']=[]
#conf['steps'][13]['datasets']['zrap'].append(1000)
#conf['steps'][13]['datasets']['zrap'].append(1001)
#conf['steps'][13]['datasets']['wasym']=[]
#conf['steps'][13]['datasets']['wasym'].append(1000)
#conf['steps'][13]['datasets']['wasym'].append(1001)
#conf['steps'][13]['datasets']['wzrv']=[]
#conf['steps'][13]['datasets']['wzrv'].append(2000)
#conf['steps'][13]['datasets']['wzrv'].append(2003)
#conf['steps'][13]['datasets']['wzrv'].append(2006)

#--Add LHC
#conf['tmc']   = 'AOT'
#conf['ht']    = True
#conf['ht type'] = 'mult'
#conf['offshell'] = False
#conf['steps'][14]={}
#conf['steps'][14]['dep']=[13]
#conf['steps'][14]['active distributions']=['pdf','ht4']
#conf['steps'][14]['passive distributions']=[]
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][14]['datasets']={}
#conf['steps'][14]['datasets']['idis']=[]
#conf['steps'][14]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][14]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][14]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][14]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][14]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][14]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][14]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][14]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][14]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][14]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][14]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][14]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][14]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
#conf['steps'][14]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
#conf['steps'][14]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
#conf['steps'][14]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS
#conf['steps'][14]['datasets']['dy']=[]
#conf['steps'][14]['datasets']['dy'].append(10001)
#conf['steps'][14]['datasets']['dy'].append(10002)
#conf['steps'][14]['datasets']['zrap']=[]
#conf['steps'][14]['datasets']['zrap'].append(1000)
#conf['steps'][14]['datasets']['zrap'].append(1001)
#conf['steps'][14]['datasets']['wasym']=[]
#conf['steps'][14]['datasets']['wasym'].append(1000)
#conf['steps'][14]['datasets']['wasym'].append(1001)
#conf['steps'][14]['datasets']['wzrv']=[]
#conf['steps'][14]['datasets']['wzrv'].append(2000)
#conf['steps'][14]['datasets']['wzrv'].append(2003)
#conf['steps'][14]['datasets']['wzrv'].append(2006)
#conf['steps'][14]['datasets']['wzrv'].append(2007)
#conf['steps'][14]['datasets']['wzrv'].append(2009)
#conf['steps'][14]['datasets']['wzrv'].append(2010)
#conf['steps'][14]['datasets']['wzrv'].append(2011)
#conf['steps'][14]['datasets']['wzrv'].append(2012)
#conf['steps'][14]['datasets']['wzrv'].append(2013)
#conf['steps'][14]['datasets']['wzrv'].append(2014)
#conf['steps'][14]['datasets']['wzrv'].append(2015)

#--Add offshell
#conf['tmc']   = 'AOT'
#conf['ht']    = True
#conf['ht type'] = 'mult'
#conf['offshell'] = True
#conf['steps'][15]={}
#conf['steps'][15]['dep']=[14]
#conf['steps'][15]['active distributions']=['pdf','ht4','off']
#conf['steps'][15]['passive distributions']=[]
#conf['params']['off']['F2p N']['zero'] = True
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][15]['datasets']={}
#conf['steps'][15]['datasets']['idis']=[]
#conf['steps'][15]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][15]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][15]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][15]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][15]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][15]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][15]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][15]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][15]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][15]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][15]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][15]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][15]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
#conf['steps'][15]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
#conf['steps'][15]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
#conf['steps'][15]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS
#conf['steps'][15]['datasets']['dy']=[]
#conf['steps'][15]['datasets']['dy'].append(10001)
#conf['steps'][15]['datasets']['dy'].append(10002)
#conf['steps'][15]['datasets']['zrap']=[]
#conf['steps'][15]['datasets']['zrap'].append(1000)
#conf['steps'][15]['datasets']['zrap'].append(1001)
#conf['steps'][15]['datasets']['wasym']=[]
#conf['steps'][15]['datasets']['wasym'].append(1000)
#conf['steps'][15]['datasets']['wasym'].append(1001)
#conf['steps'][15]['datasets']['wzrv']=[]
#conf['steps'][15]['datasets']['wzrv'].append(2000)
#conf['steps'][15]['datasets']['wzrv'].append(2003)
#conf['steps'][15]['datasets']['wzrv'].append(2006)
#conf['steps'][15]['datasets']['wzrv'].append(2007)
#conf['steps'][15]['datasets']['wzrv'].append(2009)
#conf['steps'][15]['datasets']['wzrv'].append(2010)
#conf['steps'][15]['datasets']['wzrv'].append(2011)
#conf['steps'][15]['datasets']['wzrv'].append(2012)
#conf['steps'][15]['datasets']['wzrv'].append(2013)
#conf['steps'][15]['datasets']['wzrv'].append(2014)
#conf['steps'][15]['datasets']['wzrv'].append(2015)

#--Remove isospin symmetry for HT
#conf['tmc']   = 'AOT'
#conf['ht']    = True
#conf['ht type'] = 'mult'
#conf['offshell'] = True
#conf['steps'][16]={}
#conf['steps'][16]['dep']=[15]
#conf['steps'][16]['active distributions']=['pdf','ht4','off']
#conf['steps'][16]['passive distributions']=[]
#conf['params']['ht4']['F2n N']['zero'] = True 
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][16]['datasets']={}
#conf['steps'][16]['datasets']['idis']=[]
#conf['steps'][16]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][16]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][16]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][16]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][16]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][16]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][16]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][16]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][16]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][16]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][16]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][16]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][16]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
#conf['steps'][16]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
#conf['steps'][16]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
#conf['steps'][16]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS
#conf['steps'][16]['datasets']['dy']=[]
#conf['steps'][16]['datasets']['dy'].append(10001)
#conf['steps'][16]['datasets']['dy'].append(10002)
#conf['steps'][16]['datasets']['zrap']=[]
#conf['steps'][16]['datasets']['zrap'].append(1000)
#conf['steps'][16]['datasets']['zrap'].append(1001)
#conf['steps'][16]['datasets']['wasym']=[]
#conf['steps'][16]['datasets']['wasym'].append(1000)
#conf['steps'][16]['datasets']['wasym'].append(1001)
#conf['steps'][16]['datasets']['wzrv']=[]
#conf['steps'][16]['datasets']['wzrv'].append(2000)
#conf['steps'][16]['datasets']['wzrv'].append(2003)
#conf['steps'][16]['datasets']['wzrv'].append(2006)
#conf['steps'][16]['datasets']['wzrv'].append(2007)
#conf['steps'][16]['datasets']['wzrv'].append(2009)
#conf['steps'][16]['datasets']['wzrv'].append(2010)
#conf['steps'][16]['datasets']['wzrv'].append(2011)
#conf['steps'][16]['datasets']['wzrv'].append(2012)
#conf['steps'][16]['datasets']['wzrv'].append(2013)
#conf['steps'][16]['datasets']['wzrv'].append(2014)
#conf['steps'][16]['datasets']['wzrv'].append(2015)

#--Add mixture parameters
#conf['tmc']   = 'AOT'
#conf['ht']    = True
#conf['ht type'] = 'mult'
#conf['offshell'] = True
#conf['steps'][17]={}
#conf['steps'][17]['dep']=[16]
#conf['steps'][17]['active distributions']=['pdf','ht4','off']
#conf['steps'][17]['passive distributions']=[]
#conf['params']['pdf']['mix N']['zero'] = True 
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][17]['datasets']={}
#conf['steps'][17]['datasets']['idis']=[]
#conf['steps'][17]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][17]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][17]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][17]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][17]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][17]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][17]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][17]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][17]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][17]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][17]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][17]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][17]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
#conf['steps'][17]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
#conf['steps'][17]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
#conf['steps'][17]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS
#conf['steps'][17]['datasets']['dy']=[]
#conf['steps'][17]['datasets']['dy'].append(10001)
#conf['steps'][17]['datasets']['dy'].append(10002)
#conf['steps'][17]['datasets']['zrap']=[]
#conf['steps'][17]['datasets']['zrap'].append(1000)
#conf['steps'][17]['datasets']['zrap'].append(1001)
#conf['steps'][17]['datasets']['wasym']=[]
#conf['steps'][17]['datasets']['wasym'].append(1000)
#conf['steps'][17]['datasets']['wasym'].append(1001)
#conf['steps'][17]['datasets']['wzrv']=[]
#conf['steps'][17]['datasets']['wzrv'].append(2000)
#conf['steps'][17]['datasets']['wzrv'].append(2003)
#conf['steps'][17]['datasets']['wzrv'].append(2006)
#conf['steps'][17]['datasets']['wzrv'].append(2007)
#conf['steps'][17]['datasets']['wzrv'].append(2009)
#conf['steps'][17]['datasets']['wzrv'].append(2010)
#conf['steps'][17]['datasets']['wzrv'].append(2011)
#conf['steps'][17]['datasets']['wzrv'].append(2012)
#conf['steps'][17]['datasets']['wzrv'].append(2013)
#conf['steps'][17]['datasets']['wzrv'].append(2014)
#conf['steps'][17]['datasets']['wzrv'].append(2015)

#--extend c and d parameter ranges (some hit the limits)
#--also fix small error in smearing function
#conf['tmc']   = 'AOT'
#conf['ht']    = True
#conf['ht type'] = 'mult'
#conf['offshell'] = True
#conf['steps'][18]={}
#conf['steps'][18]['dep']=[17]
#conf['steps'][18]['active distributions']=['pdf','ht4','off']
#conf['steps'][18]['passive distributions']=[]
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][18]['datasets']={}
#conf['steps'][18]['datasets']['idis']=[]
#conf['steps'][18]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][18]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][18]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][18]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][18]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][18]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][18]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][18]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][18]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][18]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][18]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][18]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][18]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
#conf['steps'][18]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
#conf['steps'][18]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
#conf['steps'][18]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS
#conf['steps'][18]['datasets']['dy']=[]
#conf['steps'][18]['datasets']['dy'].append(10001)
#conf['steps'][18]['datasets']['dy'].append(10002)
#conf['steps'][18]['datasets']['zrap']=[]
#conf['steps'][18]['datasets']['zrap'].append(1000)
#conf['steps'][18]['datasets']['zrap'].append(1001)
#conf['steps'][18]['datasets']['wasym']=[]
#conf['steps'][18]['datasets']['wasym'].append(1000)
#conf['steps'][18]['datasets']['wasym'].append(1001)
#conf['steps'][18]['datasets']['wzrv']=[]
#conf['steps'][18]['datasets']['wzrv'].append(2000)
#conf['steps'][18]['datasets']['wzrv'].append(2003)
#conf['steps'][18]['datasets']['wzrv'].append(2006)
#conf['steps'][18]['datasets']['wzrv'].append(2007)
#conf['steps'][18]['datasets']['wzrv'].append(2009)
#conf['steps'][18]['datasets']['wzrv'].append(2010)
#conf['steps'][18]['datasets']['wzrv'].append(2011)
#conf['steps'][18]['datasets']['wzrv'].append(2012)
#conf['steps'][18]['datasets']['wzrv'].append(2013)
#conf['steps'][18]['datasets']['wzrv'].append(2014)
#conf['steps'][18]['datasets']['wzrv'].append(2015)

#--reduce W2 cut to 3.0
#conf['tmc']   = 'AOT'
#conf['ht']    = True
#conf['ht type'] = 'mult'
#conf['offshell'] = True
#conf['steps'][19]={}
#conf['steps'][19]['dep']=[18]
#conf['steps'][19]['active distributions']=['pdf','ht4','off']
#conf['steps'][19]['passive distributions']=[]
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][19]['datasets']={}
#conf['steps'][19]['datasets']['idis']=[]
#conf['steps'][19]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][19]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][19]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][19]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][19]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][19]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][19]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][19]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][19]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][19]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][19]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][19]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][19]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
#conf['steps'][19]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
#conf['steps'][19]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
#conf['steps'][19]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS
#conf['steps'][19]['datasets']['dy']=[]
#conf['steps'][19]['datasets']['dy'].append(10001)
#conf['steps'][19]['datasets']['dy'].append(10002)
#conf['steps'][19]['datasets']['zrap']=[]
#conf['steps'][19]['datasets']['zrap'].append(1000)
#conf['steps'][19]['datasets']['zrap'].append(1001)
#conf['steps'][19]['datasets']['wasym']=[]
#conf['steps'][19]['datasets']['wasym'].append(1000)
#conf['steps'][19]['datasets']['wasym'].append(1001)
#conf['steps'][19]['datasets']['wzrv']=[]
#conf['steps'][19]['datasets']['wzrv'].append(2000)
#conf['steps'][19]['datasets']['wzrv'].append(2003)
#conf['steps'][19]['datasets']['wzrv'].append(2006)
#conf['steps'][19]['datasets']['wzrv'].append(2007)
#conf['steps'][19]['datasets']['wzrv'].append(2009)
#conf['steps'][19]['datasets']['wzrv'].append(2010)
#conf['steps'][19]['datasets']['wzrv'].append(2011)
#conf['steps'][19]['datasets']['wzrv'].append(2012)
#conf['steps'][19]['datasets']['wzrv'].append(2013)
#conf['steps'][19]['datasets']['wzrv'].append(2014)
#conf['steps'][19]['datasets']['wzrv'].append(2015)

#--less restrictive parameter ranges for x0
conf['tmc']   = 'AOT'
conf['ht']    = True
conf['ht type'] = 'mult'
conf['offshell'] = True
conf['steps'][20]={}
conf['steps'][20]['dep']=[19]
conf['steps'][20]['active distributions']=['pdf','ht4','off']
conf['steps'][20]['passive distributions']=[]
conf['params']['off']['F2p N']['zero'] = True
conf['params']['off']['F2p x0']['random'] = True
#------------------------------------------------------------------------------------------------------------------
conf['steps'][20]['datasets']={}
conf['steps'][20]['datasets']['idis']=[]
conf['steps'][20]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
conf['steps'][20]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
conf['steps'][20]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
conf['steps'][20]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
conf['steps'][20]['datasets']['idis'].append(10020) # proton   | F2            | NMC
conf['steps'][20]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
conf['steps'][20]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
conf['steps'][20]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
conf['steps'][20]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
conf['steps'][20]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
conf['steps'][20]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
conf['steps'][20]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
conf['steps'][20]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
conf['steps'][20]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
conf['steps'][20]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
conf['steps'][20]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS
conf['steps'][20]['datasets']['dy']=[]
conf['steps'][20]['datasets']['dy'].append(10001)
conf['steps'][20]['datasets']['dy'].append(10002)
conf['steps'][20]['datasets']['zrap']=[]
conf['steps'][20]['datasets']['zrap'].append(1000)
conf['steps'][20]['datasets']['zrap'].append(1001)
conf['steps'][20]['datasets']['wasym']=[]
conf['steps'][20]['datasets']['wasym'].append(1000)
conf['steps'][20]['datasets']['wasym'].append(1001)
conf['steps'][20]['datasets']['wzrv']=[]
conf['steps'][20]['datasets']['wzrv'].append(2000)
conf['steps'][20]['datasets']['wzrv'].append(2003)
conf['steps'][20]['datasets']['wzrv'].append(2006)
conf['steps'][20]['datasets']['wzrv'].append(2007)
conf['steps'][20]['datasets']['wzrv'].append(2009)
conf['steps'][20]['datasets']['wzrv'].append(2010)
conf['steps'][20]['datasets']['wzrv'].append(2011)
conf['steps'][20]['datasets']['wzrv'].append(2012)
conf['steps'][20]['datasets']['wzrv'].append(2013)
conf['steps'][20]['datasets']['wzrv'].append(2014)
conf['steps'][20]['datasets']['wzrv'].append(2015)






