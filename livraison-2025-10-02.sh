#!/bin/bash
#for exp in 1a 11a   ;  do
#  python3 effet-cki-ckp.py --noise bruit1.txt -m --factor 2  --exp=$exp -o exp-${exp}-facteur-2.pdf
#done
#for exp in 4c 24c ; do 
#  python3 effet-cki-ckp.py --noise bruit1.txt --monsoon  --factor 2  --exp=$exp -o exp-${exp}-facteur-2.pdf
#done
python3 compare-exp.py --noise bruit1.txt -o comp-1a-11a.pdf  1a 11a 
python3 compare-exp.py --noise bruit1.txt -o comp-4c-24c.pdf  4c 24c 
#\rm out*.pdf
