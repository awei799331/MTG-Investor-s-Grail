import json
import os
import pandas as pd

directory = 'JsonAll'
listyboi = []
for filename in os.listdir(directory):
    with open(directory + '/' + filename, 'r+', encoding='utf8') as fileboi:
        jason = json.load(fileboi)
    listyboi.extend(jason['data'])


wowdf = pd.DataFrame.from_records(listyboi)

#for index, row in wowdf.itertuples():


wowdf.to_csv('wowies.csv')