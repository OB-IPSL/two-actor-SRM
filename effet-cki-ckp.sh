#!/bin/bash
listeexp=liste-exp-test.txt
\rm -Rf plots-*
d=plots-ref
mkdir $d
ckp=1.
cki=1.
titre=" ### référence"
ln -s $d plots
for exp in $(cat $listeexp) ; do
  python3 main.py --exp=$exp --cki=$cki --ckp=$ckp --load-noise bruit1.txt --app-title "$titre"
done
\rm -f plots

#####################################################
d=plots-kix2
mkdir $d
ckp=1.
cki=2.
ln -s $d plots
titre=" ### Kp=$ckp Ki=$cki"
for exp in $(cat $listeexp) ; do
  python3 main.py --exp=$exp --cki=$cki --ckp=$ckp --load-noise bruit1.txt --app-title "$titre"
done
\rm -f plots
exit 2
#############################################################
d=plots-kpd2
mkdir $d
ckp=0.5
cki=1.
ln -s $d plots
titre=" ### Kp=$ckp Ki=$cki"
for exp in $(cat $listeexp) ; do
  python3 main.py --exp=$exp --cki=$cki --ckp=$ckp --load-noise bruit1.txt --app-title "$titre"
done
\rm -f plots
\rm -f $d/test* $d/scenar*

#####################################################
d=plots-kid2
mkdir $d
ckp=1.
cki=0.5
ln -s $d plots
titre=" ### Kp=$ckp Ki=$cki"
for exp in $(cat $listeexp) ; do
  python3 main.py --exp=$exp --cki=$cki --ckp=$ckp --load-noise bruit1.txt --app-title "$titre"
done
\rm -f plots
\rm -f $d/test* $d/scenar*
############################################################

#d=plots-kpx10
mkdir $d
ckp=10.
cki=1.
ln -s $d plots
titre=" ### Kp=$ckp Ki=$cki"
for exp in $(cat $listeexp) ; do
  python3 main.py --exp=$exp --cki=$cki --ckp=$ckp --load-noise bruit1.txt --app-title "$titre"
done
\rm -f plots
\rm -f $d/test* $d/scenar*

#####################################################
d=plots-kix10
mkdir $d
ckp=1.
cki=10.
ln -s $d plots
titre=" ### Kp=$ckp Ki=$cki"
for exp in $(cat $listeexp) ; do
  python3 main.py --exp=$exp --cki=$cki --ckp=$ckp --load-noise bruit1.txt --app-title "$titre"
done
\rm -f plots
\rm -f $d/test* $d/scenar*
#############################################################
d=plots-kpd10
mkdir $d
ckp=0.1
cki=1.
ln -s $d plots
titre=" ### Kp=$ckp Ki=$cki"
for exp in $(cat $listeexp) ; do
  python3 main.py --exp=$exp --cki=$cki --ckp=$ckp --load-noise bruit1.txt --app-title "$titre"
done
\rm -f plots
\rm -f $d/test* $d/scenar*

#####################################################
d=plots-kid10
mkdir $d
ckp=1.
cki=0.1
ln -s $d plots
titre=" ### Kp=$ckp Ki=$cki"
for exp in $(cat $listeexp) ; do
  python3 main.py --exp=$exp --cki=$cki --ckp=$ckp --load-noise bruit1.txt --app-title "$titre"
done
\rm -f plots
\rm -f $d/test* $d/scenar*
############################################################
#
