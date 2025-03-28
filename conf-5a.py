exp="5a"
A={'Kp':0.8, 'Ki':0.6, 'Kd':0.0,'type':'GMST','setpoint':0.0,'emimin':0.0,'emimax':10.0,'emipoints':['eq'],'t1':50,'t2':70,'stops':[]}
B={'Kp':0.9, 'Ki':0.5, 'Kd':0.0,'type':'GMST','setpoint':0.0,'emimin':0.0,'emimax':10.0,'emipoints':['eq'],'t1':50,'t2':70,'stops':[]}
-two actors with same targets on GMST but one stop for A

#################################################



#--directory for plots
dirout='plots/'
#--show plots while running
pltshow=False
#--if non empty, output PDF file.


#--period 
t0=0 ; t5=200
#--volcano
volcano=False
#--max GHG forcing
fmax=8.0
#--noise level
noise_T=0.15       #--in K
noise_monsoon=5.   #--in % change
#noise_monsoon=1.  #--in % change
#--interhemispheric timescales (in years)
tau_nh_sh_upper=20.
tau_nh_sh_lower=20.


# noisefilei: file with noise input (temperatures and moonson)
#             takes precedence over all noise parameters.
noisefilei="noise-2mn.nc"
#noisefilei=""
# noisefileo: file to save noise.
noisefileo="noise-o.nc"

