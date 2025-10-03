#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
import colorednoise as cn
import numpy as np
#

#--set time profiles of climate noise
def set_noise(t5,noise_T,noise_monsoon,noise_type,noise_file=''):
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
  elif noise_type=='file':
    mn=np.loadtxt(noise_file)
    nt=(mn.shape)[0]
    if nt<t5:
      stderr.write('Error: only {:d} lines in noise file, {:d} needed.\nStop.'.format(nt,t5))
      exit(1)
    Tsh_noise=mn[:,0]
    Tnh_noise=mn[:,1]
    monsoon_noise=mn[:,2]
  #
  #--monsoon noise
  if noise_type!='file':
    monsoon_noise=cn.powerlaw_psd_gaussian(0,t5)*noise_monsoon
  #
  return Tsh_noise, Tnh_noise, monsoon_noise
a=5
n=100000

print("bruit blanc")
y=cn.powerlaw_psd_gaussian(0,n)*a
print("moyenne : {:12.4e}".format(np.mean(y)))
print("stdev : {:12.4e}".format(np.std(y)))
print()
print("bruit rouge")
y=cn.powerlaw_psd_gaussian(2,n)*a
print("moyenne : {:12.4e}".format(np.mean(y)))
print("stdev : {:12.4e}".format(np.std(y)))

print()

print("bruit mélangé (red + white)")
y1=cn.powerlaw_psd_gaussian(0,n)*a*0.5
y2=cn.powerlaw_psd_gaussian(2,n)*a*0.5
y=y1+y2
print("moyenne : {:12.4e}".format(np.mean(y)))
print("stdev : {:12.4e}".format(np.std(y)))

print()
print("bruit mélangé utilisé par OB (white + white)")
y1=cn.powerlaw_psd_gaussian(0,n)*a*0.5
y2=cn.powerlaw_psd_gaussian(0,n)*a*0.5
y=y1+y2
print("moyenne : {:12.4e}".format(np.mean(y)))
print("stdev : {:12.4e}".format(np.std(y)))
