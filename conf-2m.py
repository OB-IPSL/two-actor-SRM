exp="2m"

xs=np.zeros(4)
targets={"NHST":0.,
         "SHST":3.}
for tar in targets:
  xs[target2js[tar]]=targets[tar]
  poids[target2js[tar]]=1.
emimaxl=20.
emipoint1='60N'
emipoint2='60S'
A={'type':'NHST',    'setpoint':0.0, 'emimin':0.0,'emimax':emimaxl,'emipoints':[emipoint1],'t1':50,'t2':70,'stops':[],

   'dicKp':{'NHST': {emipoint1:0.8},
       'SHST': {emipoint2:0.8},
       'GMST': {},
       'monsoon' : {}},
   'dicKi':{'NHST': {emipoint1:0.6},
       'SHST': {emipoint2:0.6},
       'GMST': {},
       'monsoon' : {}},
   'dicKd':{'NHST': {},
       'SHST': {},
       'GMST': {},
       'monsoon' : {}}
}
aremipoints2 =[]
for clef1 in ['dicKp','dicKi','dicKd']:
  dic=A[clef1]
  for tt in dic:
    for emip in dic[tt]:
      if not emip in aremipoints2:
        aremipoints2.append(emip)
print("aremipoints2",aremipoints2)


# Paramètres du modèle physique




#################################################
# output parameters
# outnc: output netCDF file
# Default value: out-EXP.nc EXP = value of exp parameter
#outnc="out-2m.nc"
# outpdf: output PDF file
# Default value: out-EXP.pdf EXP = value of exp parameter
#outpdf="sortie-2m}.pdf".format(exp)

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

# --fmax: max value for GHG forcing (Wm-2)
fmax=8.0
#noise_monsoon=1.  #--in % change
#--interhemispheric timescales (in years)
# 1.e9: valeur irréaliste destinée à découpler thermiquement les  2 hémisphères.
tau_nh_sh_upper=1.e9 # va
tau_nh_sh_lower=1.e9

# ---------------- noise related parameters ------------------------------------
 #noise added to state variables at each time step
# noise_type type of noise. Possible values: "red","white" ou "mixed"
noise_type='red'
noise_T=0.15       #--in K
noise_monsoon=5.   #--in % change


# observation noises: the value of these noises is added to the state variables
#   before they are fed into the controller. They have not effect!
#   on the state variables.  
#TSRM_noise_obs_std : standard deviation of TSRM observation noise.
#                       mean value: 0
TSRM_noise_obs_std=0. # 1.e-2
#TSRMnh_noise_obs_std : standard deviation of TSRMnh observation noise.
#                       mean value: 0
TSRMnh_noise_obs_std=0. # 1.e-2
#TSRMsh_noise_obs_std : standard deviation of TSRMsh observation noise.
#                       mean value: 0
TSRMsh_noise_obs_std=0. # 1.e-2
# monsoon_noise_obs_std:  standard deviation of monsoon observation noise.
monsoon_noise_obs_std=0. # 1


# noisefilei: file with noise input (temperatures and moonson)
#             takes precedence over all noise parameters.
noisefilei="noise-2mn.nc"
# noisefileo: file to save noise.
noisefileo="noise-zero.nc"

