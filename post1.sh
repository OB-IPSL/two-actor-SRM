#!/bin/bash
commande="pdftk "
for x in 0 20 50 ; do
  pdf=t-emiss-kp${x}.pdf 
  python3 trace-temiss.py  --loc=9 --title="kp=${x}" --tmin=0 --tmax=40  -o$pdf  out-1a-14-kp${x}.nc 
  commande="$commande $pdf"
done
$commande cat  output touskp.pdf
echo $commande
