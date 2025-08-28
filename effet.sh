#!/bin/bash
d=plots-test
mkdir $d
ckp=0.
cki=0.
ln -s $d plots
for exp in 4a; do
  python3 main.py --exp=$exp --cki=$cki --ckp=$ckp
done
\rm -f plots

