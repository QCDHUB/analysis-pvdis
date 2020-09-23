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
conf['datasets']['idis']['xlsx'][90001]='idis/expdata/90001.xlsx' # proton   | A_PV_e        | JAM4EIC (optimistic)
conf['datasets']['idis']['xlsx'][90002]='idis/expdata/90002.xlsx' # deuteron | A_PV_e        | JAM4EIC (optimistic)
conf['datasets']['idis']['xlsx'][90011]='idis/expdata/90011.xlsx' # proton   | A_PV_e        | JAM4EIC (moderate)
conf['datasets']['idis']['xlsx'][90012]='idis/expdata/90012.xlsx' # deuteron | A_PV_e        | JAM4EIC (moderate)
#conf['datasets']['idis']['xlsx'][90021]='idis/expdata/90021.xlsx' # proton   | A_PV_e        | JAM4EIC (pessimistic)
#conf['datasets']['idis']['xlsx'][90022]='idis/expdata/90022.xlsx' # deuteron | A_PV_e        | JAM4EIC (pessimistic)
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

#--weak mixing angle
conf['params']['eweak'] = {}
conf['params']['eweak']['s2wMZ']  ={'value':   0.23116,   'min':  0.0, 'max': 1.0, 'fixed':False}


#--steps
conf['steps']={}

#--less restrictive parameter ranges for x0
#conf['tmc']   = 'AOT'
#conf['ht']    = True
#conf['ht type'] = 'mult'
#conf['offshell'] = True
#conf['steps'][20]={}
#conf['steps'][20]['dep']=[19]
#conf['steps'][20]['active distributions']=['pdf','ht4','off']
#conf['steps'][20]['passive distributions']=[]
#conf['params']['off']['F2p N']['zero'] = True
#conf['params']['off']['F2p x0']['random'] = True
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][20]['datasets']={}
#conf['steps'][20]['datasets']['idis']=[]
#conf['steps'][20]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][20]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][20]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][20]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][20]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][20]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][20]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][20]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][20]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][20]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][20]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][20]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][20]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
#conf['steps'][20]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
#conf['steps'][20]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
#conf['steps'][20]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS
#conf['steps'][20]['datasets']['dy']=[]
#conf['steps'][20]['datasets']['dy'].append(10001)
#conf['steps'][20]['datasets']['dy'].append(10002)
#conf['steps'][20]['datasets']['zrap']=[]
#conf['steps'][20]['datasets']['zrap'].append(1000)
#conf['steps'][20]['datasets']['zrap'].append(1001)
#conf['steps'][20]['datasets']['wasym']=[]
#conf['steps'][20]['datasets']['wasym'].append(1000)
#conf['steps'][20]['datasets']['wasym'].append(1001)
#conf['steps'][20]['datasets']['wzrv']=[]
#conf['steps'][20]['datasets']['wzrv'].append(2000)
#conf['steps'][20]['datasets']['wzrv'].append(2003)
#conf['steps'][20]['datasets']['wzrv'].append(2006)
#conf['steps'][20]['datasets']['wzrv'].append(2007)
#conf['steps'][20]['datasets']['wzrv'].append(2009)
#conf['steps'][20]['datasets']['wzrv'].append(2010)
#conf['steps'][20]['datasets']['wzrv'].append(2011)
#conf['steps'][20]['datasets']['wzrv'].append(2012)
#conf['steps'][20]['datasets']['wzrv'].append(2013)
#conf['steps'][20]['datasets']['wzrv'].append(2014)
#conf['steps'][20]['datasets']['wzrv'].append(2015)


#--fit weak mixing angle w/ PDFs fixed
#conf['tmc']   = 'AOT'
#conf['ht']    = True
#conf['ht type'] = 'mult'
#conf['offshell'] = True
#conf['steps'][21]={}
#conf['steps'][21]['dep']=[20]
#conf['steps'][21]['active distributions']=['eweak']
#conf['steps'][21]['passive distributions']=['pdf','ht4','off']
##------------------------------------------------------------------------------------------------------------------
#conf['steps'][21]['datasets']={}
#conf['steps'][21]['datasets']['idis']=[]
#conf['steps'][21]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
#conf['steps'][21]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
#conf['steps'][21]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
#conf['steps'][21]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
#conf['steps'][21]['datasets']['idis'].append(10020) # proton   | F2            | NMC
#conf['steps'][21]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
#conf['steps'][21]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
#conf['steps'][21]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
#conf['steps'][21]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
#conf['steps'][21]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
#conf['steps'][21]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
#conf['steps'][21]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
#conf['steps'][21]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
#conf['steps'][21]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
#conf['steps'][21]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
#conf['steps'][21]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS

#--fit weak mixing angle and PDFs (with optimistic EIC)
conf['tmc']   = 'AOT'
conf['ht']    = True
conf['ht type'] = 'mult'
conf['offshell'] = True
conf['steps'][22]={}
conf['steps'][22]['dep']=[20,21]
conf['steps'][22]['active distributions']=['pdf','ht4','off','eweak']
conf['steps'][22]['passive distributions']=[]
#------------------------------------------------------------------------------------------------------------------
conf['steps'][22]['datasets']={}
conf['steps'][22]['datasets']['idis']=[]
conf['steps'][22]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
conf['steps'][22]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
conf['steps'][22]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
conf['steps'][22]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
conf['steps'][22]['datasets']['idis'].append(10020) # proton   | F2            | NMC
conf['steps'][22]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
conf['steps'][22]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
conf['steps'][22]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
conf['steps'][22]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
conf['steps'][22]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
conf['steps'][22]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
conf['steps'][22]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
conf['steps'][22]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II CC e-
conf['steps'][22]['datasets']['idis'].append(10002) # deuteron | F2            | JLab Hall C (E00-106)
conf['steps'][22]['datasets']['idis'].append(10003) # proton   | F2            | JLab Hall C (E00-106)
conf['steps'][22]['datasets']['idis'].append(10033) # n/d      | F2n/F2d       | BONUS
conf['steps'][22]['datasets']['idis'].append(90001) 
conf['steps'][22]['datasets']['idis'].append(90002) 
conf['steps'][22]['datasets']['dy']=[]
conf['steps'][22]['datasets']['dy'].append(10001)
conf['steps'][22]['datasets']['dy'].append(10002)
conf['steps'][22]['datasets']['zrap']=[]
conf['steps'][22]['datasets']['zrap'].append(1000)
conf['steps'][22]['datasets']['zrap'].append(1001)
conf['steps'][22]['datasets']['wasym']=[]
conf['steps'][22]['datasets']['wasym'].append(1000)
conf['steps'][22]['datasets']['wasym'].append(1001)
conf['steps'][22]['datasets']['wzrv']=[]
conf['steps'][22]['datasets']['wzrv'].append(2000)
conf['steps'][22]['datasets']['wzrv'].append(2003)
conf['steps'][22]['datasets']['wzrv'].append(2006)
conf['steps'][22]['datasets']['wzrv'].append(2007)
conf['steps'][22]['datasets']['wzrv'].append(2009)
conf['steps'][22]['datasets']['wzrv'].append(2010)
conf['steps'][22]['datasets']['wzrv'].append(2011)
conf['steps'][22]['datasets']['wzrv'].append(2012)
conf['steps'][22]['datasets']['wzrv'].append(2013)
conf['steps'][22]['datasets']['wzrv'].append(2014)
conf['steps'][22]['datasets']['wzrv'].append(2015)



