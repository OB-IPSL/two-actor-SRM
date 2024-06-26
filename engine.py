import matplotlib.pyplot as plt
import numpy as np
import colorednoise as cn
from simple_pid import PID
import random
from myclim import clim_sh_nh,  emi2aod, emi2rf, Monsoon, Monsoon_IPSL
#
#--some keywords
Kp='Kp' ; Ki='Ki' ; Kd='Kd' ; target='target' ; setpoint='setpoint'
#
#--beginning of simulation
t0=0
#
#--format float
myformat="{0:3.1f}"
#
#--data for plots
colors={'A':'green','B':'orange','C':'purple','D':'blue'}
markers={'60S':'v','30S':'v','15S':'v','eq':'o','15N':'^','30N':'^','60N':'^',}
sizes={'60S':30,'30S':30,'15S':15,'eq':10,'15N':15,'30N':30,'60N':30}
#
#--title 
def set_title(P):
  #
  Actors=P.keys()
  #
  title=''
  #
  for Actor in Actors:
    title=title+' - '+Actor+' '+P[Actor][target]+' '+str(P[Actor]['setpoint'])
    print(Actor,'=',P[Actor])
  print('Scenario title: ',title)
  #
  return title
#
#--set emipoints 
def set_emipoints(P):
  #
  Actors=P.keys()
  #
  emipoints=[]
  #
  for Actor in Actors:
    for emipoint in P[Actor]['emipoints']:
        if emipoint not in emipoints: emipoints.append(emipoint)
    #--if target type is monsoon, reverse sign of target for technical reason
    if P[Actor][target]=='monsoon': P[Actor]['setpoint'] = -1.* P[Actor]['setpoint']
  #
  print('List of emission points:', emipoints)
  #
  return emipoints
#
#--initialise forcing
def initialise_forcing(t5,fmax,volcano):
  #
  f=np.zeros((t5))
  f[0:100]=np.linspace(0.,fmax,100)
  f[100:150]=fmax
  f[150:]=np.linspace(fmax,3*fmax/4,50)
  #--transient decrease in forcing if volcanic eruption
  if volcano:
     f[125]+=-2.0
     f[126]+=-1.0
  return f
#
#--set time profiles of climate noise
def set_noise(t5,noise_T,noise_monsoon,noise_type):
  #
  if noise_type=='white':
    white_noise_T=cn.powerlaw_psd_gaussian(0,t5)*noise_T
    Tsh_noise=white_noise_T
    Tnh_noise=white_noise_T
  elif noise_type=='red':
    Tsh_noise=cn.powerlaw_psd_gaussian(2,t5)*noise_T
    Tnh_noise=cn.powerlaw_psd_gaussian(2,t5)*noise_T
  elif noise_type=='mixed':
    white_noise_T=cn.powerlaw_psd_gaussian(0,t5)*noise_T/2.
    red_noise_T=cn.powerlaw_psd_gaussian(0,t5)*noise_T/2.
    Tsh_noise=white_noise_T+red_noise_T
    red_noise_T=cn.powerlaw_psd_gaussian(0,t5)*noise_T/2.
    Tnh_noise=white_noise_T+red_noise_T
  #
  #--monsoon noise
  monsoon_noise=cn.powerlaw_psd_gaussian(0,t5)*noise_monsoon
  #
  return Tsh_noise, Tnh_noise, monsoon_noise
#
#--main engine: the climate controller
def run_controller(t5,nbyr_irf,f,P,tau_nh_sh_upper,tau_nh_sh_lower,aod_strat_sh,aod_strat_nh,Tsh_noise,Tnh_noise,monsoon_noise):
  #
  Actors=P.keys()
  #
  #--time profiles of observation noise
  TSRM_noise_obs=np.random.normal(0,0.01,t5)
  TSRMnh_noise_obs=np.random.normal(0,0.01,t5)
  TSRMsh_noise_obs=np.random.normal(0,0.01,t5)
  monsoon_noise_obs=np.random.normal(0,1,t5)
  #
  #--define the PIDs and the emission min/max profiles
  PIDs={} ; emissmin={} ; emissmax={} ; emi_SRM={}
  #--loop on Actors
  for Actor in Actors:
    PIDs[Actor]={}
    emi_SRM[Actor]={}
    #--loop on emission points of Actor
    for emipoint in P[Actor]['emipoints']:
      #--initialise the PID
      PIDs[Actor][emipoint] = PID(P[Actor][Kp],P[Actor][Ki],P[Actor][Kd],setpoint=P[Actor][setpoint])
      #--initialise the emission arrays
      emi_SRM[Actor][emipoint]=[0.0]
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
  for t in range(t0,t5):
    #
    #--reference calculation with no SRM 
    #-----------------------------------
    TnoSRM, TnoSRMsh,TnoSRMnh,T0noSRMsh,T0noSRMnh,gsh,gnh = clim_sh_nh(TnoSRMsh,TnoSRMnh,T0noSRMsh,T0noSRMnh,{},aod_strat_sh,aod_strat_nh,nbyr_irf,\
                                                                       f=f[t],Tsh_noise=Tsh_noise[t],Tnh_noise=Tnh_noise[t], \
                                                                       tau_nh_sh_upper=tau_nh_sh_upper,tau_nh_sh_lower=tau_nh_sh_lower)
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
    for Actor in Actors:
       for emipoint in P[Actor]['emipoints']:
          if emipoint in emits:
             emits[emipoint] = [x + y for x,y in zip(emits[emipoint],emi_SRM[Actor][emipoint])]
          else:
             emits[emipoint] = emi_SRM[Actor][emipoint]
    #
    #--iterate climate model with emits as input
    TSRM, TSRMsh,TSRMnh,T0SRMsh,T0SRMnh,gsh,gnh = clim_sh_nh(TSRMsh,TSRMnh,T0SRMsh,T0SRMnh,emits,aod_strat_sh,aod_strat_nh,nbyr_irf,\
                                                             f=f[t],Tsh_noise=Tsh_noise[t],Tnh_noise=Tnh_noise[t])
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
      #--check for additional interactive stops
      stops=[stop for stop in P[Actor]['stops'] if type(stop)==type(0.0)]
      #--loop on emission points
      for emipoint in P[Actor]['emipoints']:
         #--checking for additional interactive limits if target is overshoot => 5-yr stop in SRM
         for stop in stops: 
             if t > t1:
                 if P[Actor][target]=='GMST' and TSRM <= stop: 
                     emissmin[Actor][t:t+5]=0.0 ; emissmax[Actor][t:t+5]=0.0
                 if P[Actor][target]=='NHST' and TSRMnh <= stop: 
                     emissmin[Actor][t:t+5]=0.0 ; emissmax[Actor][t:t+5]=0.0
                 if P[Actor][target]=='SHST' and TSRMsh <= stop: 
                     emissmin[Actor][t:t+5]=0.0 ; emissmax[Actor][t:t+5]=0.0
                 if P[Actor][target]=='monsoon' and monsoon >= -1*stop: 
                     emissmin[Actor][t:t+5]=0.0 ; emissmax[Actor][t:t+5]=0.0 
         #--setting limits on emissions for each Actor's PID
         PIDs[Actor][emipoint].output_limits = (emissmin[Actor][t],emissmax[Actor][t])
         #--append the emission arrays
         if P[Actor][target]=='GMST':
             emi_SRM[Actor][emipoint].append(PIDs[Actor][emipoint](TSRM+TSRM_noise_obs[t],dt=1))
         if P[Actor][target]=='NHST':
             emi_SRM[Actor][emipoint].append(PIDs[Actor][emipoint](TSRMnh+TSRMnh_noise_obs[t],dt=1))
         if P[Actor][target]=='SHST':
             emi_SRM[Actor][emipoint].append(PIDs[Actor][emipoint](TSRMsh+TSRMsh_noise_obs[t],dt=1))
         if P[Actor][target]=='monsoon':
             emi_SRM[Actor][emipoint].append(PIDs[Actor][emipoint](-1*monsoon+monsoon_noise_obs[t],dt=1))
  #
  #--change sign of emissions before plotting
  for Actor in Actors:
     for emipoint in P[Actor]['emipoints']:
         emi_SRM[Actor][emipoint] = [-1.*x for x in emi_SRM[Actor][emipoint]]
  #
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
  return emi_SRM, emissmin, g_SRM_nh,g_SRM_sh,T_noSRM_nh,T_noSRM_sh,T_SRM_nh,T_SRM_sh,monsoon_noSRM,monsoon_SRM
#
#--graphics
def plot_graphs(dirout,exp,pltshow,title,t5,f,P,Tnh_noise,Tsh_noise,monsoon_noise,emi_SRM,emissmin,\
                g_SRM_nh,g_SRM_sh,T_noSRM_nh,T_noSRM_sh,T_SRM_nh,T_SRM_sh,monsoon_noSRM,monsoon_SRM):
  #
  #--define filename
  filename='test'+exp+'.png'
  #
  Actors=P.keys()
  #
  #--basic plot with results
  title='Controlling global SAI'+title
  fig, axs = plt.subplots(3,2,figsize=(22,13))
  fig.suptitle(title,fontsize=16)
  plt.subplots_adjust(bottom=0.15)
  #
  axs[0,0].plot([t0,t5],[0,0],zorder=0,linewidth=0.4)
  axs[0,0].plot(f,label='GHG + volcanic RF',c='red')
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
     for emipoint in P[Actor]['emipoints']:
         axs[1,0].plot(emi_SRM[Actor][emipoint],linestyle='solid',c=colors[Actor])
         axs[1,0].scatter(range(t0,t5+1,10),emi_SRM[Actor][emipoint][::10],label='Emissions '+Actor+' '+emipoint,\
                          c=colors[Actor],marker=markers[emipoint],s=sizes[emipoint])
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
  axs[2,0].set_ylabel('Temp. ($^\circ$C)',fontsize=14)
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
  if pltshow: plt.show()
  #
  return
#
def plot1(t5,f):
  #--basic plot with results
  title='External climate forcing for experiment'
  fig=plt.figure(figsize=(8,6))
  plt.title(title,fontsize=16)
  plt.plot([t0,t5],[0,0],zorder=0,linewidth=0.4)
  plt.plot(f,label='GHG + volcanic RF',c='red')
  plt.legend(loc='upper left',fontsize=12)
  plt.ylabel('RF (Wm$^{-2}$)',fontsize=14)
  plt.xlim(t0,t5)
  plt.xticks(np.arange(t0,t5+1,25))
  plt.tick_params(size=14)
  plt.tick_params(size=14)
  return fig

def plot2(t5,Tsh_noise,Tnh_noise,monsoon_noise):
  title='Prescribed noise level'
  fig=plt.figure(figsize=(8,6))
  plt.title(title,fontsize=16)
  plt.plot([t0,t5],[0,0],zorder=0,linewidth=0.4)
  plt.plot(Tsh_noise,label='SHST noise',c='green')
  plt.plot(Tnh_noise,label='NHST noise',c='black')
  plt.plot(monsoon_noise/100.,label='Monsoon noise',c='red')
  plt.legend(loc='lower right',fontsize=12)
  plt.ylabel('Noise level',fontsize=14)
  plt.xlim(t0,t5)
  plt.xticks(np.arange(t0,t5+1,25))
  plt.tick_params(size=14)
  plt.tick_params(size=14)
  return fig
  #
def plot3(t5,P,emi_SRM,emissmin):
  title='Emissions per actor and per emission point'
  fig=plt.figure(figsize=(8,6))
  plt.title(title,fontsize=16)
  Actors=P.keys()
  for Actor in Actors:
     for emipoint in P[Actor]['emipoints']:
         plt.plot(emi_SRM[Actor][emipoint],linestyle='solid',c=colors[Actor])
         plt.scatter(range(t0,t5+1,10),emi_SRM[Actor][emipoint][::10],label='Emissions '+Actor+' '+emipoint,\
                     c=colors[Actor],marker=markers[emipoint],s=sizes[emipoint])
         plt.plot(-1*emissmin[Actor],linestyle='dashed',linewidth=0.5,c=colors[Actor])
  plt.legend(loc='upper left',fontsize=12)
  plt.ylabel('Emi (TgS yr$^{-1}$)',fontsize=14)
  plt.xlim(t0,t5)
  plt.xticks(np.arange(t0,t5+1,25))
  plt.tick_params(size=14)
  plt.tick_params(size=14)
  return fig
  #
def plot4(t5,g_SRM_sh,g_SRM_nh):
  title='SRM forcing'
  fig=plt.figure(figsize=(8,6))
  plt.title(title,fontsize=16)
  plt.plot(g_SRM_sh,label='SH SRM g',c='blue',linestyle='dashed')
  plt.plot(g_SRM_nh,label='NH SRM g',c='blue')
  plt.legend(loc='upper left',fontsize=12)
  plt.ylabel('RF SRM (Wm$^{-2}$)',fontsize=14)
  plt.xlim(t0,t5)
  plt.xticks(np.arange(t0,t5+1,25))
  plt.tick_params(size=14)
  plt.tick_params(size=14)
  return fig
  #
def plot5(t5,T_noSRM_sh,T_noSRM_nh,T_SRM_sh,T_SRM_nh):
  title='Temperature change'
  fig=plt.figure(figsize=(8,6))
  plt.title(title,fontsize=16)
  plt.plot(T_noSRM_sh,label='SH dT w/o SRM',c='red',linestyle='dashed',zorder=100)
  plt.plot(T_noSRM_nh,label='NH dT w/o SRM',c='red',zorder=100)
  plt.plot(T_SRM_sh,label='SH dT w SRM',c='blue',linestyle='dashed',zorder=0)
  plt.plot(T_SRM_nh,label='NH dT w SRM',c='blue',zorder=0)
  plt.plot([t0,t5],[0,0],c='black',linewidth=0.5)
  plt.legend(loc='upper left',fontsize=12)
  plt.xlabel('Years',fontsize=14)
  plt.ylabel('Temp. ($^\circ$C)',fontsize=14)
  plt.xlim(t0,t5)
  plt.xticks(np.arange(t0,t5+1,25))
  plt.tick_params(size=14)
  plt.tick_params(size=14)
  return fig
  #
def plot6(t5,monsoon_noSRM,monsoon_SRM):
  title='Monsoon change'
  fig=plt.figure(figsize=(8,6))
  plt.title(title,fontsize=16)
  plt.plot(monsoon_noSRM,label='monsoon w/o SRM',c='red',zorder=100)
  plt.plot(monsoon_SRM,label='monsoon w SRM',c='blue',zorder=0)
  plt.plot([t0,t5],[0,0],c='black',linewidth=0.5)
  plt.legend(loc='lower left',fontsize=12)
  plt.xlabel('Years',fontsize=14)
  plt.ylabel('Monsoon (%)',fontsize=14)
  plt.xlim(t0,t5)
  plt.xticks(np.arange(t0,t5+1,25))
  plt.tick_params(size=14)
  plt.tick_params(size=14)
  return fig
