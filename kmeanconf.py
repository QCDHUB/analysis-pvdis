def _hook_db1(params,order):
    sample=[]

    for i in range(len(order)):
        if order[i][0]!=1: continue
        if order[i][1]!='pdf': continue
        if 'g1'  in order[i][2]: continue 
        if 'uv1' in order[i][2]: continue 
        if 'dv1' in order[i][2]: continue 
        #if 'db1' in order[i][2]: continue 
        if 'ub1' in order[i][2]: continue 
        if 's1' in order[i][2]: continue 
        if 'sb1' in order[i][2]: continue
        if 'sea1' in order[i][2]: continue
        if 'sea1' in order[i][2]: continue

        #if order[i][2].split()[1]=='N': continue
        #if order[i][2].split()[1]=='a': continue
        #if order[i][2].split()[1]=='b': continue
        #if order[i][2].split()[1]=='c': continue
        #if order[i][2].split()[1]=='d': continue
        #print (order[i][2], params[i])
        sample.append(params[i])
    return sample

def _hook_off(params,order):
    sample=[]

    for i in range(len(order)):
        if order[i][0]!=1: continue
        if order[i][1]!='off': continue
        sample.append(params[i])
    return sample


nc={}
hooks={}

#for i in range(100):
#  nc[i+1]=1
#  hooks[i+1]=None

nc[1] = 1
hooks[1] = None
nc[2] = 1
hooks[2] = None
nc[3] = 1
hooks[3] = None
nc[4] = 1
hooks[4] = None
nc[5] = 1
hooks[5] = None
nc[6] = 1
hooks[6] = None
nc[7] = 1
hooks[7] = None
nc[8] = 1
hooks[8] = None
nc[9] = 1
hooks[9] = None
nc[10] = 1
hooks[10] = None
nc[11] = 1
hooks[11] = None
nc[12] = 1
hooks[12] = None
nc[13] = 1
hooks[13] = None
nc[14] = 1
hooks[14] = None
nc[15] = 1
hooks[15] = None
nc[16] = 1
hooks[16] = None
nc[17] = 1
hooks[17] = None
nc[18] = 1
hooks[18] = None
nc[19] = 1
hooks[19] = None
nc[20] = 1
hooks[20] = None
nc[21] = 1
hooks[21] = None
nc[22] = 1
hooks[22] = None
nc[23] = 1
hooks[23] = None
nc[24] = 1
hooks[24] = None











