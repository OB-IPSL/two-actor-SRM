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

compteurm=0
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
  # boundedint: boolean. If true, Ki
  #                      
  def __init__(self,ns,nc,xs,Kp,Ki,Kd,poids=[],boundedint=True,dt=1.):
    self.ns=ns
    self.nc=nc
    self.xs=xs
    self.Kp=Kp
    self.Ki=Ki
    self.Kd=Kd
    self.eint=np.zeros(self.ns)
    self.t=[]
    self.nt=0
    self.dt=dt
    self.m=self.ns
    self.n=self.nc
    self.cmin=-1.e99*np.ones(self.nc)
    self.cmax=1.e99*np.ones(self.nc)
    self.boundedint=boundedint
    if poids:
      poids=np.array(poids)
      if poids.size!=self.ns:
        print("Erreur: nombre de variables {:d} taille du vecteur des poids {:d}".format(poids.size,
                                                                                         ns))
        exit(1)
      self.poids=poids#/np.sum(poids)
    else:
      self.poids=np.ones(ns)/ns


  # setlimits: sets min and max values for output control variables
  # 
  # cmin: cmin[i] = min value for c[i]
  # cmax: cmax[i] = max value for c[i]
  # c = vector of control variables, returned by state2control 
  def setoutlimits(self,cmin,cmax):
    self.cmin=cmin*np.ones(self.nc)
    self.cmax=cmax*np.ones(self.nc)
  def setoutminmax(self,cmin,cmax):
     self.setoutlimits(cmin,cmax) 
# state2control(): computes the control variables from the state variables
#               at the times t[0],...,t[self.nt-1]
# xs:  state vector of size m
# t: current time
  def state2control(self,xs,t):
    global compteurm
    compteurm=compteurm+1 
    #print("testj2: eint",self.eint)
    self.t.append(t)
    deltaeint=np.zeros(self.ns)
    if self.nt==0:
      self.e=np.zeros([self.ns,1])
      self.eint=np.zeros(self.ns)
      self.e[:,0]=self.xs-np.array(xs)
    else:
      self.e=np.concatenate((self.e,np.reshape(self.xs-np.array(xs),(ns,1))),axis=1)
      #deltaeint=0.5*(self.e[:,-2]+self.e[:,-1])*(self.t[-1]-self.t[-2])
      deltaeint=self.e[:,-1]*self.dt
    self.nt=self.nt+1




    c=np.zeros(self.nc)
    e=self.e
    alpha=1.
    print("testjc t,c[2]= {:7.0f} {:8.3f}".format(t,c[2]))
    print("xs",xs)
    js=2
    print("avant t,eint",t,self.eint[js]) 
    js0=1
    
    for jc in range(0,self.nc):
      c[jc]=0.
      dcp=0.
      dcd=0.
      dci=0.
      for js in range(0,self.ns):
        c[jc]=c[jc]+self.poids[js]*self.Kp[jc,js]*e[js,-1]+ \
                  +self.poids[js]*self.Ki[jc,js]*(self.eint[js]+deltaeint[js])
        if self.nt>=2:
          c[jc]=c[jc]+self.poids[js]*self.Kd[jc,js]*(e[js,-1]-e[js,-2])/(self.t[-1]-self.t[-2])

        ddcp=self.Kp[jc,js]*e[js,-1]*self.poids[js]
        dcp=dcp+ddcp # self.Kp[jc,js]*e[js,-1]*self.poids[js]
        if (js==1) and (jc==2):
          print("uu2m dd error,dt,ki  {:12.4f} {:12.4f} {:12.4f}".format(e[js,-1],self.dt,self.Ki[jc,js]))
        ddci=self.Ki[jc,js]*(self.dt*e[js,-1])*self.poids[js]
        if (js==1) and (jc==2):
          print("uu2m inc {:12.4f}".format(ddci))
        dci=dci+ddci
        if (js==1) and (jc==2):

          print("uuu m: t,dcp,dci ={:d} {:12.4f} dci={:12.4f}".format(t,dcp,dci))
        if self.nt>=2:
          dcd=dcd+self.poids[js]*self.Kd[jc,js]*(e[js,-1]-e[js,-2])/(self.t[-1]-self.t[-2])
        else:
          dcd=0
      if jc==2:
        print("uu2m inc {:12.4f}".format(dci))
      alphap=1.
      alpham=1.
      #if self.boundedint:
      #  print("testii mult dci,cmin,cmax {:12.4e} {:12.4e} {:12.4e}".format(dci,self.cmin[jc],self.cmax[jc]))
      #  if dci>self.cmax[jc]:
      #    alphap=self.cmax[jc]/dci
      #  if dci<self.cmin[jc]:
      #    alpham=abs(self.cmin[jc]/dci)
      #  if min(alphap,alpham)<alpha:
      #    alpha=min(alphap,alpham)
      if jc==2:
        dci0=dci
        e0=self.e[js0,-1]
        
      if jc==2:     
        print("testbb: mult jc={:d}(prop,int,der) = {:-12.4e} {:-10.4e} {:-10.4e}".format(jc,
                                                                                         dcp,
                                                                                         dci,
                                                                                         dcd))

    print("uu2m inc {:12.4f}".format(dci0))
    #print("testjc t,t,c p2= {:7.0f} {:8.3f}".format(t,c[2]))

    print("testii mult avant  Ki*eint={:12.4e}".format(self.Ki[2,1]*(self.eint[2]+deltaeint[2])))
    print("alpha",alpha)
    print("uu2 m: compteur,e,deltaeint,eint {:d} {:12.4f} {:12.4f} {:12.4f} {:12.4f}\n".format(compteurm,
                                                                                 self.e[js0,-1],
                                                                        dci0,
                                                                        self.eint[js0]+deltaeint[js0],
                                                                        self.cmin[jc]))


    self.eint=self.eint+alpha*deltaeint
    print("uu2 m: compteur,e,deltaeint,eint {:d} {:12.4f} {:12.4f} {:12.4f} {:12.4f}\n".format(compteurm,
                                                                                 self.e[js0,-1],
                                                                        dci0,
                                                                        self.eint[js0],
                                                                        self.cmin[jc]))


    print("testii mult après Ki*eint={:12.4e}".format(self.Ki[2,1]*self.eint[2]))
    for jc in range(0,nc):

#      print("jc={:d} c={:12.4e} self.cmin={:12.4e} self.cmax={:12.4e}".format(jc,
#                                                                          c[jc],
#                                                                          self.cmin[jc],
#                                                                          self.cmax[jc]))

      #if jc==2:
      #  print("testjc t,t,cmin   = {:7.0f} {:8.3f}".format(t,self.cmin[jc]))
      #  print("testjc t,t,cmax   = {:7.0f} {:8.3f}".format(t,self.cmax[jc]))
      #  print("testjc t,t,c avant= {:7.0f} {:8.3f}".format(t,c[jc]))
      if c[jc]<self.cmin[jc]:
        c[jc]=self.cmin[jc]

      if c[jc]>self.cmax[jc]:
        c[jc]=self.cmax[jc]

      #if jc==2:
      #  print("testjc t,t,c après= {:7.0f} {:8.3f}".format(t,c[jc]))
    fmt="cc: " + c.size* " {:10.2e}"+"\n"
    print(fmt.format(*c))

    print("apres t,eint",t,self.eint[js]) 
    return c

  

