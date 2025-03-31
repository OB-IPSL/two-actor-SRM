exp="2m"
xs=np.zeros(4)
targets={"NHST":0.,
         "SHST":3.}
for tar in targets:
  xs[target2js[tar]]=targets[tar]
  poids[target2js[tar]]=1.
tau=1.e9 #  test
emimaxl=20.
emipoint1='60N'
emipoint2='60S'
A={'Kp':0.8, 'Ki':0.6, 'Kd':0.0,'type':'NHST',    'setpoint':0.0, 'emimin':0.0,'emimax':emimaxl,'emipoints':[emipoint1],'t1':50,'t2':70,'stops':[]}
dicKp={'NHST': {emipoint1:0.8},
       'SHST': {emipoint2:0.8},
       'GMST': {},
       'monsoon' : {}}
dicKi={'NHST': {emipoint1:0.6},
       'SHST': {emipoint2:0.6},
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
print("aremipoints2",aremipoints2)

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
tau_nh_sh_upper=20.
tau_nh_sh_lower=20.

# ---------------- noise related parameters ------------------------------------
# noise_type type of noise. Possible values: "red","white" ou "mixed"
noise_type='red'
#--noise level
noise_T=0.  # 0.15       #--in K
noise_monsoon=0. # 5.   #--in % change


# noisefilei: file with noise input (temperatures and moonson)
#             takes precedence over all noise parameters.
#noisefilei="noise-2mn.nc"
noisefilei=""
# noisefileo: file to save noise.
noisefileo="noise-zero.nc"

