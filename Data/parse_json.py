import json
import os
import pandas as pd

directory = 'JsonAll'
listyboi = []
for filename in os.listdir(directory):
    with open(directory + '/' + 'filename', 'r') as fileboi:
        jason = json.load(fileboi)
    listyboi.extend(jason[data])

print(len(listyboi))

wowdf = pd.DataFrame.fromrecords(listyboi)

wowdf.to_csv('wowies.csv')