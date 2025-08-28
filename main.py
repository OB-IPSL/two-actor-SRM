from simple_pid import PID
import numpy as np
import random
import argparse
import sys, os
from myclim import initialise_aod_responses
from engine import set_title, set_emipoints, initialise_forcing, set_noise, run_controller
from engine import plot_graphs, plot_paper, plot1, plot2, plot3, plot4, plot5, plot6
from experiments import set_experiment
import matplotlib.pyplot as plt

#--call script as: python test.py --exp=4a --noise=mixed

parser = argparse.ArgumentParser()
parser.add_argument('--exp', type=str, default='4a', help='experiment number')
parser.add_argument('--noise', type=str, default='mixed', choices=['white','red','mixed'],help='Noise type')
parser.add_argument('--ckp', default=1.,type=float,help='multiplicative factor for Kp')
parser.add_argument('--cki', default=1.,type=float,help='multiplicative factor for ki')
parser.add_argument('-s', action='store_true',help='plots graphs interactively')
group = parser.add_mutually_exclusive_group()
group.add_argument('--save-noise', action='store',
                   metavar='FILE',help='save noises (NH,SH and monsoon) in FILE')
group.add_argument('--load-noise', action='store',
                   metavar='FILE',help='load noises (NH,SH and monsoon) from FILE')
args = parser.parse_args()
exp=args.exp
noise_type=args.noise

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
pltshow=args.s
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
P = set_experiment(exp,args.ckp,args.cki)
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
if args.load_noise:
  print("loading noise from " + args.load_noise)
  m=np.loadtxt(args.load_noise,skiprows=4)
  Tsh_noise=m[:,0]
  Tnh_noise=m[:,1]
  monsoon_noise=m[:,2]
else:
  Tsh_noise, Tnh_noise, monsoon_noise = set_noise(t5,noise_T,noise_monsoon,noise_type)
  if args.save_noise:
    print("saving noise to " + args.save_noise)
    f=open(args.save_noise,"w")
    n=len(Tsh_noise)
    f.write('''Column 1: year
  Column 2: Tsh_noise (K)
  Column 3: Tnh_noise (K)
  Column 4: monsoon noise (K)
  ''')
    for i in range(0,n):
      f.write('{:4d} {:22.14e} {:22.14e} {:22.14e}\n'.format(i,
                                                             Tsh_noise[i],
                                                             Tnh_noise[i],
                                                             monsoon_noise[i]))
    f.close()

#
#--call controller
emi_SRM, emissmin, g_SRM_nh,g_SRM_sh,T_noSRM_nh,T_noSRM_sh,T_SRM_nh,T_SRM_sh,monsoon_noSRM,monsoon_SRM = \
              run_controller(t5,nbyr_irf,f,P,tau_nh_sh_upper,tau_nh_sh_lower,aod_strat_sh,aod_strat_nh,Tsh_noise,Tnh_noise,monsoon_noise)
#
#--make plots
plot_graphs(dirout,exp,pltshow,title,t5,f,P,Tnh_noise,Tsh_noise,monsoon_noise,emi_SRM,emissmin,\
            g_SRM_nh,g_SRM_sh,T_noSRM_nh,T_noSRM_sh,T_SRM_nh,T_SRM_sh,monsoon_noSRM,monsoon_SRM)
#
#--redo plots one by one
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
#
#--make plots for the paper
plot_paper(dirout,exp,pltshow,title,t5,f,P,Tnh_noise,Tsh_noise,monsoon_noise,emi_SRM,emissmin,\
            g_SRM_nh,g_SRM_sh,T_noSRM_nh,T_noSRM_sh,T_SRM_nh,T_SRM_sh,monsoon_noSRM,monsoon_SRM)
#
