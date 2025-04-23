#from simple_pid import PID
from simplepidj import PID
import matplotlib.pyplot as plt
from matplotlib import rc
import colorednoise as cn
import numpy as np
import random
import argparse
import sys
import importlib
from modnetcdf import ecrit1d
import  tkinter as tk
from modmultipid import  *
from myclim import clim_sh_nh, initialise_aod_responses, emi2aod, emi2rf, Monsoon, Monsoon_IPSL
from matplotlib.backends.backend_pdf import PdfPages
import netCDF4 as nc4
import copy


print("aremipoints",aremipoints)
#--call script as: python test.py --exp=4 --noise=mixed

parser = argparse.ArgumentParser()
parser.add_argument('conf',
                    type=str,
                    help='configuration file. Contains the description of experiment')

args = parser.parse_args()


poids=np.zeros(4)

with open(args.conf) as f:
  exec(f.read())
del f

print("tau_nh_sh_upper",tau_nh_sh_upper)
g=globals()
if (not "outpdf" in g) or  (not outpdf):
  outpdf="out-{:}.pdf".format(exp)
if (not "outnc" in g) or  (not outnc):
  outnc="out-{:}.nc".format(exp)



#--initialise PID controller for each actors
#--PID(Kp, Ki, Kd, setpoint)
#--Kp: proportional gain (typically 0.8 (TgS/yr)/°C    for T target and 0.08 (TgS/yr)/% monsoon    for monsoon change target)
#--Ki: integral gain     (typically 0.6 (TgS/yr)/°C/yr for T target and 0.06 (TgS/yr)/% monsoon/yr for monsoon change target)
#--Kd: derivative gain   (typically 0)
#--type: GMST (global mean surf temp), NHST (NH surf temp), SHST (SH surf temp), monsoon
#--setpoint: objective (temperature change in K, monsoon change in %)
#--emimin, emimax: bounds of emissions (in TgS/yr)
#--emipoints: emission points: 30N, 15N, Eq, 15S, 30S
#--t0= start of model integration (in years)
#--t1: start of ramping up SRM intervention
#--t2: end of ramping up SRM intervention
#--t5: time of end of SRM intervention (in years)
#--stops: periods of SRM interruption, list of tuples (t3,t4) and targets exceeded

#--directory for plots
dirout='plots/'
#--show plots while running
pltshow=False
#--if non empty, output PDF file.




#--List of experiments with list of actors, type of setpoint, setpoint, emissions min/max and emission points
#--single actor in NH emitting in his own hemisphere

#




#--Initialise properties of Actors
P={'A':A}
if 'B' in vars(): P['B']=B
if 'C' in vars(): P['C']=C
if 'D' in vars(): P['D']=D
Actors=P.keys()
#
#--print Actors and their properties on screen
title=''
#
#--create a list of all emission points
emipoints=[]
print('List of emission points:', emipoints)
markers={'60S':'v','30S':'v','15S':'v','eq':'o','15N':'^','30N':'^','60N':'^',}
sizes={'60S':30,'30S':30,'15S':15,'eq':10,'15N':15,'30N':30,'60N':30}
colors={'A':'green','B':'orange','C':'purple'}
#
#--format float
myformat="{0:3.1f}"
#
#--initialise impulse response functions
aod_strat_sh, aod_strat_nh, nbyr_irf = initialise_aod_responses()
#
#--initialise GHG forcing scenario, increases linearly for 100 yrs then constant then decrease slowly
if not ("f" in globals()):
  f=np.zeros((t5))
  f[0:100]=np.linspace(0.,fmax,100)
  f[100:150]=fmax
  f[150:]=np.linspace(fmax,3*fmax/4,50)
#--transient decrease in forcing if volcanic eruption
  if volcano:
     f[125]+=-2.0
     f[126]+=-1.0
#
eminoise={}
if not noisefilei: # generation of noise

  #--time profiles of climate noise
  for emipoint in aremipoints:
    eminoise[emipoint]=np.zeros(t5)
    if emipoint in eminoisestd.keys():
      std1=eminoisestd[emipoint]
      if std1>0:
        eminoise[emipoint]=np.random.normal(0,std1,t5)


  if noise_type=='white':
    white_noise_T=cn.powerlaw_psd_gaussian(0,t5)*noise_T
    Tnh_noise=white_noise_T
    Tsh_noise=white_noise_T
  elif noise_type=='red':
    Tnh_noise=cn.powerlaw_psd_gaussian(2,t5)*noise_T
    Tsh_noise=cn.powerlaw_psd_gaussian(2,t5)*noise_T
  elif noise_type=='mixed':
    white_noise_T=cn.powerlaw_psd_gaussian(0,t5)*noise_T/2.
    red_noise_T=cn.powerlaw_psd_gaussian(0,t5)*noise_T/2.
    Tnh_noise=white_noise_T+red_noise_T
    red_noise_T=cn.powerlaw_psd_gaussian(0,t5)*noise_T/2.
    Tsh_noise=white_noise_T+red_noise_T
  #--monsoon noise
  monsoon_noise=cn.powerlaw_psd_gaussian(0,t5)*noise_monsoon
  
  print("point 1, bruit mousson min = {:12.4e} max = {:12.4e}\n".format(monsoon_noise.min(),
                                                                        monsoon_noise.max()))
  #--time profiles of observation noise
  if "TSRM_noise_obs" in globals():
    TSRM_noise_obs=np.random.normal(0,TSRM_noise_obs_std,t5)
  else:
    TSRM_noise_obs=np.zeros(t5)
  if "TSRMnh_noise_obs" in globals():
    TSRMnh_noise_obs=np.random.normal(0,TSRMnh_noise_obs_std,t5)
  else:
    TSRMnh_noise_obs=np.zeros(t5)

  if "TSRMsh_noise_obs" in globals():
    TSRMsh_noise_obs=np.random.normal(0,TSRMsh_noise_obs_std,t5)
  else:
    TSRMsh_noise_obs=np.zeros(t5)
  if "monsoon_noise_obs" in globals():
    monsoon_noise_obs=np.random.normal(0,monsoon_noise_obs_std,t5)
  else:
    monsoon_noise_obs=np.zeros(t5)

  for emipoint in aremipoints:
    if emipoint in eminoisestd:
     eminoise[emipoint]=np.random.normal(0,eminoisestd[emipoint],t5)
  else:
    eminoise[emipoint]=np.zeros(t5)

    
else: # noise is read from noisefilei
  fn = nc4.Dataset(noisefilei, "r", format="NETCDF4")
  var=fn.variables
  Tnh_noise=np.copy(var['tnh_noise'][:])
  Tsh_noise=np.copy(var['tsh_noise'][:])
  monsoon_noise=np.copy(var['monsoon_noise'])
  TSRM_noise_obs=np.copy(var['tg_noise_obs'][:])
  TSRMnh_noise_obs=np.copy(var['tnh_noise_obs'][:])
  TSRMsh_noise_obs=np.copy(var['tsh_noise_obs'][:])
  monsoon_noise_obs=np.copy(var['monsoon_noise_obs'])
  for emipoint in aremipoints:
    nomvar='eminoise_'+emipoint
    eminoise[emipoint]=np.copy(var[nomvar])
      



  fn.close()

print("tnhnoise[-1]",Tnh_noise[-1])
if "noisefileo" in globals() and noisefileo:
  fn = nc4.Dataset(noisefileo, "w", format="NETCDF4")
  fn.createDimension('t', size=t5)
  
  
  tnhn=fn.createVariable("tnh_noise","f8",("t"))
  tnhn[:]=Tnh_noise[:]
  tnhn.description='Nothern hemisphere temperature noise (K)'
  
  tshn=fn.createVariable("tsh_noise","f8",("t"))
  tshn[:]=Tsh_noise[:]
  tshn.description='Southern hemisphere temperature noise (K)'
  
  mn=fn.createVariable("monsoon_noise","f8",("t"))
  mn[:]=monsoon_noise[:]
  mn.description='Monsoon noise'
  
  
  tgno=fn.createVariable("tg_noise_obs","f8",("t"))
  tgno[:]=TSRM_noise_obs[:]
  tgno.description='Global temperature obs noise (K)'
  
  tnhno=fn.createVariable("tnh_noise_obs","f8",("t"))
  tnhno[:]=TSRMnh_noise_obs[:]
  tnhno.description='Nothern hemisphere temperature obs noise (K)'
  
  tshno=fn.createVariable("tsh_noise_obs","f8",("t"))
  tshno[:]=TSRMsh_noise_obs[:]
  tshno.description='Southern hemisphere temperature obs noise (K)'
  
  mno=fn.createVariable("monsoon_noise_obs","f8",("t"))
  mno[:]=monsoon_noise_obs[:]
  mno.description='Monsoon obs noise'
  
  vn={}
  for emipoint in aremipoints:
    nomvar='eminoise_'+emipoint
    vn[emipoint]=ecrit1d(fn,nomvar,"f8","t",eminoise[emipoint])
    vn[emipoint]="emission noise at " + emipoint
  fn.close()

#
#--define filename
filename='test'+exp+'.png'
#
#--define the PIDs and the emission min/max profiles
g=globals()
PIDs={} ; emissmin={} ; emissmax={} ; emi_SRM={} ; emi_SRM={}
#--loop on Actors



for Actor in Actors:



  if not P[Actor]:
    continue
  dic=P[Actor]
  keysact=(P[Actor]).keys()
  
  drp=("dicKp" in keysact )
  dri=("dicKi" in keysact )
  drd=("dicKd" in keysact )
  
  if not (dri or drd or drp):
    stderr.write('No multiPID controller defined. End of program\n')
    exit(1)




  Kp=np.zeros([nc,ns])
  Ki=np.zeros([nc,ns])
  Kd=np.zeros([nc,ns])
  if drp:
    dicKpa=copy.deepcopy(P[Actor]['dicKp'])
    for t in dicKpa: 
      js=target2js[t]
      for e in dicKpa[t]:
        jc= emipoint2jc[e]
        Kp[jc,js]=dicKpa[t][e]

  if dri:
    dicKia=copy.deepcopy(P[Actor]['dicKi'])
    for t in dicKia: 
      js=target2js[t]
      for e in dicKia[t]:
        jc= emipoint2jc[e]
        Ki[jc,js]=dicKia[t][e]
  if drd:
    dicKda=copy.deepcopy(P[Actor]['dicKd'])
    for t in dicKia: 
      js=target2js[t]
      for e in dicKda[t]:
        jc= emipoint2jc[e]
        Kd[jc,js]=dicKda[t][e]
  P[Actor]['Kp']=copy.deepcopy(Kp)
  P[Actor]['Ki']=copy.deepcopy(Ki)
  P[Actor]['Kd']=copy.deepcopy(Kd)
  


  PIDs[Actor]={}
  if False:
    xs=np.zeros(ns)
    xs[type2js[P[Actor]['type']]]=P[Actor][setpoint]

  for target in P[Actor]['targets']:
    xs[type2js[target]]=P[Actor]['targets'][target]

  for target in P[Actor]['poids']:
    poids[type2js[target]]=P[Actor]['poids'][target]
     
  #xs[:]=0.
  emi_SRM[Actor]={}
  #--loop on emission points of Actor

  for emipoint in aremipoints:
    emi_SRM[Actor][emipoint]=[0.0]
  PIDs[Actor] = multipid(ns,
                          nc,
                          xs,
                          P[Actor]['Kp'],
                          P[Actor]['Ki'],
                          P[Actor]['Kd'],
                          boundedint=True,
                          poids=poids,
                          dt=1.)
                          



  #--initialise the profile of emission min/max (emissions are counted negative)
  emimin=-1*P[Actor]['emimax'] ; emimax=-1*P[Actor]['emimin']
  t1=P[Actor]['t1'] ; t2=P[Actor]['t2'] ; stops=P[Actor]['stops']
  emissmin[Actor]=np.zeros((t5))
  emissmax[Actor]=np.zeros((t5))
  emissmin[Actor][t1:t2]=np.linspace(0.0,emimin,t2-t1)
  emissmax[Actor][t1:t2]=np.linspace(0.0,emimax,t2-t1)
  emissmin[Actor][t2:]=emimin
  emissmax[Actor][t2:]=emimax
  for stop in stops:
     if type(stop)==type(()):
       t3=stop[0] ; t4=stop[1]
       emissmin[Actor][t3:t4]=0
       emissmax[Actor][t3:t4]=0
#
#--initialise more stuff
T_SRM=[] ; T_SRM_sh=[] ; T_SRM_nh=[] ; T_noSRM=[] ; T_noSRM_sh=[] ; T_noSRM_nh=[] ; g_SRM_sh=[] ; g_SRM_nh=[]
TnoSRMsh=0 ; T0noSRMsh=0 ; TnoSRMnh=0 ; T0noSRMnh=0
TSRMsh=0   ; T0SRMsh=0   ; TSRMnh=0   ; T0SRMnh=0
monsoon_SRM=[] ; monsoon_noSRM=[] 
#
#--loop on time
fl=open("log.txt","w")
for t in range(t0,t5):
  #print("###################### t={:d} ###########################################".format(t))
  #
  #--reference calculation with no SRM 
  #-----------------------------------

  if (t==1):
    print("nnn",f[t],Tsh_noise[t],Tnh_noise[t],tau_nh_sh_lower,tau_nh_sh_upper)
  TnoSRM, TnoSRMsh,TnoSRMnh,T0noSRMsh,T0noSRMnh,gsh,gnh = clim_sh_nh(TnoSRMsh,TnoSRMnh,T0noSRMsh,T0noSRMnh,{}, \
                                                                     aod_strat_sh,aod_strat_nh,nbyr_irf,\
                                                                     f=f[t], 
                                                                     geff=geff,
                                                                     tau_nh_sh_upper=tau_nh_sh_upper,
                                                                     tau_nh_sh_lower=tau_nh_sh_lower,
                                                                     C=Catm,
                                                                     C0=C0,
                                                                     lam=lam,
                                                                     gamma=gamma,
                                                                     ndt=ndt, 
                                                                     Tsh_noise=Tsh_noise[t],
                                                                     Tnh_noise=Tnh_noise[t])







#  print("t={:d} Tnh = {:14.7e} ".format(t,TnoSRMnh))
#  print("t={:d} Tsh = {:14.7e} ".format(t,TnoSRMsh))
#  print("t={:d} T0nh = {:14.7e} ".format(t,T0noSRMnh))
#  print("t={:d} T0sh = {:14.7e} ".format(t,T0noSRMsh))
#  print("t={:d} f = {:14.7e} ".format(t,f[t]))
#  print("t={:d} tnh_noise = {:14.7e} ".format(t,Tnh_noise[t]))
#  print("t={:d} tsh_noise = {:14.7e} ".format(t,Tsh_noise[t]))
#
  T_noSRM.append(TnoSRM) ; T_noSRM_sh.append(TnoSRMsh) ; T_noSRM_nh.append(TnoSRMnh) 
  ##monsoon=Monsoon(0.0,0.0,noise=monsoon_noise[t]) ; monsoon_noSRM.append(monsoon)
  monsoon=Monsoon_IPSL(0.0,0.0,0.0,0.0,noise=monsoon_noise[t]) ; monsoon_noSRM.append(monsoon)
  #
  #--calculation with SRM
  #----------------------
  #
  #--prepare dictionary of combined emissions across all Actors
  emits={}
  #--loop on emission points of Actor
  print("emi_SRM.keys",emi_SRM.keys())

  for Actor in Actors:
    if not P[Actor]:
      continue
    for emipoint in P[Actor]['aremipoints2']:
      if emipoint in emits:
         emits[emipoint] = [x + y for x,y in zip(emits[emipoint],emi_SRM[Actor][emipoint])]
      else:
         emits[emipoint] = emi_SRM[Actor][emipoint]



  #
  #--iterate climate model with emits as input
  TSRM, TSRMsh,TSRMnh,T0SRMsh,T0SRMnh,gsh,gnh = clim_sh_nh(TSRMsh,TSRMnh,T0SRMsh,T0SRMnh,emits,aod_strat_sh,aod_strat_nh,nbyr_irf,
                                                                     f=f[t],
                                                                     geff=geff,
                                                                     tau_nh_sh_upper=tau_nh_sh_upper,
                                                                     tau_nh_sh_lower=tau_nh_sh_lower,
                                                                     C=Catm,
                                                                     C0=C0,
                                                                     lam=lam,
                                                                     gamma=gamma,
                                                                     ndt=ndt, 
                                                                     Tsh_noise=Tsh_noise[t],
                                                                     Tnh_noise=Tnh_noise[t])

  fl.write("t,gnh,gsh {:3d} {:10.2e} {:10.2e}\n".format(t,gnh,gsh))
  #
  #--compute monsoon change
  ##monsoon=Monsoon(*emi2aod(emits,aod_strat_sh,aod_strat_nh,nbyr_irf),noise=monsoon_noise[t])
  monsoon=Monsoon_IPSL(*emi2aod(emits,aod_strat_sh,aod_strat_nh,nbyr_irf),TSRMsh,TSRMnh,noise=monsoon_noise[t])
  #
  #--report climate model output into lists for plots
  T_SRM.append(TSRM) ; T_SRM_sh.append(TSRMsh) ; T_SRM_nh.append(TSRMnh) ; g_SRM_sh.append(gsh) ; g_SRM_nh.append(gnh) ; monsoon_SRM.append(monsoon)
  #
  # compute new ouput from the PID according to the systems current value
  #--loop on emission points of Actor
  for Actor in Actors:
    if not P[Actor]:
      continue
    #--check for additional interactive stops
    stops=[stop for stop in P[Actor]['stops'] if type(stop)==type(0.0)]
    #--loop on emission points
    PIDs[Actor].setoutlimits(emissmin[Actor][t],emissmax[Actor][t])
    x=var2x(TSRM+TSRM_noise_obs[t],
              TSRMnh+TSRMnh_noise_obs[t],
              TSRMsh+TSRMsh_noise_obs[t],
              -1*monsoon+monsoon_noise_obs[t])
    #PIDs[Actor].addstatevector(xs,t)
    xc=PIDs[Actor].state2control(x,t)
    print("t,xc",t,xc) 
    for i in range(0,xc.size):
      emipoint=aremipoints[i]
      try:
        emi_SRM[Actor][emipoint].append(xc[i])
      except:
        pass
   


print("Actor ",Actor)
for Actor in Actors:
  if not P[Actor]:
    continue
  for emipoint in P[Actor]['aremipoints2']:
    print("  {:} : {:10.2e}".format(emipoint,emi_SRM[Actor][emipoint][-1]))
    emi_SRM[Actor][emipoint] = [-1.*x for x in emi_SRM[Actor][emipoint]]
#

fl.close()
#--assess mean and variability
print('Mean and s.d. of TSRMnh w/o SRM:',myformat.format(np.mean(T_noSRM_nh[t2:])),'+/-',myformat.format(np.std(T_noSRM_nh[t2:])))
print('Mean and s.d. of TSRMnh w   SRM:',myformat.format(np.mean(T_SRM_nh[t2:])),'+/-',myformat.format(np.std(T_SRM_nh[t2:])))
#
print('Mean and s.d. of TSRMsh w/o SRM:',myformat.format(np.mean(T_noSRM_sh[t2:])),'+/-',myformat.format(np.std(T_noSRM_sh[t2:])))
print('Mean and s.d. of TSRMsh w   SRM:',myformat.format(np.mean(T_SRM_sh[t2:])),'+/-',myformat.format(np.std(T_SRM_sh[t2:])))
#
print('Mean and s.d. of monsoon w/o SRM:',myformat.format(np.mean(monsoon_noSRM[t2:])),'+/-',myformat.format(np.std(monsoon_noSRM[t2:])))
print('Mean and s.d. of monsoon w   SRM:',myformat.format(np.mean(monsoon_SRM[t2:])),'+/-',myformat.format(np.std(monsoon_SRM[t2:])))
#
print("outpdf",outpdf)

if outpdf:
  pp=PdfPages(outpdf)
#--basic plot with results
title='Controlling global SAI'+title
fig, axs = plt.subplots(3,2,figsize=(22,13))
fig.suptitle(title,fontsize=16)
plt.subplots_adjust(bottom=0.15)
#
axs[0,0].plot([t0,t5],[0,0],zorder=0,linewidth=0.4)
axs[0,0].plot(f,label='GHG RF',c='red')
axs[0,0].legend(loc='upper left',fontsize=12)
axs[0,0].set_ylabel('RF (Wm$^{-2}$)',fontsize=14)
axs[0,0].set_xlim(t0,t5)
axs[0,0].set_xticks(np.arange(t0,t5+1,25))
axs[0,0].tick_params(size=14)
axs[0,0].tick_params(size=14)
#
axs[0,1].plot([t0,t5],[0,0],zorder=0,linewidth=0.4)
axs[0,1].plot(Tnh_noise,label='NHST noise',c='black')
axs[0,1].plot(Tsh_noise,label='SHST noise',c='green')
axs[0,1].plot(monsoon_noise/100.,label='Monsoon noise',c='red')
axs[0,1].legend(loc='lower right',fontsize=12)
axs[0,1].set_ylabel('Noise level',fontsize=14)
axs[0,1].set_xlim(t0,t5)
axs[0,1].set_xticks(np.arange(t0,t5+1,25))
axs[0,1].tick_params(size=14)
axs[0,1].tick_params(size=14)
#
for Actor in Actors:
  if not P[Actor]:
    continue
  for emipoint in P[Actor]['aremipoints2']: # P[Actor]['emipoints']:
       axs[1,0].plot(emi_SRM[Actor][emipoint],linestyle='solid',c=colors[Actor])
       axs[1,0].scatter(range(t0,t5+1,10),emi_SRM[Actor][emipoint][::10],label='Emissions '+Actor+' '+emipoint,c=colors[Actor],marker=markers[emipoint],s=sizes[emipoint])
       axs[1,0].plot(-1*emissmin[Actor],linestyle='dashed',linewidth=0.5,c=colors[Actor])
axs[1,0].legend(loc='upper left',fontsize=12)
axs[1,0].set_ylabel('Emi (TgS yr$^{-1}$)',fontsize=14)
axs[1,0].set_xlim(t0,t5)
axs[1,0].set_xticks(np.arange(t0,t5+1,25))
axs[1,0].tick_params(size=14)
axs[1,0].tick_params(size=14)
#
axs[1,1].plot(g_SRM_nh,label='NH SRM g',c='blue')
axs[1,1].plot(g_SRM_sh,label='SH SRM g',c='blue',linestyle='dashed')
axs[1,1].legend(loc='upper left',fontsize=12)
axs[1,1].set_ylabel('RF SRM (Wm$^{-2}$)',fontsize=14)
axs[1,1].set_xlim(t0,t5)
axs[1,1].set_xticks(np.arange(t0,t5+1,25))
axs[1,1].tick_params(size=14)
axs[1,1].tick_params(size=14)
#
axs[2,0].plot(T_noSRM_nh,label='NH dT w/o SRM',c='red',zorder=100)
axs[2,0].plot(T_noSRM_sh,label='SH dT w/o SRM',c='red',linestyle='dashed',zorder=100)
axs[2,0].plot(T_SRM_nh,label='NH dT w SRM',c='blue',zorder=0)
axs[2,0].plot(T_SRM_sh,label='SH dT w SRM',c='blue',linestyle='dashed',zorder=0)
axs[2,0].plot([t0,t5],[0,0],c='black',linewidth=0.5)
axs[2,0].legend(loc='upper left',fontsize=12)
axs[2,0].set_xlabel('Years',fontsize=14)
axs[2,0].set_ylabel(r'Temp. ($^\circ$C)',fontsize=14)
axs[2,0].set_xlim(t0,t5)
axs[2,0].set_xticks(np.arange(t0,t5+1,25))
axs[2,0].tick_params(size=14)
axs[2,0].tick_params(size=14)
#
axs[2,1].plot(monsoon_noSRM,label='monsoon w/o SRM',c='red',zorder=100)
axs[2,1].plot(monsoon_SRM,label='monsoon w SRM',c='blue',zorder=0)
axs[2,1].plot([t0,t5],[0,0],c='black',linewidth=0.5)
axs[2,1].legend(loc='lower left',fontsize=12)
axs[2,1].set_xlabel('Years',fontsize=14)
axs[2,1].set_ylabel('Monsoon (%)',fontsize=14)
axs[2,1].set_xlim(t0,t5)
axs[2,1].set_xticks(np.arange(t0,t5+1,25))
axs[2,1].tick_params(size=14)
axs[2,1].tick_params(size=14)
#
fig.tight_layout()
fig.savefig(dirout+filename)
if outpdf:
  pp.savefig()
  pp.close()
if pltshow: plt.show()


print("point 2, bruit mousson min = {:12.4e} max = {:12.4e}\n".format(monsoon_noise.min(),
                                                                      monsoon_noise.max()))
fo = nc4.Dataset(outnc, "w", format="NETCDF4")
fo.description="Output of two-actors"
fo.experiment=exp
#t=f.createVariable(experiment","f4",("x","y"))
fo.createDimension('t', size=t5)
#

# ecrit1d(fo,name,dtype,dimname,data,description=""):
ecrit1d(fo,"Tnh_noise",'f8',"t",Tnh_noise)
ecrit1d(fo,"Tsh_noise","f8","t",Tsh_noise)
ecrit1d(fo,"monsoon_noise","f8","t",monsoon_noise)
for emipoint in aremipoints:
  nomvar='eminoise_'+emipoint
  ecrit1d(fo,nomvar,"f8","t",eminoise[emipoint])

for acteur in emi_SRM:
  for emipoint in emi_SRM[acteur]:
    nomvar="emi_SRM_{:}_{:}".format(acteur,emipoint)
    ecrit1d(fo,nomvar,"f8","t",emi_SRM[acteur][emipoint][1:])

# pour avoir la même taille que pouqr les autres tableaux
# on n'écrit pas emi[acteur][emipoint][0], qui vaut 0

ecrit1d(fo,"g_SRM_nh","f8","t",g_SRM_nh)
ecrit1d(fo,"g_SRM_sh","f8","t",g_SRM_sh)
ecrit1d(fo,"T_noSRM_nh","f8","t",T_noSRM_nh)
ecrit1d(fo,"T_noSRM_sh","f8","t",T_noSRM_sh)
ecrit1d(fo,"T_SRM_nh","f8","t",T_SRM_nh)
ecrit1d(fo,"T_SRM_sh","f8","t",T_SRM_sh)
ecrit1d(fo,"monsoon_noSRM","f8","t",monsoon_noSRM)
ecrit1d(fo,"monsoon_SRM","f8","t",monsoon_SRM)


t=fo.createVariable('t',"i4",("t",))
t[:]=np.arange(1,t5+1,dtype='i4')

fo.close()

