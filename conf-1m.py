exp="1m"
xs=np.zeros(4)
targets={"NHST":0.}
for tar in targets:
  xs[target2js[tar]]=targets[tar]
  poids[target2js[tar]]=1.
  
noise_T=0.
noise_monsoon=0.
tau=1.e9 #  test
emimaxl=20.
emipoint1='60S'
A={'Kp':0.8, 'Ki':0.6, 'Kd':0.0,'type':'NHST',    'setpoint':0.0, 'emimin':0.0,'emimax':emimaxl,'emipoints':[emipoint1],'t1':50,'t2':70,'stops':[]}
dicKp={'NHST': {emipoint1:0.8},
       'SHST': {},
       'GMST': {},
       'monsoon' : {}}
dicKi={'NHST': {emipoint1:0.6},
       'SHST': {},
       'GMST': {},
       'monsoon' : {}}
dicKd={'NHST': {},
       'SHST': {},
       'GMST': {},
       'monsoon' : {}}
aremipoints2 =[]
for dic in [dicKp,dicKi,dicKd]:
  for tt in dic:
    for emip in dic[tt]:
      if not emip in aremipoints2:
        aremipoints2.append(emip)
tau_nh_sh_upper=tau
tau_nh_sh_lower=tau

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

