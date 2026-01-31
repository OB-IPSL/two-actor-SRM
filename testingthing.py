import streamlistfile as slf

results = [{'Actor': 1, 'type': 'GMST', 'emipoints': ['15N', '15S'], 'setpoint': 0.0}, 
           {'Actor': 2, 'type': 'NHST', 'emipoints': ['eq', '15N'], 'setpoint': 0.0}]

added_entries_temp = {'Kp':0.8, 'Ki':0.6, 'Kd':0.0,'emimin':0.0,'emimax':10.0,'t1':50,'t2':70,'stops':[]}
added_entries_mons = {'Kp':0.08,'Ki':0.06,'Kd':0.0,'emimin':0.0,'emimax':10.0,'t1':50,'t2':70,'stops':[]}

P = {}

for item in results:
    Actor = item['Actor']
    copied_item = item.copy()
    copied_item.pop('Actor', None)
    if copied_item['type'] == "monsoon":
        copied_item.update(added_entries_mons)
    else:
        copied_item.update(added_entries_temp)
    P[Actor] = copied_item
    




print(P)