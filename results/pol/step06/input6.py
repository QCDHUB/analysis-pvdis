conf = {}

## block comment can not appear as this file will be executed by 'exec'
## setup posterior sampling

conf['bootstrap'] = True
conf['flat par'] = False
conf['ftol'] = 1e-8

## setup qcd evolution

conf['alphaSmode'] = 'backward'
conf['order'] = 'NLO'
conf['Q20'] = 1.27 ** 2.0

## setup for idis

conf['tmc'] = False
conf['ht'] = False
conf['nuc'] = True
conf['offshell'] = False
# conf['sidis nuc smearing'] = False
# conf['hq'] = False

## datasets

conf['datasets'] = {}

## cuts

Q2cut = 1.3 ** 2.0
W2cut = 10.0
jet_pt_cut = 10.0 ## pt cut for unpolarized JET dataset
pjet_pt_cut = 10.0 ## pt cut for polarized JET dataset

## IDIS
conf['datasets']['idis'] = {}
conf['datasets']['idis']['filters'] = []
conf['datasets']['idis']['filters'].append("Q2>%f" % Q2cut)
conf['datasets']['idis']['filters'].append("W2>%f" % W2cut)
conf['datasets']['idis']['xlsx'] = {}
conf['datasets']['idis']['xlsx'][10010] = 'idis/expdata/10010.xlsx' # proton   | F2            | SLAC
conf['datasets']['idis']['xlsx'][10011] = 'idis/expdata/10011.xlsx' # deuteron | F2            | SLAC
conf['datasets']['idis']['xlsx'][10016] = 'idis/expdata/10016.xlsx' # proton   | F2            | BCDMS
conf['datasets']['idis']['xlsx'][10017] = 'idis/expdata/10017.xlsx' # deuteron | F2            | BCDMS
conf['datasets']['idis']['xlsx'][10020] = 'idis/expdata/10020.xlsx' # proton   | F2            | NMC
conf['datasets']['idis']['xlsx'][10021] = 'idis/expdata/10021.xlsx' # d/p      | F2d/F2p       | NMC
conf['datasets']['idis']['xlsx'][10026] = 'idis/expdata/10026.xlsx' # proton   | sigma red     | HERA II NC e+ (1)
conf['datasets']['idis']['xlsx'][10027] = 'idis/expdata/10027.xlsx' # proton   | sigma red     | HERA II NC e+ (2)
conf['datasets']['idis']['xlsx'][10028] = 'idis/expdata/10028.xlsx' # proton   | sigma red     | HERA II NC e+ (3)
conf['datasets']['idis']['xlsx'][10029] = 'idis/expdata/10029.xlsx' # proton   | sigma red     | HERA II NC e+ (4)
conf['datasets']['idis']['xlsx'][10030] = 'idis/expdata/10030.xlsx' # proton   | sigma red     | HERA II NC e-
conf['datasets']['idis']['xlsx'][10031] = 'idis/expdata/10031.xlsx' # proton   | sigma red     | HERA II CC e+
conf['datasets']['idis']['xlsx'][10032] = 'idis/expdata/10032.xlsx' # proton   | sigma red     | HERA II NC e-
conf['datasets']['idis']['norm'] = {}
conf['datasets']['idis']['norm'][10010] = {'value': 1, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['idis']['norm'][10011] = {'value': 1, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['idis']['norm'][10016] = {'value': 1, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['idis']['norm'][10017] = {'value': 1, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['idis']['norm'][10020] = {'value': 1, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}

## DY
conf['datasets']['dy'] = {}
conf['datasets']['dy']['filters'] = []
conf['datasets']['dy']['filters'].append("Q2>36")
conf['datasets']['dy']['xlsx'] = {}
conf['datasets']['dy']['xlsx'][10001] = 'dy/expdata/10001.xlsx'
conf['datasets']['dy']['xlsx'][10002] = 'dy/expdata/10002.xlsx'
conf['datasets']['dy']['norm'] = {}
conf['datasets']['dy']['norm'][10001] = {'value': 1, 'fixed': False, 'min': 0.8, 'max': 1.2}
conf['datasets']['dy']['norm'][10002] = {'value': 1, 'fixed': False, 'min': 0.8, 'max': 1.2}

## JET
conf['datasets']['jet'] = {}
conf['datasets']['jet']['filters'] = []
conf['datasets']['jet']['filters'].append("pT>%f" % jet_pt_cut)
conf['datasets']['jet']['xlsx'] = {}
conf['datasets']['jet']['xlsx'][10001] = 'jets/expdata/10001.xlsx' ## D0 dataset
conf['datasets']['jet']['xlsx'][10002] = 'jets/expdata/10002.xlsx' ## CDF dataset
conf['datasets']['jet']['xlsx'][10003] = 'jets/expdata/10003.xlsx' ## STAR MB dataset
conf['datasets']['jet']['xlsx'][10004] = 'jets/expdata/10004.xlsx' ## STAR HT dataset
conf['datasets']['jet']['norm'] = {}
conf['channels'] = {'q_qp': 0, 'q_qbp': 1, 'q_q': 2, 'q_qb': 3, 'q_g': 4, 'g_g': 5}
conf['qr'] = {}
conf['qr']['parameter'] = {'epsilon': 1e-11, 'block_size': 10, 'power_scheme': 1}
conf['jet_qr_fit'] = {'method': 'fixed', 'f_scale': 1.0, 'r_scale': 1.0}
conf['parton_to_hadron'] = False

## PIDIS
conf['datasets']['pidis'] = {}
conf['datasets']['pidis']['filters'] = []
conf['datasets']['pidis']['filters'].append("Q2>%f" % Q2cut)
conf['datasets']['pidis']['filters'].append("W2>%f" % W2cut)
conf['datasets']['pidis']['xlsx'] = {}
## --------------------------------------------------------------------------------------------------------------------------
conf['datasets']['pidis']['xlsx'][10002] = 'pidis/expdata/10002.xlsx' # 10002 | proton   | A1   | COMPASS         |          |
conf['datasets']['pidis']['xlsx'][10003] = 'pidis/expdata/10003.xlsx' # 10003 | proton   | A1   | COMPASS         |          |
conf['datasets']['pidis']['xlsx'][10004] = 'pidis/expdata/10004.xlsx' # 10004 | proton   | A1   | EMC             |          |
conf['datasets']['pidis']['xlsx'][10007] = 'pidis/expdata/10007.xlsx' # 10007 | proton   | Apa  | HERMES          |          |
conf['datasets']['pidis']['xlsx'][10008] = 'pidis/expdata/10008.xlsx' # 10008 | proton   | A2   | HERMES          |          |
conf['datasets']['pidis']['xlsx'][10017] = 'pidis/expdata/10017.xlsx' # 10017 | proton   | Apa  | JLabHB(EG1DVCS) |          |
conf['datasets']['pidis']['xlsx'][10022] = 'pidis/expdata/10022.xlsx' # 10022 | proton   | Apa  | SLAC(E143)      |          |
conf['datasets']['pidis']['xlsx'][10023] = 'pidis/expdata/10023.xlsx' # 10023 | proton   | Ape  | SLAC(E143)      |          |
conf['datasets']['pidis']['xlsx'][10028] = 'pidis/expdata/10028.xlsx' # 10028 | proton   | Ape  | SLAC(E155)      |          |
conf['datasets']['pidis']['xlsx'][10029] = 'pidis/expdata/10029.xlsx' # 10029 | proton   | Apa  | SLAC(E155)      |          |
conf['datasets']['pidis']['xlsx'][10031] = 'pidis/expdata/10031.xlsx' # 10031 | proton   | Atpe | SLAC(E155x)     |          |
conf['datasets']['pidis']['xlsx'][10032] = 'pidis/expdata/10032.xlsx' # 10032 | proton   | Apa  | SLACE80E130     |          |
conf['datasets']['pidis']['xlsx'][10035] = 'pidis/expdata/10035.xlsx' # 10035 | proton   | A1   | SMC             |          |
conf['datasets']['pidis']['xlsx'][10036] = 'pidis/expdata/10036.xlsx' # 10036 | proton   | A1   | SMC             |          |
conf['datasets']['pidis']['xlsx'][10041] = 'pidis/expdata/10041.xlsx' # 10041 | proton   | Apa  | JLabHB(EG1b)    | E =1 GeV |
conf['datasets']['pidis']['xlsx'][10042] = 'pidis/expdata/10042.xlsx' # 10042 | proton   | Apa  | JLabHB(EG1b)    | E =2 GeV |
conf['datasets']['pidis']['xlsx'][10043] = 'pidis/expdata/10043.xlsx' # 10043 | proton   | Apa  | JLabHB(EG1b)    | E =4 GeV |
conf['datasets']['pidis']['xlsx'][10044] = 'pidis/expdata/10044.xlsx' # 10044 | proton   | Apa  | JLabHB(EG1b)    | E =5 GeV |
conf['datasets']['pidis']['xlsx'][10005] = 'pidis/expdata/10005.xlsx' # 10005 | neutron  | A1   | HERMES          |          |
## --------------------------------------------------------------------------------------------------------------------------
conf['datasets']['pidis']['xlsx'][10001] = 'pidis/expdata/10001.xlsx' # 10001 | deuteron | A1   | COMPASS         |          |
conf['datasets']['pidis']['xlsx'][10006] = 'pidis/expdata/10006.xlsx' # 10006 | deuteron | Apa  | HERMES          |          |
conf['datasets']['pidis']['xlsx'][10016] = 'pidis/expdata/10016.xlsx' # 10016 | deuteron | Apa  | JLabHB(EG1DVCS) |          |
conf['datasets']['pidis']['xlsx'][10020] = 'pidis/expdata/10020.xlsx' # 10020 | deuteron | Ape  | SLAC(E143)      |          |
conf['datasets']['pidis']['xlsx'][10021] = 'pidis/expdata/10021.xlsx' # 10021 | deuteron | Apa  | SLAC(E143)      |          |
conf['datasets']['pidis']['xlsx'][10026] = 'pidis/expdata/10026.xlsx' # 10026 | deuteron | Ape  | SLAC(E155)      |          |
conf['datasets']['pidis']['xlsx'][10027] = 'pidis/expdata/10027.xlsx' # 10027 | deuteron | Apa  | SLAC(E155)      |          |
conf['datasets']['pidis']['xlsx'][10030] = 'pidis/expdata/10030.xlsx' # 10030 | deuteron | Atpe | SLAC(E155x)     |          |
conf['datasets']['pidis']['xlsx'][10033] = 'pidis/expdata/10033.xlsx' # 10033 | deuteron | A1   | SMC             |          |
conf['datasets']['pidis']['xlsx'][10034] = 'pidis/expdata/10034.xlsx' # 10034 | deuteron | A1   | SMC             |          |
conf['datasets']['pidis']['xlsx'][10037] = 'pidis/expdata/10037.xlsx' # 10037 | deuteron | Apa  | JLabHB(EG1b)    | E =1 GeV |
conf['datasets']['pidis']['xlsx'][10038] = 'pidis/expdata/10038.xlsx' # 10038 | deuteron | Apa  | JLabHB(EG1b)    | E =2 GeV |
conf['datasets']['pidis']['xlsx'][10039] = 'pidis/expdata/10039.xlsx' # 10039 | deuteron | Apa  | JLabHB(EG1b)    | E =4 GeV |
conf['datasets']['pidis']['xlsx'][10040] = 'pidis/expdata/10040.xlsx' # 10040 | deuteron | Apa  | JLabHB(EG1b)    | E =5 GeV |
## --------------------------------------------------------------------------------------------------------------------------
conf['datasets']['pidis']['norm'] = {}
conf['datasets']['pidis']['norm'][10002] = {'value':    1, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['pidis']['norm'][10003] = {'value':    1, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['pidis']['norm'][10004] = {'value':    1, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['pidis']['norm'][10022] = {'value':    1, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['pidis']['norm'][10023] = {'value':    1, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['pidis']['norm'][10029] = {'value':    1, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['pidis']['norm'][10031] = {'value':    1, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['pidis']['norm'][10041] = {'value':    1, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
##---------------------------------------------------------------------------------------------------------------------------
conf['datasets']['pidis']['norm'][10020] = {'value':    1, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['pidis']['norm'][10021] = {'value':    1, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['pidis']['norm'][10001] = {'value':    1, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['pidis']['norm'][10027] = {'value':    1, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}
conf['datasets']['pidis']['norm'][10030] = {'value':    1, 'min': 8.00000e-01, 'max': 1.20000e+00, 'fixed': False}

## PJET
conf['datasets']['pjet'] = {}
conf['datasets']['pjet']['filters'] = []
conf['datasets']['pjet']['filters'].append("pT>%f" % pjet_pt_cut)
conf['datasets']['pjet']['xlsx'] = {}
conf['datasets']['pjet']['xlsx'][20001] = 'pjets/expdata/20001.xlsx' ## STAR 2006 paper on 2003 and 2004 data
conf['datasets']['pjet']['xlsx'][20002] = 'pjets/expdata/20002.xlsx' ## STAR 2012 paper on 2005 data
conf['datasets']['pjet']['xlsx'][20003] = 'pjets/expdata/20003.xlsx' ## STAR 2012 paper on 2006 data
conf['datasets']['pjet']['xlsx'][20004] = 'pjets/expdata/20004.xlsx' ## STAR 2015 paper on 2009 data
conf['datasets']['pjet']['xlsx'][20005] = 'pjets/expdata/20005.xlsx' ## PHENIX 2011 paper on 2005 data
conf['datasets']['pjet']['xlsx'][20006] = 'pjets/expdata/20006.xlsx' ## STAR 2019 paper on 2012 data
conf['datasets']['pjet']['norm'] = {}
conf['datasets']['pjet']['norm'][20002] = {'value': 1, 'fixed': False, 'min': 0.8, 'max': 1.2}
conf['datasets']['pjet']['norm'][20003] = {'value': 1, 'fixed': False, 'min': 0.8, 'max': 1.2}
conf['datasets']['pjet']['norm'][20004] = {'value': 1, 'fixed': False, 'min': 0.8, 'max': 1.2}
conf['datasets']['pjet']['norm'][20006] = {'value': 1, 'fixed': False, 'min': 0.8, 'max': 1.2}
conf['channels'] = {'q_qp': 0, 'q_qbp': 1, 'q_q': 2, 'q_qb': 3, 'q_g': 4, 'g_g': 5}
conf['qr'] = {}
conf['qr']['parameter'] = {'epsilon': 1e-11, 'block_size': 10, 'power_scheme': 1}
conf['pjet_qr_fit'] = {'method': 'fixed', 'f_scale': 1.0, 'r_scale': 1.0}

## parameters
conf['params'] = {}

## pdf parameters

conf['params']['pdf'] = {}

## first shape of PDF
conf['params']['pdf']['g1 N']    = {'value':    1, 'min':  None, 'max':  None, 'fixed': True }
conf['params']['pdf']['g1 a']    = {'value': -0.5, 'min':  -1.9, 'max':     1, 'fixed': False}
conf['params']['pdf']['g1 b']    = {'value':    6, 'min':     0, 'max':    10, 'fixed': False}
conf['params']['pdf']['g1 c']    = {'value':  0.0, 'min':   -10, 'max':    10, 'fixed': False, 'zero': True}
conf['params']['pdf']['g1 d']    = {'value':  0.0, 'min':   -10, 'max':    10, 'fixed': False, 'zero': True}

conf['params']['pdf']['uv1 N']   = {'value':    1, 'min':  None, 'max':  None, 'fixed': True }
conf['params']['pdf']['uv1 a']   = {'value': -0.5, 'min':  -0.5, 'max':     1, 'fixed': False}
conf['params']['pdf']['uv1 b']   = {'value':    6, 'min':     0, 'max':    10, 'fixed': False}
conf['params']['pdf']['uv1 c']   = {'value':  0.0, 'min':   -10, 'max':    10, 'fixed': False, 'zero': True}
conf['params']['pdf']['uv1 d']   = {'value':  0.0, 'min':   -10, 'max':    10, 'fixed': False, 'zero': True}

conf['params']['pdf']['dv1 N']   = {'value':    1, 'min':  None, 'max':  None, 'fixed': True }
conf['params']['pdf']['dv1 a']   = {'value': -0.5, 'min':  -0.5, 'max':     1, 'fixed': False}
conf['params']['pdf']['dv1 b']   = {'value':    6, 'min':     0, 'max':    10, 'fixed': False}
conf['params']['pdf']['dv1 c']   = {'value':  0.0, 'min':   -10, 'max':    10, 'fixed': False, 'zero': True}
conf['params']['pdf']['dv1 d']   = {'value':  0.0, 'min':   -10, 'max':    10, 'fixed': False, 'zero': True}

conf['params']['pdf']['ub1 N']   = {'value':    1, 'min':     0, 'max':     1, 'fixed': False}
conf['params']['pdf']['ub1 a']   = {'value': -0.5, 'min':    -1, 'max':     1, 'fixed': False}
conf['params']['pdf']['ub1 b']   = {'value':    6, 'min':     0, 'max':    10, 'fixed': False}
conf['params']['pdf']['ub1 c']   = {'value':  0.0, 'min':   -10, 'max':    10, 'fixed': False, 'zero': True}
conf['params']['pdf']['ub1 d']   = {'value':  0.0, 'min':   -10, 'max':    10, 'fixed': False, 'zero': True}

conf['params']['pdf']['db1 N']   = {'value':    1, 'min':     0, 'max':     1, 'fixed': False}
conf['params']['pdf']['db1 a']   = {'value': -0.5, 'min':    -1, 'max':     1, 'fixed': False}
conf['params']['pdf']['db1 b']   = {'value':    6, 'min':     0, 'max':    10, 'fixed': False}
conf['params']['pdf']['db1 c']   = {'value':  0.0, 'min':   -10, 'max':    10, 'fixed': False, 'zero': True}
conf['params']['pdf']['db1 d']   = {'value':  0.0, 'min':   -10, 'max':    10, 'fixed': False, 'zero': True}

conf['params']['pdf']['s1 N']    = {'value':    1, 'min':     0, 'max':     1, 'fixed': True }
conf['params']['pdf']['s1 a']    = {'value':    0, 'min':  -0.5, 'max':     1, 'fixed': False}
conf['params']['pdf']['s1 b']    = {'value':    6, 'min':     0, 'max':    10, 'fixed': False}

conf['params']['pdf']['sb1 N']   = {'value':    1, 'min':     0, 'max':     1, 'fixed': False}
conf['params']['pdf']['sb1 a']   = {'value':    0, 'min':  -0.5, 'max':     1, 'fixed': False}
conf['params']['pdf']['sb1 b']   = {'value':    6, 'min':     0, 'max':    10, 'fixed': False}

conf['params']['pdf']['sea1 N']  = {'value':  0.5, 'min':     0, 'max':     1, 'fixed': False}
conf['params']['pdf']['sea1 a']  = {'value': -1.5, 'min':  -1.9, 'max':    -1, 'fixed': False}
conf['params']['pdf']['sea1 b']  = {'value':    6, 'min':     0, 'max':    10, 'fixed': False}

conf['params']['pdf']['sea2 N']  = {'value':    1, 'min':     0, 'max':     1, 'fixed': 'sea1 N'}
conf['params']['pdf']['sea2 a']  = {'value': -1.5, 'min':  -1.9, 'max':    -1, 'fixed': 'sea1 a'}
conf['params']['pdf']['sea2 b']  = {'value':    6, 'min':     0, 'max':    10, 'fixed': 'sea1 b'}

## ppdf parameters
conf['su2+su3'] = True
conf['ppdf_choice'] = 'plus'
conf['params']['ppdf'] = {}

conf['params']['ppdf']['g1 N']    = {'value':    3.87592e-01, 'min':   -10, 'max':    10, 'fixed': False}
conf['params']['ppdf']['g1 a']    = {'value':   -6.60217e-01, 'min':    -1, 'max':     2, 'fixed': False}
conf['params']['ppdf']['g1 b']    = {'value':    8.12091e+00, 'min':     0, 'max':    10, 'fixed': False}
conf['params']['ppdf']['g1 d']    = {'value':    0.21230e+00, 'min':   -10, 'max':    10, 'fixed': False}

conf['params']['ppdf']['up1 N']   = {'value':    3.47549e-01, 'min':   -10, 'max':    10, 'fixed': True }
conf['params']['ppdf']['up1 a']   = {'value':   -1.14055e-01, 'min':    -1, 'max':     2, 'fixed': False}
conf['params']['ppdf']['up1 b']   = {'value':    3.21230e+00, 'min':     0, 'max':    10, 'fixed': False}
conf['params']['ppdf']['up1 d']   = {'value':    0.21230e+00, 'min':   -10, 'max':    10, 'fixed': False}

conf['params']['ppdf']['dp1 N']   = {'value':    1.52089e-01, 'min':   -10, 'max':    10, 'fixed': True }
conf['params']['ppdf']['dp1 a']   = {'value':   -3.80099e-02, 'min':    -1, 'max':     2, 'fixed': False}
conf['params']['ppdf']['dp1 b']   = {'value':    4.36319e+00, 'min':     0, 'max':    10, 'fixed': False}
conf['params']['ppdf']['dp1 d']   = {'value':    0.36319e+00, 'min':   -10, 'max':    10, 'fixed': False}

conf['params']['ppdf']['sp1 N']   = {'value':    1.52089e-01, 'min':   -10, 'max':    10, 'fixed': False}
conf['params']['ppdf']['sp1 a']   = {'value':   -3.80099e-02, 'min':    -1, 'max':     2, 'fixed': False}
conf['params']['ppdf']['sp1 b']   = {'value':    4.36319e+00, 'min':     0, 'max':    10, 'fixed': False}
conf['params']['ppdf']['sp1 d']   = {'value':    0.36319e+00, 'min':   -10, 'max':    10, 'fixed': False}

# conf['params']['ppdf']['um1 N']   = {'value':    3.47549e-01, 'min':   -10, 'max':    10, 'fixed': False}
# conf['params']['ppdf']['um1 a']   = {'value':   -1.14055e-01, 'min':    -1, 'max':     2, 'fixed': False}
# conf['params']['ppdf']['um1 b']   = {'value':    3.21230e+00, 'min':     0, 'max':    10, 'fixed': False}
# conf['params']['ppdf']['um1 d']   = {'value':    0.21230e+00, 'min':   -10, 'max':    10, 'fixed': False}
# 
# conf['params']['ppdf']['dm1 N']   = {'value':    1.52089e-01, 'min':   -10, 'max':    10, 'fixed': False}
# conf['params']['ppdf']['dm1 a']   = {'value':   -3.80099e-02, 'min':    -1, 'max':     2, 'fixed': False}
# conf['params']['ppdf']['dm1 b']   = {'value':    4.36319e+00, 'min':     0, 'max':    10, 'fixed': False}
# conf['params']['ppdf']['dm1 d']   = {'value':    0.36319e+00, 'min':   -10, 'max':    10, 'fixed': False}
# 
# conf['params']['ppdf']['sm1 N']   = {'value':    1.52089e-01, 'min':   -10, 'max':    10, 'fixed': False}
# conf['params']['ppdf']['sm1 a']   = {'value':   -3.80099e-02, 'min':    -1, 'max':     2, 'fixed': False}
# conf['params']['ppdf']['sm1 b']   = {'value':    4.36319e+00, 'min':     0, 'max':    10, 'fixed': False}
# conf['params']['ppdf']['sm1 d']   = {'value':    0.36319e+00, 'min':   -10, 'max':    10, 'fixed': False}

## steps
conf['steps'] = {}

## DIS without HERA
## fit only first shape of PDF
conf['steps'][1] = {}
conf['steps'][1]['dep'] = []
conf['steps'][1]['active distributions'] = ['pdf']
conf['steps'][1]['passive distributions'] = ['ppdf']
conf['steps'][1]['datasets'] = {}
conf['steps'][1]['datasets']['idis'] = []
conf['steps'][1]['datasets']['idis'].append(10010) ## proton   | F2            | SLAC
conf['steps'][1]['datasets']['idis'].append(10011) ## deuteron | F2            | SLAC
conf['steps'][1]['datasets']['idis'].append(10016) ## proton   | F2            | BCDMS
conf['steps'][1]['datasets']['idis'].append(10017) ## deuteron | F2            | BCDMS
conf['steps'][1]['datasets']['idis'].append(10020) ## proton   | F2            | NMC
conf['steps'][1]['datasets']['idis'].append(10021) ## d/p      | F2d/F2p       | NMC

## DIS with HERA
## fit only first shape of PDF
conf['steps'][2] = {}
conf['steps'][2]['dep'] = [1]
conf['steps'][2]['active distributions'] = ['pdf']
conf['steps'][2]['passive distributions'] = ['ppdf']
conf['steps'][2]['datasets'] = {}
conf['steps'][2]['datasets']['idis'] = []
conf['steps'][2]['datasets']['idis'].append(10010) ## proton   | F2            | SLAC
conf['steps'][2]['datasets']['idis'].append(10011) ## deuteron | F2            | SLAC
conf['steps'][2]['datasets']['idis'].append(10016) ## proton   | F2            | BCDMS
conf['steps'][2]['datasets']['idis'].append(10017) ## deuteron | F2            | BCDMS
conf['steps'][2]['datasets']['idis'].append(10020) ## proton   | F2            | NMC
conf['steps'][2]['datasets']['idis'].append(10021) ## d/p      | F2d/F2p       | NMC
conf['steps'][2]['datasets']['idis'].append(10026) ## proton   | sigma red     | HERA II NC e+ (1)
conf['steps'][2]['datasets']['idis'].append(10027) ## proton   | sigma red     | HERA II NC e+ (2)
conf['steps'][2]['datasets']['idis'].append(10028) ## proton   | sigma red     | HERA II NC e+ (3)
conf['steps'][2]['datasets']['idis'].append(10029) ## proton   | sigma red     | HERA II NC e+ (4)
conf['steps'][2]['datasets']['idis'].append(10030) ## proton   | sigma red     | HERA II NC e-
conf['steps'][2]['datasets']['idis'].append(10031) ## proton   | sigma red     | HERA II CC e+
conf['steps'][2]['datasets']['idis'].append(10032) ## proton   | sigma red     | HERA II NC e-

## DIS
## DY
## fit only first shape of PDF
conf['steps'][3] = {}
conf['steps'][3]['dep'] = [2]
conf['steps'][3]['active distributions'] = ['pdf']
conf['steps'][3]['passive distributions'] = ['ppdf']
conf['steps'][3]['datasets'] = {}
conf['steps'][3]['datasets']['idis'] = []
conf['steps'][3]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
conf['steps'][3]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
conf['steps'][3]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
conf['steps'][3]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
conf['steps'][3]['datasets']['idis'].append(10020) # proton   | F2            | NMC
conf['steps'][3]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
conf['steps'][3]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
conf['steps'][3]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
conf['steps'][3]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
conf['steps'][3]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
conf['steps'][3]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
conf['steps'][3]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
conf['steps'][3]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II NC e-
conf['steps'][3]['datasets']['dy'] = []
conf['steps'][3]['datasets']['dy'].append(10001)
conf['steps'][3]['datasets']['dy'].append(10002)

## DIS with HERA
## DY
## jet Tevatron
## fit only first shape of PDF
conf['steps'][4] = {}
conf['steps'][4]['dep'] = [3]
conf['steps'][4]['active distributions'] = ['pdf']
conf['steps'][4]['passive distributions'] = ['ppdf']
conf['steps'][4]['datasets'] = {}
conf['steps'][4]['datasets']['idis'] = []
conf['steps'][4]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
conf['steps'][4]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
conf['steps'][4]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
conf['steps'][4]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
conf['steps'][4]['datasets']['idis'].append(10020) # proton   | F2            | NMC
conf['steps'][4]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
conf['steps'][4]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
conf['steps'][4]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
conf['steps'][4]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
conf['steps'][4]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
conf['steps'][4]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
conf['steps'][4]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
conf['steps'][4]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II NC e-
conf['steps'][4]['datasets']['dy'] = []
conf['steps'][4]['datasets']['dy'].append(10001)
conf['steps'][4]['datasets']['dy'].append(10002)
conf['steps'][4]['datasets']['jet'] = []
conf['steps'][4]['datasets']['jet'].append(10001) ## D0 dataset
conf['steps'][4]['datasets']['jet'].append(10002) ## CDF dataset

## DIS with HERA
## DY
## jet Tevatron and RHIC
## fit only first shape of PDF
conf['steps'][5] = {}
conf['steps'][5]['dep'] = [4]
conf['steps'][5]['active distributions'] = ['pdf']
conf['steps'][5]['passive distributions'] = ['ppdf']
conf['steps'][5]['datasets'] = {}
conf['steps'][5]['datasets']['idis'] = []
conf['steps'][5]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
conf['steps'][5]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
conf['steps'][5]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
conf['steps'][5]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
conf['steps'][5]['datasets']['idis'].append(10020) # proton   | F2            | NMC
conf['steps'][5]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
conf['steps'][5]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
conf['steps'][5]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
conf['steps'][5]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
conf['steps'][5]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
conf['steps'][5]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
conf['steps'][5]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
conf['steps'][5]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II NC e-
conf['steps'][5]['datasets']['dy'] = []
conf['steps'][5]['datasets']['dy'].append(10001)
conf['steps'][5]['datasets']['dy'].append(10002)
conf['steps'][5]['datasets']['jet'] = []
conf['steps'][5]['datasets']['jet'].append(10001) ## D0 dataset
conf['steps'][5]['datasets']['jet'].append(10002) ## CDF dataset
conf['steps'][5]['datasets']['jet'].append(10003) ## STAR MB dataset
conf['steps'][5]['datasets']['jet'].append(10004) ## STAR HT dataset

## DIS with HERA
## DY
## jet Tevatron and RHIC
## fit only first shape of PDF and fit with parameters c and d
conf['steps'][6] = {}
conf['steps'][6]['dep'] = [5]
conf['steps'][6]['active distributions'] = ['pdf']
conf['steps'][6]['passive distributions'] = ['ppdf']
conf['steps'][6]['datasets'] = {}
conf['steps'][6]['datasets']['idis'] = []
conf['steps'][6]['datasets']['idis'].append(10010) # proton   | F2            | SLAC
conf['steps'][6]['datasets']['idis'].append(10011) # deuteron | F2            | SLAC
conf['steps'][6]['datasets']['idis'].append(10016) # proton   | F2            | BCDMS
conf['steps'][6]['datasets']['idis'].append(10017) # deuteron | F2            | BCDMS
conf['steps'][6]['datasets']['idis'].append(10020) # proton   | F2            | NMC
conf['steps'][6]['datasets']['idis'].append(10021) # d/p      | F2d/F2p       | NMC
conf['steps'][6]['datasets']['idis'].append(10026) # proton   | sigma red     | HERA II NC e+ (1)
conf['steps'][6]['datasets']['idis'].append(10027) # proton   | sigma red     | HERA II NC e+ (2)
conf['steps'][6]['datasets']['idis'].append(10028) # proton   | sigma red     | HERA II NC e+ (3)
conf['steps'][6]['datasets']['idis'].append(10029) # proton   | sigma red     | HERA II NC e+ (4)
conf['steps'][6]['datasets']['idis'].append(10030) # proton   | sigma red     | HERA II NC e-
conf['steps'][6]['datasets']['idis'].append(10031) # proton   | sigma red     | HERA II CC e+
conf['steps'][6]['datasets']['idis'].append(10032) # proton   | sigma red     | HERA II NC e-
conf['steps'][6]['datasets']['dy'] = []
conf['steps'][6]['datasets']['dy'].append(10001)
conf['steps'][6]['datasets']['dy'].append(10002)
conf['steps'][6]['datasets']['jet'] = []
conf['steps'][6]['datasets']['jet'].append(10001) ## D0 dataset
conf['steps'][6]['datasets']['jet'].append(10002) ## CDF dataset
conf['steps'][6]['datasets']['jet'].append(10003) ## STAR MB dataset
conf['steps'][6]['datasets']['jet'].append(10004) ## STAR HT dataset
