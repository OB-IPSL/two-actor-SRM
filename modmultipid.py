#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
#Format python datetime: %Y-%m-%dT%H:%M:%S.%f 
# fmtdate=%Y-%m-%dT%H:%M:%S.%f"
# string => datetime object:
# tt=datetime.strptime(chaine,format)
import re
from sys import *
import sys
import os
import subprocess
import numpy as np
from numpy import sin,cos,exp,log,tan,sqrt,mean,std,pi,arctan,arcsin,arccos
from scipy import interpolate,integrate
import phys
from os.path import isfile,isdir
from ctypes import *
from struct import *
import h5py
import argparse
from datetime import *

emipoint2ic ={"60N":0,
              "30N":1,
              "15N":2,
              "eq":3,
              "15N":4,
              "30N":5,
              "60N":6}

ic2emipoint =["60N",
              "30N",
              "15N",
              "eq",
              "15N",
              "30N",
              "60N"]

# var2xs: fills the state vector with variables
def var2x(tsrm, tsrmnh, tsrmsh, moonsoon):
  x=np.zeros(4)
  x[0]=tsrm
  x[1]=tsrmnh
  x[2]=tsrmsh
  x[3]=moonsoon
  return x


target2jc={"GMST":0,
           "NHST":1,
           "SHST":2,
           "moonsoon":3}


# ns: size of state vector
ns=4
# nc: size of control vector
nc=len(ic2emipoint)



# class multipid
# - m = size of state vector
# - n = size of control vector 
# - xs[l] = setpoint for (l+1)-th state variable (= (l+1)-component of the state variable)
# - e:  e[l,it]=xs[l]-x[l,it] , x[i,it] being the value of the i-th component of the state vecto
#     r at time t[it]
# - t: time array t[it] = time at it-th instant
# - Kp,Ki,Kd: matrixes used to determine the control vector from the state Vector
# - (p=> proportional, i=> integral, d => derivate)
# - c[j] = \sum_{l=0}^{m-1} [ Kp[j,l]*e[l,it]
#                          + Ki[j,l]}*\sum_{jt=1}^{it} 0.5*(e[l,it]+e[l,it-1])*(t[jt]-t[jt-1])
#                          + Kd[j,l]*(e[l,it]-e[l,it-1])/(t[it]-t[it-1])]
#   Avec:
#   
# nt: number of times





class multipid:
  # m: size of the state vector
  # n: number of control variables
  # Kp,Ki,Kd,: dimension (m,n) = (ns,nc)
  # xs: vector of size m = setpoint 
  # dt: default value for the time step
  def __init__(self,m,n,xs,Kp,Ki,Kd,dt):
    self.m=m
    self.n=n
    self.xs=xs
    self.Kp=Kp
    self.Ki=Ki
    self.Kd=Kd
    self.t=[]
    
# addstatevector: add the state vector at current timestep
# x:  state vector if size m
# dt: timestep. If <0, the  default timestep self.dt will be used
# 
  def addstatevector(self,x,dt=-1):
    if dt>0:
      self.t.append(self.t[-1]+dt)
    else:
      self.t.append(self.t[-1]+self.dt)
    if self.nt==0:
      self.e=np.zeros([self.m,1])
      self.eint=np.zeros[self.m]
      self.e[:,0]=self.xs-np.array(x)
    else:
      self.e=np.concatenate(self.e,self.xs-np.array(x),axis=1)
      self.eint=self.eint+0.5*(self.e[:,-2]+self.e[:,-1])*(t[-1]-t[-2])
    self.nt=self.nt+1
# getcontrol(): computes the control variables from the state variables
#               at the times t[0],...,t[self.nt-1]
  def state2control(self):
    c=np.zeros(n)
    for j in range(0,n):
      c[j]=0.
      for l in range(0,m):
        c[j]=c[j]+self.Kp[j,l]*e[m,-1]+ \
                  self.Ki[j,m]*eint[m]+ \
                  self.Kd[j,m]*(e[m,-1]-e[m,-2])/(t[-1]-t[-2])

    return c

  

