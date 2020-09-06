import sys,os
import numpy as np
import copy

#--matplotlib
import matplotlib
matplotlib.use('Agg')
import pylab as py

#--from scipy stack 
from scipy.integrate import fixed_quad
from scipy import interpolate

#--from tools
from tools.tools     import load,save,checkdir,lprint
from tools.config    import conf,load_config

#--from fitlib
from fitlib.resman import RESMAN

#-- from qcdlib
from qcdlib import aux

#--from local
from analysis.corelib import core
from analysis.corelib import classifier

#--from obslib
from obslib.idis.reader import READER

def plot_pvdis_e(wdir,kc):

    #--estimations:
    #--'opt':  optimistic datasets  (90001 and 90002)
    #--'mod':  moderate datasets    (90011 and 90012)
    #--'pes': pessimistic datasets  (90021 and 90022)

    print('\ngenerating PVDIS (electron) asymmetry from %s'%(wdir))
    load_config('%s/input.py'%wdir)
    istep=core.get_istep()
    predictions = load('%s/data/predictions-%d.dat'%(wdir,istep))
    if 'idis' not in predictions['reactions']: return

    nrows,ncols=1,1
    fig = py.figure(figsize=(ncols*7,nrows*4))
    ax11 = py.subplot(nrows,ncols,1)

    conf['aux']=aux.AUX()
    conf['datasets'] = {}
    conf['datasets']['idis']={}
    conf['datasets']['idis']['xlsx']={}

    #--optimistic
    conf['datasets']['idis']['xlsx'][90001]='idis/expdata/90001.xlsx'
    conf['datasets']['idis']['xlsx'][90002]='idis/expdata/90002.xlsx'
    #--moderate
    conf['datasets']['idis']['xlsx'][90011]='idis/expdata/90011.xlsx'
    conf['datasets']['idis']['xlsx'][90012]='idis/expdata/90012.xlsx'
    #--pessimistic
    #conf['datasets']['idis']['xlsx'][90021]='idis/expdata/90021.xlsx'
    #conf['datasets']['idis']['xlsx'][90022]='idis/expdata/90022.xlsx'

    conf['datasets']['idis']['norm']={}
    conf['datasets']['idis']['filters']=[]
    conf['idis tabs']=READER().load_data_sets('idis')
    tables = conf['idis tabs'].keys()

    replicas=core.get_replicas(wdir)
    core.mod_conf(istep,replicas[0]) #--set conf as specified in istep   
   
    resman=RESMAN(nworkers=1,parallel=False,datasets=False)   #conf['pdf'] comes from this line!!!
    parman=resman.parman

    jar=load('%s/data/jar-%d.dat'%(wdir,istep))
    replicas=jar['replicas']
    parman.order=jar['order']

    data = predictions['reactions']['idis']

    cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc)

    for idx in data:
        predictions = copy.copy(data[idx]['prediction-rep'])
        del data[idx]['prediction-rep']
        del data[idx]['residuals-rep']
        for ic in range(kc.nc[istep]):
            predictions_ic = [predictions[i] for i in range(len(predictions)) if cluster[i] == ic]
            data[idx]['thy-%d' % ic] = np.mean(predictions_ic, axis = 0)
            data[idx]['dthy-%d' % ic] = np.std(predictions_ic, axis = 0)

    if 90001 in data.keys(): idxs,est = [90001,90002],'opt'
    if 90011 in data.keys(): idxs,est = [90011,90012],'mod'
    if 90021 in data.keys(): idxs,est = [90021,90022],'pes'

    hand = {}
    #--plot data
    for idx in idxs:
        if idx in [90001,90011,90021]: color,fmt = 'firebrick' , 'o'
        if idx in [90002,90012,90022]: color,fmt = 'darkgreen' , '^'
        x  = conf['idis tabs'][idx]['X']
        q2 = conf['idis tabs'][idx]['Q2']
        values = conf['idis tabs'][idx]['value']
        alpha  = data[idx]['alpha']
        #--mean and standard deviation of replicas      
        theory  = data[idx]['thy-0']
        dtheory = data[idx]['dthy-0']
        l = len(values)
        #--get fixed values for Q2
        Q2 = []
        for j in range(len(q2)):
            if q2[j] in Q2: continue
            Q2.append(q2[j])
        #--get corresponding x, asymmetry values
        for j in range(len(Q2)):
            X, val, alp, thy, dthy = [],[],[],[],[]
            for i in range(l):
                if q2[i] != Q2[j]: continue
                X   .append(x[i])
                val .append(values[i])
                alp .append(alpha[i])
                thy .append(theory[i])
                dthy.append(dtheory[i])

            hand[idx] = ax11.errorbar(X,np.abs(val),yerr=alp,color=color,fmt=fmt,ms=3.0)
            thy_plot ,= ax11.plot(X,thy,color='black',alpha=1.0)
            down = np.array(thy) - np.array(dthy)
            up   = np.array(thy) + np.array(dthy)
            thy_band  = ax11.fill_between(X,down,up,color='gold',alpha=1.0)

    ax11.set_xlabel(r'$x$',size=30)
    ax11.set_xlim(2e-5,1)
    ax11.set_ylim(1e-4,1)
    ax11.semilogx()
    ax11.semilogy()
    ax11.text(0.03,0.03,r'$Q^2=%s$'%np.round(Q2[0],1) + ' ' + r'\textrm{GeV}' + r'$^2$',transform=ax11.transAxes,size=16)
    ax11.text(0.15,0.12,r'$Q^2=%s$'%np.round(Q2[1],1)                                  ,transform=ax11.transAxes,size=16)
    ax11.text(0.25,0.21,r'$Q^2=%s$'%np.round(Q2[2],1)                                  ,transform=ax11.transAxes,size=16)
    ax11.text(0.30,0.31,r'$Q^2=%s$'%np.round(Q2[3],1)                                  ,transform=ax11.transAxes,size=16)
    ax11.text(0.40,0.42,r'$Q^2=%s$'%np.round(Q2[4],1)                                  ,transform=ax11.transAxes,size=16)
    ax11.text(0.50,0.52,r'$Q^2=%s$'%np.round(Q2[5],1)                                  ,transform=ax11.transAxes,size=16)
    ax11.text(0.55,0.61,r'$Q^2=%s$'%np.round(Q2[6],1)                                  ,transform=ax11.transAxes,size=16)
    ax11.text(0.65,0.71,r'$Q^2=%s$'%np.round(Q2[7],1)                                  ,transform=ax11.transAxes,size=16)
    ax11.text(0.70,0.81,r'$Q^2=%s$'%np.round(Q2[8],1)                                  ,transform=ax11.transAxes,size=16)

    if est == 'opt': ax11.text(0.4,0.9,r'\textrm{Optimistic}' ,transform=ax11.transAxes,size=20)
    if est == 'mod': ax11.text(0.4,0.9,r'\textrm{Moderate}'   ,transform=ax11.transAxes,size=20)
    if est == 'pes': ax11.text(0.4,0.9,r'\textrm{Pessimistic}',transform=ax11.transAxes,size=20)

    ax11.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=20)

    if est == 'opt': handles = [(thy_band,thy_plot),hand[90001],hand[90002]]
    if est == 'mod': handles = [(thy_band,thy_plot),hand[90011],hand[90012]]
    if est == 'pes': handles = [(thy_band,thy_plot),hand[90021],hand[90022]]
    label1  = r'\textbf{\textrm{JAM}}'
    label2  = r'\textbf{\textrm{JAM4EIC(p)}}'
    label3  = r'\textbf{\textrm{JAM4EIC(d)}}'
    labels  = [label1,label2,label3]
    ax11.legend(handles,labels,loc='upper left', fontsize = 20, frameon = 0, handletextpad = 0.3, handlelength = 1.0)
    ax11.set_ylabel(r'$A_{PV}^e$',size=30)

    py.tight_layout()
    checkdir('%s/gallery'%wdir)
    filename='%s/gallery/pvdis_e.png'%(wdir)

    py.savefig(filename)
    print
    print 'Saving PV asymmetry plot to %s'%filename

def plot_pvdis_e_ratio(wdir,kc,kind='opt'):

    print('\ngenerating PVDIS (electron) asymmetry ratio from %s'%(wdir))
    load_config('%s/input.py'%wdir)
    istep=core.get_istep()
    predictions = load('%s/data/predictions-%d.dat'%(wdir,istep))
    if 'idis' not in predictions['reactions']: return

    nrows,ncols=6,3
    fig = py.figure(figsize=(ncols*12,nrows*3))
    ax11 = py.subplot(nrows,ncols,1)
    ax12 = py.subplot(nrows,ncols,2)
    ax13 = py.subplot(nrows,ncols,3)
    ax21 = py.subplot(nrows,ncols,4)
    ax22 = py.subplot(nrows,ncols,5)
    ax23 = py.subplot(nrows,ncols,6)
    ax31 = py.subplot(nrows,ncols,7)
    ax32 = py.subplot(nrows,ncols,8)
    ax33 = py.subplot(nrows,ncols,9)
    ax41 = py.subplot(nrows,ncols,10)
    ax42 = py.subplot(nrows,ncols,11)
    ax43 = py.subplot(nrows,ncols,12)
    ax51 = py.subplot(nrows,ncols,13)
    ax52 = py.subplot(nrows,ncols,14)
    ax53 = py.subplot(nrows,ncols,15)
    ax61 = py.subplot(nrows,ncols,16)
    ax62 = py.subplot(nrows,ncols,17)
    ax63 = py.subplot(nrows,ncols,18)

    if kind == 'opt':  idx1,idx2 = 90001,90002
    if kind == 'mod':  idx1,idx2 = 90011,90012
    if kind == 'pess': idx1,idx2 = 90021,90022

    conf['aux']=aux.AUX()
    conf['datasets'] = {}
    conf['datasets']['idis']={}
    conf['datasets']['idis']['xlsx']={}
    conf['datasets']['idis']['xlsx'][idx1]='idis/expdata/%s.xlsx'%idx1
    conf['datasets']['idis']['xlsx'][idx2]='idis/expdata/%s.xlsx'%idx2
    conf['datasets']['idis']['norm']={}
    conf['datasets']['idis']['filters']=[]
    conf['idis tabs']=READER().load_data_sets('idis')
    tables = conf['idis tabs'].keys()

    replicas=core.get_replicas(wdir)
    core.mod_conf(istep,replicas[0]) #--set conf as specified in istep   
   
    resman=RESMAN(nworkers=1,parallel=False,datasets=False)   #conf['pdf'] comes from this line!!!
    parman=resman.parman

    jar=load('%s/data/jar-%d.dat'%(wdir,istep))
    replicas=jar['replicas']
    parman.order=jar['order']

    data = predictions['reactions']['idis']

    cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc)

    #--get theory by seperating solutions and taking mean
    for idx in tables:
        predictions = copy.copy(data[idx]['prediction-rep'])
        del data[idx]['prediction-rep']
        del data[idx]['residuals-rep']
        for ic in range(nc):
            predictions_ic = [predictions[i] for i in range(len(predictions)) if cluster[i] == ic]
            data[idx]['thy-%d'%ic]  = np.mean(predictions_ic, axis = 0)
            data[idx]['dthy-%d'%ic] = np.std(predictions_ic, axis=0)**0.5

    Q2 = {}
    for idx in tables:
        x      = conf['idis tabs'][idx]['X']
        q2     = conf['idis tabs'][idx]['Q2']
        values = conf['idis tabs'][idx]['value']
        alpha  = data[idx]['alpha']
        l = len(values)
        theory=data[idx]['thy-0']
        #--get fixed values for Q2
        Q2[idx] = []
        for j in range(len(q2)):
            if q2[j] in Q2[idx]: continue
            Q2[idx].append(q2[j])
        #--get corresponding x, theory values
        X, thy, val, alp = {}, {}, {}, {}
        for j in range(len(Q2[idx])):
            X[j], thy[j], val[j], alp[j] = [],[],[],[]
            for i in range(l):
                if q2[i] != Q2[idx][j]: continue
                X[j].append(x[i])
                thy[j].append(theory[i])
                val[j].append(values[i])
                alp[j].append(alpha[i])
        for j in range(len(Q2[idx])):
            if j==0 and idx in [90001,90011,90021]: ax=ax11
            if j==1 and idx in [90001,90011,90021]: ax=ax12
            if j==2 and idx in [90001,90011,90021]: ax=ax13
            if j==3 and idx in [90001,90011,90021]: ax=ax21
            if j==4 and idx in [90001,90011,90021]: ax=ax22
            if j==5 and idx in [90001,90011,90021]: ax=ax23
            if j==6 and idx in [90001,90011,90021]: ax=ax31
            if j==7 and idx in [90001,90011,90021]: ax=ax32
            if j==8 and idx in [90001,90011,90021]: ax=ax33

            if j==0 and idx in [90002,90012,90022]: ax=ax41
            if j==1 and idx in [90002,90012,90022]: ax=ax42
            if j==2 and idx in [90002,90012,90022]: ax=ax43
            if j==3 and idx in [90002,90012,90022]: ax=ax51
            if j==4 and idx in [90002,90012,90022]: ax=ax52
            if j==5 and idx in [90002,90012,90022]: ax=ax53
            if j==6 and idx in [90002,90012,90022]: ax=ax61
            if j==7 and idx in [90002,90012,90022]: ax=ax62
            if j==8 and idx in [90002,90012,90022]: ax=ax63

            ratio = np.array(val[j])/np.array(thy[j])
            yerr  = np.array(alp[j])/np.array(val[j])
            #ax.errorbar(X[j],np.ones(len(X[j])),yerr=np.array(alp[j])/np.array(val[j]),color='black',fmt='o',ms=3.0)
            #ax.plot(X[j],ratio,color=color,alpha=0.5)
            ax.errorbar(X[j],ratio,yerr=yerr,color='red',fmt='.',ms=10)

    for ax in [ax11,ax12,ax13,ax21,ax22,ax23,ax31,ax32,ax33,ax41,ax42,ax43,ax51,ax52,ax53,ax61,ax62,ax63]:
        ax.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=20)
        ax.semilogx()
        ax.axhline(1,0,1,ls='--',color='black',alpha=0.5)
        ax.set_ylim(0.97,1.03)
        ax.set_xlim(3e-4,0.7)

    #ax11.set_ylim(0.97,1.03)
    #ax12.set_ylim(0.99,1.01)
    #ax13.set_ylim(0.994,1.006)
    #ax14.set_ylim(0.9975,1.0025)
    #ax15.set_ylim(0.999,1.001)
    #ax21.set_ylim(0.999,1.001)
    #ax22.set_ylim(0.999,1.001)
    #ax23.set_ylim(0.999,1.001)
    #ax24.set_ylim(0.999,1.001)

    ax61.set_xlabel(r'$x$',size=24)
    ax62.set_xlabel(r'$x$',size=24)
    ax63.set_xlabel(r'$x$',size=24)
    ax11.set_ylabel(r'$data/theory$',size=24)
    ax21.set_ylabel(r'$data/theory$',size=24)


    ax11.text(0.05,0.9,r'$Q^2=%s$'%np.round(Q2[90001][0],1),transform=ax11.transAxes,size=30)
    ax12.text(0.05,0.9,r'$Q^2=%s$'%np.round(Q2[90001][1],1),transform=ax12.transAxes,size=30)
    ax13.text(0.05,0.9,r'$Q^2=%s$'%np.round(Q2[90001][2],1),transform=ax13.transAxes,size=30)
    ax21.text(0.05,0.9,r'$Q^2=%s$'%np.round(Q2[90001][3],1),transform=ax21.transAxes,size=30)
    ax22.text(0.05,0.9,r'$Q^2=%s$'%np.round(Q2[90001][4],1),transform=ax22.transAxes,size=30)
    ax23.text(0.05,0.9,r'$Q^2=%s$'%np.round(Q2[90001][5],1),transform=ax23.transAxes,size=30)
    ax31.text(0.05,0.9,r'$Q^2=%s$'%np.round(Q2[90001][6],1),transform=ax31.transAxes,size=30)
    ax32.text(0.05,0.9,r'$Q^2=%s$'%np.round(Q2[90001][7],1),transform=ax32.transAxes,size=30)
    ax33.text(0.05,0.9,r'$Q^2=%s$'%np.round(Q2[90001][8],1),transform=ax33.transAxes,size=30)

    py.tight_layout()
    checkdir('%s/gallery'%wdir)
    filename='%s/gallery/pvdis_e_ratio.png'%(wdir)

    py.savefig(filename)
    print
    print 'Saving PV (electron) asymmetry ratio plot to %s'%filename

def plot_pvdis_had(wdir,kc):

    #--estimations:
    #--'opt':  optimistic datasets  (90001)
    #--'mod':  moderate datasets    (90011)
    #--'pes': pessimistic datasets  (90021)

    print('\ngenerating PVDIS (hadron) asymmetry from %s'%(wdir))
    load_config('%s/input.py'%wdir)
    istep=core.get_istep()
    predictions = load('%s/data/predictions-%d.dat'%(wdir,istep))
    if 'idis' not in predictions['reactions']: return

    nrows,ncols=1,1
    fig = py.figure(figsize=(ncols*7,nrows*4))
    ax11 = py.subplot(nrows,ncols,1)

    conf['aux']=aux.AUX()
    conf['datasets'] = {}
    conf['datasets']['pidis']={}
    conf['datasets']['pidis']['xlsx']={}

    #--optimistic
    conf['datasets']['pidis']['xlsx'][90001]='pidis/expdata/90001.xlsx'
    #--moderate
    conf['datasets']['pidis']['xlsx'][90011]='pidis/expdata/90011.xlsx'
    #--pessimistic
    #conf['datasets']['pidis']['xlsx'][90021]='pidis/expdata/90021.xlsx'

    conf['datasets']['pidis']['norm']={}
    conf['datasets']['pidis']['filters']=[]
    conf['pidis tabs']=READER().load_data_sets('pidis')
    tables = conf['pidis tabs'].keys()

    replicas=core.get_replicas(wdir)
    core.mod_conf(istep,replicas[0]) #--set conf as specified in istep   
   
    resman=RESMAN(nworkers=1,parallel=False,datasets=False)
    parman=resman.parman

    jar=load('%s/data/jar-%d.dat'%(wdir,istep))
    replicas=jar['replicas']
    parman.order=jar['order']

    data = predictions['reactions']['pidis']

    cluster,colors,nc,cluster_order = classifier.get_clusters(wdir,istep,kc)

    for idx in data:
        predictions = copy.copy(data[idx]['prediction-rep'])
        del data[idx]['prediction-rep']
        del data[idx]['residuals-rep']
        for ic in range(kc.nc[istep]):
            predictions_ic = [predictions[i] for i in range(len(predictions)) if cluster[i] == ic]
            data[idx]['thy-%d' % ic] = np.mean(predictions_ic, axis = 0)
            data[idx]['dthy-%d' % ic] = np.std(predictions_ic, axis = 0)

    if 90001 in data.keys(): idxs,est = [90001],'opt'
    if 90011 in data.keys(): idxs,est = [90011],'mod'
    if 90021 in data.keys(): idxs,est = [90021],'pes'

    hand = {}
    #--plot data
    for idx in idxs:
        x  = conf['pidis tabs'][idx]['X']
        q2 = conf['pidis tabs'][idx]['Q2']
        values = conf['pidis tabs'][idx]['value']
        alpha  = data[idx]['alpha']
        l = len(values)
        #--average asymmetry and standard deviation       
        theory  = data[idx]['thy-0']
        dtheory = data[idx]['dthy-0']
        #--get fixed values for Q2
        Q2 = []
        for j in range(len(q2)):
            if q2[j] in Q2: continue
            Q2.append(q2[j])
        #--get corresponding x, asymmetry values
        for j in range(len(Q2)):
            Xp, valp, alpp, thyp, dthyp = [],[],[],[],[]
            Xn, valn, alpn, thyn, dthyn = [],[],[],[],[]
            for i in range(l):
                if q2[i] != Q2[j]: continue
                if values[i] > 0: 
                    valp .append(values[i])
                    Xp   .append(x[i])
                    alpp .append(alpha[i])
                    thyp .append(theory[i])
                    dthyp.append(dtheory[i])
                else:
                    valn .append(values[i])
                    Xn   .append(x[i])
                    alpn .append(alpha[i])
                    thyn .append(theory[i])
                    dthyn.append(dtheory[i])

            hand['pos'] = ax11.errorbar(Xp,valp        ,yerr=alpp,color='firebrick',fmt='o',ms=3.0)
            hand['neg'] = ax11.errorbar(Xn,np.abs(valn),yerr=alpn,color='darkgreen',fmt='^',ms=3.0)

            thy_plot ,= ax11.plot(Xp,thyp,color='black',alpha=1.0)
            ax11.plot(Xn,np.abs(thyn)    ,color='black',alpha=1.0)
            downp = np.array(thyp) - np.array(dthyp)
            upp   = np.array(thyp) + np.array(dthyp)
            downn = np.array(np.abs(thyn)) - np.array(dthyn)
            upn   = np.array(np.abs(thyn)) + np.array(dthyn)
            thy_band  = ax11.fill_between(Xp,downp,upp,color='gold',alpha=1.0)
            ax11.fill_between(Xn,downn,upn,color='gold',alpha=1.0)

    ax11.semilogx()
    ax11.semilogy()
    ax11.set_xlabel(r'$x$',size=30)
    ax11.set_xlim(3e-4,4.0)
    ax11.set_ylim(5e-9,1e-1)
    ax11.set_yticks([1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1])
    locmin = matplotlib.ticker.LogLocator(base=10.0,subs=(0.2,0.4,0.6,0.8),numticks=8)
    ax11.yaxis.set_minor_locator(locmin)
    ax11.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

    ax11.text(0.60,0.30,r'$Q^2=%s$'%np.round(Q2[0],1) + ' ' + r'\textrm{GeV}' + r'$^2$',transform=ax11.transAxes,size=14)
    ax11.text(0.66,0.38,r'$Q^2=%s$'%np.round(Q2[1],1)                                  ,transform=ax11.transAxes,size=14)
    ax11.text(0.73,0.46,r'$Q^2=%s$'%np.round(Q2[2],1)                                  ,transform=ax11.transAxes,size=14)
    ax11.text(0.80,0.53,r'$Q^2=%s$'%np.round(Q2[3],1)                                  ,transform=ax11.transAxes,size=14)
    ax11.text(0.80,0.60,r'$Q^2=%s$'%np.round(Q2[4],1)                                  ,transform=ax11.transAxes,size=14)
    ax11.text(0.80,0.66,r'$Q^2=%s$'%np.round(Q2[5],1)                                  ,transform=ax11.transAxes,size=14)
    ax11.text(0.80,0.73,r'$Q^2=%s$'%np.round(Q2[6],1)                                  ,transform=ax11.transAxes,size=14)
    ax11.text(0.80,0.80,r'$Q^2=%s$'%np.round(Q2[7],1)                                  ,transform=ax11.transAxes,size=14)
    ax11.text(0.80,0.90,r'$Q^2=%s$'%np.round(Q2[8],1)                                  ,transform=ax11.transAxes,size=14)

    if est == 'opt': ax11.text(0.4,0.9,r'\textrm{Optimistic}' ,transform=ax11.transAxes,size=20)
    if est == 'mod': ax11.text(0.4,0.9,r'\textrm{Moderate}'   ,transform=ax11.transAxes,size=20)
    if est == 'pes': ax11.text(0.4,0.9,r'\textrm{Pessimistic}',transform=ax11.transAxes,size=20)

    ax11.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=20)

    handles = [(thy_band,thy_plot),hand['pos'],hand['neg']]
    label1  = r'\textbf{\textrm{JAM}}'
    label2  = r'\textbf{\textrm{JAM4EIC(pos)}}'
    label3  = r'\textbf{\textrm{JAM4EIC(neg)}}'
    labels  = [label1,label2,label3]
    ax11.legend(handles,labels,loc='upper left', fontsize = 20, frameon = 0, handletextpad = 0.3, handlelength = 1.0)
    ax11.set_ylabel(r'$|A_{PV}^{had}|$',size=30)

    py.tight_layout()
    checkdir('%s/gallery'%wdir)
    filename='%s/gallery/pvdis_had.png'%(wdir)

    py.savefig(filename)
    print
    print 'Saving PV asymmetry plot to %s'%filename

def plot_obs(wdir,kc,kind):

    if kind=='e':
        plot_pvdis_e(wdir,kc)

    if kind=='had':
        plot_pvdis_had(wdir,kc)




