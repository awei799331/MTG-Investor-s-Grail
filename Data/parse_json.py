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
    for each in jason['data']:
        if each['legalities']['standard'] == 'legal' and each['type_line'] in list(sadness.card_types.keys):
            listyboi.append(each)
        else:
            continue


wowdf = pd.DataFrame.from_records(listyboi)
wowdf = wowdf[["mana_cost", "cmc", "type_line", "oracle_text", "power", "toughness", "rarity", "booster", "prices"]]


for tupleboi in wowdf.itertuples():

    #1st index is index

    #Handling Mana Cost
    jankydict = sadness.jankydict.copy()
    generic_mana = 0.0
    mana_cost = str(tupleboi[1])
    split_card = False
    if '//' in mana_cost:
        split_card = True
    mana_cost = mana_cost.replace("{", "").replace("//", "").replace(" ", "").split("}")
    # generic, w, u, b, r, g :
    for each in mana_cost:
        if '/' in each:
            each = each.split('/')
            for yoch in each:
                try:
                    float(yoch)
                except:
                    jankydict[yoch] += 0.5
        else:
            try:
                float(each)
                generic_mana = each
            except:
                jankydict[each] += 1
    newtuple = (generic_mana,) + tuple(jankydict.values)
    
    #handling cmc
    cmc = tupleboi[2]
    newtuple += (float(cmc))

    #handling type
    #added variable for legendary, adventure, card_types..., creature_types..., artifact_types..., planeswalker_types...
    type_of_card = str(tupleboi[3])
    legendary = 0
    adventure = 0
    card_types = sadness.card_types.copy()
    creature_types = sadness.creature_types.copy()
    artifact_types = sadness.artifact_types.copy()
    planeswalker_types = sadness.planeswalker_types.copy()
    if 'Legendary' in type_of_card:
        type_of_card = type_of_card.replace('Legendary', '')
        legendary = 1.0
    if 'Adventure' in type_of_card:
        type_of_card = type_of_card.replace('Adventure', "")
        adventure = 1.0

    type_of_card = type_of_card.replace('â€”', '').split()
    for types in type_of_card:
        if types in card_types:
            card_types[types] = 1.0
        if types in creature_types:
            creature_types[types] = 1.0
        if types in artifact_types:
            artifact_types[types] = 1.0
        if types in planeswalker_types:
            planeswalker_types[types] = 1.0
    newtuple += (legendary, adventure) + tuple(card_types.values) + tuple(creature_types.values) + \
tuple(artifact_types.values) + tuple(planeswalker_types.values)

    #handling Oracle text
    oracle_text = str(tupleboi[4])
    mode = "not stupid"
    if mode == "stupid":
        ree


wowdf.to_csv('wowies.csv')