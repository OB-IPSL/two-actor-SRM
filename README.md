README two-actor-SRM  

Authors: Olivier Boucher, 2023, 2024  
         Anni Määttänen  
         Thibaut Lurton (IPSL-CM6A-LR experiments)  
         Omar Doutriaux and Krish Khotari (streamlit interface)  

runs on python 3  

Requires package simple-pid  
https://pypi.org/project/simple-pid/  
which can be installed as  
pip install simple-pid  

two-actor-SRM can be run through  

1/ a line command  

main.py  = simple test of the climate model and 1, 2, or 3 global actors for SRM using predefined experiments

python main.py --exp=4a --noise=mixed


2/ a streamlit user interface  

Requires package streamlit  
https://streamlit.io/  
which can be installed as  
pip install streamlit   
pip install altair==4.0  
Depending on your system, you need to set up the path for your streamlit executable  
On spirit, I can execute streamlit from ~/.local/bin/streamlit  

streamlit run stream.py   
