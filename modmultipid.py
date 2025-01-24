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

emipoint2jc ={"60N":0,
              "30N":1,
              "15N":2,
              "eq":3,
              "15S":4,
              "30S":5,
              "60S":6}

ic2emipoint =["60N",
              "30N",
              "15N",
              "eq",
              "15S",
              "30S",
              "60S"]

# var2xs: fills the state vector with variables
def var2x(tsrm, tsrmnh, tsrmsh, monsoon):
  x=np.zeros(4)
  x[0]=tsrm
  x[1]=tsrmnh
  x[2]=tsrmsh
  x[3]=monsoon
  return x


target2js={"GMST":0,
           "NHST":1,
           "SHST":2,
           "monsoon":3}

type2js=target2js
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
#   Kp(nc,ns)
# - (p=> proportional, i=> integral, d => derivate)
# - c[ic] = \sum_{js=0}^{m-1} [ 
#                         Kp[ic,js]*e[js,it]
#                       + Ki[ic,js]}*\sum_{ict=1}^{it} 0.5*(e[js,it]+e[js,it-1])*(t[ict]-t[ict-1])
#                       + Kd[ic,js]*(e[js,it]-e[js,it-1])/(t[it]-t[it-1])]
#                        ]
#   Avec:
#   
# nt: number of times





class multipid:
  # ns: size of the state vector
  # nc: number of control variables
  # Kp,Ki,Kd,: dimension = (nc,ns)
  # xs: vector of size m = setpoint 
  # dt: default value for the time step
  def __init__(self,ns,nc,xs,Kp,Ki,Kd,dt=-1.):
    self.ns=ns
    self.nc=nc
    self.xs=xs
    self.Kp=Kp
    self.Ki=Ki
    self.Kd=Kd
    self.t=[]
    self.nt=0
    self.m=self.ns
    self.n=self.nc

# addstatevector: add the state vector at current timestep
# x:  state vector if size m
# dt: timestep. If <0, the  default timestep self.dt will be used
# 
  def addstatevector(self,x,t):
    self.t.append(t)
    if self.nt==0:
      self.e=np.zeros([self.ns,1])
      self.eint=np.zeros(self.ns)
      self.e[:,0]=self.xs-np.array(x)
    else:
      self.e=np.concatenate(self.e,self.xs-np.array(x),axis=1)
      self.eint=self.eint+0.5*(self.e[:,-2]+self.e[:,-1])*(t[-1]-t[-2])
    self.nt=self.nt+1

# state2control(): computes the control variables from the state variables
#               at the times t[0],...,t[self.nt-1]
  def state2control(self):
    c=np.zeros(self.nc)
    e=self.e
    eint=self.eint
    for jc in range(0,self.nc):
      c[jc]=0.
      for js in range(0,self.ns):
        c[jc]=c[jc]+self.Kp[js,jc]*e[js,-1]+ \
                  self.Ki[jc,js]*eint[js]
        if self.nt>=2:
          c[jc]=c[jc]+self.Kd[jc,js]*(e[js,-1]-e[js,-2])/(t[-1]-t[-2])


    return c

  

