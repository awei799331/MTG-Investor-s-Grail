import json
import os
import pandas as pd
import numpy as np
import sadness

directory = 'JsonAll'
listyboi = []
for filename in os.listdir(directory):
    with open(directory + '/' + filename, 'r+', encoding='utf8') as fileboi:
        jason = json.load(fileboi)
    listyboi.extend(jason['data'])
    # for each in jason['data']:
    #     if each['legalities']['standard'] == 'legal' and each['type_line'] in list(sadness.card_types.keys):
    #         listyboi.append(each)
    #     else:
    #         continue


wowdf = pd.DataFrame.from_records(listyboi)
wowdf = wowdf[["oracle_text"]]
wowdf.to_csv("LSTMData.csv")


