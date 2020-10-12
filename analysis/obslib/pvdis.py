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

def plot_obs(wdir,kc,kind,tar):

    if kind=='e':
        plot_pvdis_e(wdir,kc,tar)

    if kind=='had':
        plot_pvdis_had(wdir,kc,tar)

def plot_pvdis_e(wdir,kc,tar):

    print('\ngenerating A_PV electron from %s'%(wdir))
    load_config('%s/input.py'%wdir)
    istep=core.get_istep()
    predictions = load('%s/data/predictions-%d.dat'%(wdir,istep))
    if 'idis' not in predictions['reactions']: return

    conf['aux']=aux.AUX()
    conf['datasets'] = {}
    conf['datasets']['idis']={}
    conf['datasets']['idis']['xlsx']={}

    if tar == 'p': conf['datasets']['idis']['xlsx'][90001]='idis/expdata/90001.xlsx'
    if tar == 'd': conf['datasets']['idis']['xlsx'][90002]='idis/expdata/90002.xlsx'

    conf['datasets']['idis']['norm']={}
    conf['datasets']['idis']['filters']=[]
    conf['datasets']['idis']['filters'].append('W2>3')
    conf['datasets']['idis']['filters'].append('Q2>1.69')
    conf['idis tabs']=READER().load_data_sets('idis')
    tables = conf['idis tabs'].keys()

    replicas=core.get_replicas(wdir)
    core.mod_conf(istep,replicas[0]) #--set conf as specified in istep   
   
    resman=RESMAN(nworkers=1,parallel=False,datasets=False)
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

    hand = {}
    #--plot data
    for idx in tables:
        RS = np.sort(np.unique(conf['idis tabs'][idx]['RS']))
        for rs in RS:
            nrows,ncols=3,5
            fig = py.figure(figsize=(ncols*7,nrows*6))
            ax11 = py.subplot(nrows,ncols,1)
            ax12 = py.subplot(nrows,ncols,2)
            ax13 = py.subplot(nrows,ncols,3)
            ax14 = py.subplot(nrows,ncols,4)
            ax15 = py.subplot(nrows,ncols,5)
            ax21 = py.subplot(nrows,ncols,6)
            ax22 = py.subplot(nrows,ncols,7)
            ax23 = py.subplot(nrows,ncols,8)
            ax24 = py.subplot(nrows,ncols,9)
            ax25 = py.subplot(nrows,ncols,10)
            ax31 = py.subplot(nrows,ncols,11)
            ax32 = py.subplot(nrows,ncols,12)
            ax33 = py.subplot(nrows,ncols,13)
            ax34 = py.subplot(nrows,ncols,14)
            ax35 = py.subplot(nrows,ncols,15)

            x  = conf['idis tabs'][idx]['X']
            q2 = conf['idis tabs'][idx]['Q2']
            values = conf['idis tabs'][idx]['value']
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
                if j == 0:  ax = ax11
                if j == 1:  ax = ax12
                if j == 2:  ax = ax13
                if j == 3:  ax = ax14
                if j == 4:  ax = ax15
                if j == 5:  ax = ax21
                if j == 6:  ax = ax22
                if j == 7:  ax = ax23
                if j == 8:  ax = ax24
                if j == 9:  ax = ax25
                if j == 10: ax = ax31
                if j == 11: ax = ax32
                if j == 12: ax = ax33
                if j == 13: ax = ax34
                if j == 14: ax = ax35
                X, val, alp, thy, dthy = [],[],[],[],[]
                for i in range(l):
                    if q2[i] != Q2[j]: continue
                    if conf['idis tabs'][idx]['RS'][i] != rs: continue
                    val .append(values[i])
                    X   .append(x[i])
                    alp .append(alpha[i])
                    thy .append(theory[i])
                    dthy.append(dtheory[i])

                hand['obs'] = ax.errorbar(X,val,yerr=alp,color='firebrick',fmt='o',ms=3.0,capsize=3.0)

                thy_plot ,= ax.plot(X,thy,color='black',alpha=1.0)
                down = np.array(thy) - np.array(dthy)
                up   = np.array(thy) + np.array(dthy)
                thy_band  = ax.fill_between(X,down,up,color='gold',alpha=1.0)

            axes = [ax11,ax12,ax13,ax14,ax15,ax21,ax22,ax23,ax24,ax25,ax31,ax32,ax33,ax34,ax35]
   
            for ax in axes:
                ax.axhline(0,0,1,alpha=1.0,color='black',ls='--')
                ax.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=20)
                ax.set_xlim(3e-4,1.0)
                ax.semilogx()

            for ax in [ax11,ax12,ax13,ax14,ax15,ax21,ax22,ax23,ax24,ax25]:
                ax.tick_params(labelbottom=False)

            for ax in [ax31,ax32,ax33,ax34,ax35]:
                ax.set_xlabel(r'\boldmath$x$',size=30)

            for ax in [ax11,ax21,ax31]:
                ax.set_ylabel(r'\boldmath$A_{PV}^{e\rm{(%s)}}$'%tar,size=30)

            #ax11.text(0.05,0.05,r'$\textrm{Proton}$',transform=ax11.transAxes,size=30)
            ax11.text(0.05,0.07,r'$Q^2=%s$'%np.round(Q2[0],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax11.transAxes,size=25)
            ax12.text(0.05,0.07,r'$Q^2=%s$'%np.round(Q2[1],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax12.transAxes,size=25)
            ax13.text(0.05,0.07,r'$Q^2=%s$'%np.round(Q2[2],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax13.transAxes,size=25)
            ax14.text(0.05,0.07,r'$Q^2=%s$'%np.round(Q2[3],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax14.transAxes,size=25)
            ax15.text(0.05,0.07,r'$Q^2=%s$'%np.round(Q2[4],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax15.transAxes,size=25)
            ax21.text(0.05,0.07,r'$Q^2=%s$'%np.round(Q2[5],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax21.transAxes,size=25)
            ax22.text(0.05,0.07,r'$Q^2=%s$'%np.round(Q2[6],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax22.transAxes,size=25)
            ax23.text(0.05,0.07,r'$Q^2=%s$'%np.round(Q2[7],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax23.transAxes,size=25)
            ax24.text(0.05,0.07,r'$Q^2=%s$'%np.round(Q2[8],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax24.transAxes,size=25)
            ax25.text(0.05,0.07,r'$Q^2=%s$'%np.round(Q2[9],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax25.transAxes,size=25)
            ax31.text(0.05,0.07,r'$Q^2=%s$'%np.round(Q2[10],1) + ' ' + r'\textrm{GeV}' + r'$^2$',transform=ax31.transAxes,size=25)
            ax32.text(0.05,0.07,r'$Q^2=%s$'%np.round(Q2[11],1) + ' ' + r'\textrm{GeV}' + r'$^2$',transform=ax32.transAxes,size=25)
            ax33.text(0.05,0.07,r'$Q^2=%s$'%np.round(Q2[12],1) + ' ' + r'\textrm{GeV}' + r'$^2$',transform=ax33.transAxes,size=25)
            ax34.text(0.05,0.07,r'$Q^2=%s$'%np.round(Q2[13],1) + ' ' + r'\textrm{GeV}' + r'$^2$',transform=ax34.transAxes,size=25)
            ax35.text(0.05,0.07,r'$Q^2=%s$'%np.round(Q2[14],1) + ' ' + r'\textrm{GeV}' + r'$^2$',transform=ax35.transAxes,size=25)
            #ax11.text(0.80,0.07,r'$Q^2=%s$'%np.round(Q2[8],1)                                  ,transform=ax11.transAxes,size=14)


            ax11.text(0.05,0.15, r'$\sqrt{s} = %s$'%np.round(rs,1)   +' '+r'\textrm{GeV}', transform = ax11.transAxes,fontsize=35)

            handles = [(thy_band,thy_plot),hand['obs']]
            label1  = r'\textbf{\textrm{JAM}}'
            label2  = r'\textbf{\textrm{JAM4EIC}}'
            labels  = [label1,label2]
            ax11.legend(handles,labels,loc='upper right', fontsize = 25, frameon = 0, handletextpad = 0.3, handlelength = 1.0)

            py.tight_layout()
            py.subplots_adjust(hspace=0)
            checkdir('%s/gallery'%wdir)
            filename='%s/gallery/pvdis_e_%s_RS-%s.png'%(wdir,tar,np.round(rs,1))

            py.savefig(filename)
            py.clf()
            print
            print 'Saving A_PV electron %s plot to %s'%(tar,filename)

def plot_pvdis_had(wdir,kc,tar):

    print('\ngenerating A_PV hadron from %s'%(wdir))
    load_config('%s/input.py'%wdir)
    istep=core.get_istep()
    predictions = load('%s/data/predictions-%d.dat'%(wdir,istep))
    if 'idis' not in predictions['reactions']: return

    conf['aux']=aux.AUX()
    conf['datasets'] = {}
    conf['datasets']['pidis']={}
    conf['datasets']['pidis']['xlsx']={}

    if tar == 'p': conf['datasets']['pidis']['xlsx'][90001]='pidis/expdata/90001.xlsx'

    conf['datasets']['pidis']['norm']={}
    conf['datasets']['pidis']['filters']=[]
    conf['datasets']['pidis']['filters'].append('W2>10')
    conf['datasets']['pidis']['filters'].append('Q2>1.69')
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

    hand = {}
    #--plot data
    for idx in tables:
        RS = np.sort(np.unique(conf['pidis tabs'][idx]['RS']))
        for rs in RS:
            nrows,ncols=3,5
            fig = py.figure(figsize=(ncols*7,nrows*6))
            ax11 = py.subplot(nrows,ncols,1)
            ax12 = py.subplot(nrows,ncols,2)
            ax13 = py.subplot(nrows,ncols,3)
            ax14 = py.subplot(nrows,ncols,4)
            ax15 = py.subplot(nrows,ncols,5)
            ax21 = py.subplot(nrows,ncols,6)
            ax22 = py.subplot(nrows,ncols,7)
            ax23 = py.subplot(nrows,ncols,8)
            ax24 = py.subplot(nrows,ncols,9)
            ax25 = py.subplot(nrows,ncols,10)
            ax31 = py.subplot(nrows,ncols,11)
            ax32 = py.subplot(nrows,ncols,12)
            ax33 = py.subplot(nrows,ncols,13)
            ax34 = py.subplot(nrows,ncols,14)
            ax35 = py.subplot(nrows,ncols,15)

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
                if j == 0:  ax = ax11
                if j == 1:  ax = ax12
                if j == 2:  ax = ax13
                if j == 3:  ax = ax14
                if j == 4:  ax = ax15
                if j == 5:  ax = ax21
                if j == 6:  ax = ax22
                if j == 7:  ax = ax23
                if j == 8:  ax = ax24
                if j == 9:  ax = ax25
                if j == 10: ax = ax31
                if j == 11: ax = ax32
                if j == 12: ax = ax33
                if j == 13: ax = ax34
                if j == 14: ax = ax35
                X, val, alp, thy, dthy = [],[],[],[],[]
                for i in range(l):
                    if q2[i] != Q2[j]: continue
                    if conf['pidis tabs'][idx]['RS'][i] != rs: continue
                    val .append(values[i])
                    X   .append(x[i])
                    alp .append(alpha[i])
                    thy .append(theory[i])
                    dthy.append(dtheory[i])

                hand['obs'] = ax.errorbar(X,val,yerr=alp,color='firebrick',fmt='o',ms=3.0,capsize=3.0)

                thy_plot ,= ax.plot(X,thy,color='black',alpha=1.0)
                down = np.array(thy) - np.array(dthy)
                up   = np.array(thy) + np.array(dthy)
                thy_band  = ax.fill_between(X,down,up,color='gold',alpha=1.0)

            axes = [ax11,ax12,ax13,ax14,ax15,ax21,ax22,ax23,ax24,ax25,ax31,ax32,ax33,ax34,ax35]
   
            for ax in axes:
                ax.axhline(0,0,1,alpha=1.0,color='black',ls='--')
                ax.tick_params(axis='both',which='both',top=True,right=True,direction='in',labelsize=20)
                ax.set_xlim(3e-4,1.0)
                ax.semilogx()

            for ax in [ax11,ax12,ax13,ax14,ax15,ax21,ax22,ax23,ax24,ax25]:
                ax.tick_params(labelbottom=False)

            for ax in [ax31,ax32,ax33,ax34,ax35]:
                ax.set_xlabel(r'\boldmath$x$',size=30)

            for ax in [ax11,ax21,ax31]:
                ax.set_ylabel(r'\boldmath$A_{PV}^{%s}$'%tar,size=30)

            #ax11.text(0.05,0.05,r'$\textrm{Proton}$',transform=ax11.transAxes,size=30)
            ax11.text(0.05,0.05,r'$Q^2=%s$'%np.round(Q2[0],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax11.transAxes,size=25)
            ax12.text(0.05,0.05,r'$Q^2=%s$'%np.round(Q2[1],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax12.transAxes,size=25)
            ax13.text(0.05,0.05,r'$Q^2=%s$'%np.round(Q2[2],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax13.transAxes,size=25)
            ax14.text(0.05,0.05,r'$Q^2=%s$'%np.round(Q2[3],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax14.transAxes,size=25)
            ax15.text(0.05,0.05,r'$Q^2=%s$'%np.round(Q2[4],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax15.transAxes,size=25)
            ax21.text(0.05,0.05,r'$Q^2=%s$'%np.round(Q2[5],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax21.transAxes,size=25)
            ax22.text(0.05,0.05,r'$Q^2=%s$'%np.round(Q2[6],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax22.transAxes,size=25)
            ax23.text(0.05,0.05,r'$Q^2=%s$'%np.round(Q2[7],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax23.transAxes,size=25)
            ax24.text(0.05,0.05,r'$Q^2=%s$'%np.round(Q2[8],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax24.transAxes,size=25)
            ax25.text(0.05,0.05,r'$Q^2=%s$'%np.round(Q2[9],1) + ' ' + r'\textrm{GeV}' + r'$^2$' ,transform=ax25.transAxes,size=25)
            ax31.text(0.05,0.05,r'$Q^2=%s$'%np.round(Q2[10],1) + ' ' + r'\textrm{GeV}' + r'$^2$',transform=ax31.transAxes,size=25)
            ax32.text(0.05,0.05,r'$Q^2=%s$'%np.round(Q2[11],1) + ' ' + r'\textrm{GeV}' + r'$^2$',transform=ax32.transAxes,size=25)
            ax33.text(0.05,0.05,r'$Q^2=%s$'%np.round(Q2[12],1) + ' ' + r'\textrm{GeV}' + r'$^2$',transform=ax33.transAxes,size=25)
            ax34.text(0.05,0.05,r'$Q^2=%s$'%np.round(Q2[13],1) + ' ' + r'\textrm{GeV}' + r'$^2$',transform=ax34.transAxes,size=25)
            ax35.text(0.05,0.05,r'$Q^2=%s$'%np.round(Q2[14],1) + ' ' + r'\textrm{GeV}' + r'$^2$',transform=ax35.transAxes,size=25)
            #ax11.text(0.80,0.07,r'$Q^2=%s$'%np.round(Q2[8],1)                                  ,transform=ax11.transAxes,size=14)


            ax11.text(0.05,0.15, r'$\sqrt{s} = %s$'%np.round(rs,1)   +' '+r'\textrm{GeV}', transform = ax11.transAxes,fontsize=35)

            handles = [(thy_band,thy_plot),hand['obs']]
            label1  = r'\textbf{\textrm{JAM}}'
            label2  = r'\textbf{\textrm{JAM4EIC}}'
            labels  = [label1,label2]
            ax11.legend(handles,labels,loc='upper right', fontsize = 25, frameon = 0, handletextpad = 0.3, handlelength = 1.0)

            py.tight_layout()
            py.subplots_adjust(hspace=0)
            checkdir('%s/gallery'%wdir)
            filename='%s/gallery/pvdis_had_%s_RS-%s.png'%(wdir,tar,np.round(rs,1))

            py.savefig(filename)
            py.clf()
            print
            print 'Saving A_PV hadron %s plot to %s'%(tar,filename)



