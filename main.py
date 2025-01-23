from simple_pid import PID
import numpy as np
import random
import argparse
import sys, os
from myclim import initialise_aod_responses
from engine import set_title, set_emipoints, initialise_forcing, set_noise, run_controller
from engine import plot_graphs, plot1, plot2, plot3, plot4, plot5, plot6
from experiments import set_experiment
import matplotlib.pyplot as plt
import re
from socket import gethostname
from commun import hote
from modnetcdf import ecrit1d
from modmultipid import multipid
import netCDF4 as nc4

sys.path.insert(0,".")
#--call script as: python test.py --exp=4a --noise=mixed

global hote
hostname=gethostname()
m=re.search("^spiritx[0-9]?[.]",hostname)
m2=re.search("^spirit[0-9]?[.]",hostname)
if m:
  hote="spirit"
elif m2:
  hote="spiritx"
else:
  hote=hostname

parser = argparse.ArgumentParser()
parser.add_argument('--exp', type=str, default='4a', help='experiment number')
# file: noise read in file. Default: noise.txt. Otherwise: noise_file argument
parser.add_argument('--noise', type=str, default='mixed', choices=['white','red','mixed','file'],help='Noise type')
parser.add_argument('--noise_file', type=str, default='noise.txt',help='Noise file')
parser.add_argument('--write_noise', action='store_true', default=False)
parser.add_argument('--ncfile', default='out.nc')

args = parser.parse_args()
exp=args.exp
noise_type=args.noise
if args.noise!='file':
  args.noise_file=''

#--initialise PID controller for each actors
#--PID(Kp, Ki, Kd, setpoint)
#--Kp: proportional gain (typically 0.8 (TgS/yr)/°C    for T target and 0.08 (TgS/yr)/% monsoon    for monsoon change target)
#--Ki: integral gain     (typically 0.6 (TgS/yr)/°C/yr for T target and 0.06 (TgS/yr)/% monsoon/yr for monsoon change target)
#--Kd: derivative gain   (typically 0)
#--type: GMST (global mean surf temp), NHST (NH surf temp), SHST (SH surf temp), monsoon
#--setpoint: objective (temperature change in K, monsoon change in %)
#--emimin, emimax: bounds of emissions (in TgS/yr)
#--emipoints: emission points: 30N, 15N, Eq, 15S, 30S
#--t1: start of ramping up SRM intervention
#--t2: end of ramping up SRM intervention
#--t5: time of end of SRM intervention (in years)
#--stops: periods of SRM interruption, list of tuples (t3,t4) and targets exceeded
#--fmax: max value for GHG forcing (Wm-2)
#--noise: noise level for T0 (in K)
#--directory for plots
dirout='plots/'
if not os.path.exists(dirout): os.makedirs(dirout)
#--show plots while running
pltshow=True
#--period of integration
t5=200
#--volcano
volcano=True
#--max GHG forcing
fmax=4.0
#--noise level
noise_T=0.15       #--in K
noise_monsoon=5.   #--in % change
#--interhemispheric timescales (in years)
tau_nh_sh_upper=20.
tau_nh_sh_lower=20.
#
#--define experiment among predefined experiments
P = set_experiment(exp)
#
#--print Actors and their properties on screen
title = set_title(P)
#
#--create a list of all emission points
emipoints = set_emipoints(P)
#
#--initialise impulse response functions
aod_strat_sh, aod_strat_nh, nbyr_irf = initialise_aod_responses()
#
#--initialise GHG forcing scenario, increases linearly for 100 yrs then constant then decrease slowly
f = initialise_forcing(t5,fmax,volcano)
#
#--time profiles of climate noise
Tsh_noise, Tnh_noise, monsoon_noise = set_noise(t5,noise_T,noise_monsoon,noise_type,args.noise_file)


Tsh_noise[:]=0.   # test jb
Tnh_noise[:]=0.   # test jb
monsoon_noise[:]=0.   # test jb
if args.write_noise:
  print("t5 = {:d} len(tsh_noise) = {:d}".format(t5,Tsh_noise.size))
  f=open(args.noise_file,'w')
  for i in range(0,t5):
    f.write('{:22.14e} {:22.14e} {:22.14e}\n'.format(Tsh_noise[i],
                                                     Tnh_noise[i],
                                                     monsoon_noise[i]))
  f.close()
#
#--call controller
emi_SRM, emissmin, g_SRM_nh,g_SRM_sh,T_noSRM_nh,T_noSRM_sh,T_SRM_nh,T_SRM_sh,monsoon_noSRM,monsoon_SRM = \
              run_controller(t5,nbyr_irf,f,P,tau_nh_sh_upper,tau_nh_sh_lower,aod_strat_sh,aod_strat_nh,Tsh_noise,Tnh_noise,monsoon_noise)


fo = nc4.Dataset(args.ncfile, "w", format="NETCDF4")
fo.description="Output of two-actors"
fo.experiment=exp
#t=f.createVariable(experiment","f4",("x","y"))
fo.createDimension('t', size=t5)
#
# ecrit1d(fo,name,dtype,dimname,data,description=""):
ecrit1d(fo,"Tnh_noise",'f8',"t",Tnh_noise)
ecrit1d(fo,"Tsh_noise","f8","t",Tsh_noise)
ecrit1d(fo,"monsoon_noise","f8","t",monsoon_noise)
for acteur in emi_SRM:
  for emipoint in emi_SRM[acteur]:
    nomvar="emi_SRM_{:}_{:}".format(acteur,emipoint)
    ecrit1d(fo,nomvar,"f8","t",emi_SRM[acteur][emipoint][1:])

# pour avoir la même taille que pouqr les autres tableaux
# on n'écrit pas emi[acteur][emipoint][0], qui vaut 0
#ecrit1d(fo,"emi_SRM","f8","t",emi_SRM)

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
#--make plots
plot_graphs(dirout,exp,pltshow,title,t5,f,P,Tnh_noise,Tsh_noise,monsoon_noise,emi_SRM,emissmin,\
            g_SRM_nh,g_SRM_sh,T_noSRM_nh,T_noSRM_sh,T_SRM_nh,T_SRM_sh,monsoon_noSRM,monsoon_SRM)

# --redo plots one by one
#fig=plot1(t5,f)
#plt.show()
#fig=plot2(t5,Tsh_noise,Tnh_noise,monsoon_noise)
#plt.show()
#fig=plot3(t5,P,emi_SRM,emissmin)
#plt.show()
#fig=plot4(t5,g_SRM_sh,g_SRM_nh)
#plt.show()
#fig=plot5(t5,T_noSRM_sh,T_noSRM_nh,T_SRM_sh,T_SRM_nh)
#plt.show()
#fig=plot6(t5,monsoon_noSRM,monsoon_SRM)
#plt.show()
