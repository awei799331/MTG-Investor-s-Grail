import json
import os
import pandas as pd
import numpy as np
import sadness

directory = 'MTGJSON'


card_data = pd.read_csv(directory + "/" + "cards.csv")

card_data = card_data[["manaCost", "convertedManaCost", "type", "text", "power", "toughness", "rarity", "uuid", "setCode"]]

list4df = []

for tupleboi in card_data.itertuples():

    #1st index is index

    #Handling Mana Cost
    jankydict = sadness.jankydict.copy()
    generic_mana = 0.0
    if str(tupleboi[1]) != 'nan':
        mana_cost = str(tupleboi[1])
    else:
        mana_cost = ''
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
                    if yoch in jankydict:
                        jankydict[yoch] += 0.5
        elif each != '':
            try:
                float(each)
                generic_mana = each
            except:
                if each in jankydict:
                    jankydict[each] += 1
    newtuple = (generic_mana,) + tuple(jankydict.values())
    
    #handling cmc
    if str(tupleboi[2]) != 'nan':
        cmc = tupleboi[2]
    else:
        cmc = -1.0
    #newtuple += (float(cmc),)

    #handling type
    #added variable for legendary, card_types..., creature_types..., artifact_types..., planeswalker_types...
    if str(tupleboi[3]) != 'nan':
        type_of_card = str(tupleboi[3])
    else:
        type_of_card = ''
    legendary = 0
    card_types = sadness.card_types.copy()
    creature_types = sadness.creature_types.copy()
    artifact_types = sadness.artifact_types.copy()
    planeswalker_types = sadness.planeswalker_types.copy()
    if 'Legendary' in type_of_card:
        type_of_card = type_of_card.replace('Legendary', '')
        legendary = 1.0

    type_of_card = type_of_card.replace('â€”', '').split()
    for types in type_of_card:
        if types in card_types:
            card_types[types] = 1.0
        if types in creature_types:
            creature_types[types] = 1.0
        if types in artifact_types:
            artifact_types[types] = 1.0
    newtuple += (legendary,) + \
tuple(card_types.values())
# + tuple(creature_types.values()) + \
#tuple(artifact_types.values()) + tuple(planeswalker_types.values())

    #handling Oracle text
    if str(tupleboi[4]) != 'nan':
        oracle_text = str(tupleboi[4])
    else:
        oracle_text = ''
    mode = "stupid"
    if mode == "stupid":
        char_dict = sadness.char_dict.copy()
        for char in oracle_text:
            if char in char_dict:
                char_dict[char] += 1
    #newtuple += tuple(char_dict.values())

    #handling power
    if str(tupleboi[5]) != 'nan':
        try:
            power = float(tupleboi[5])
        except:
            power = 0.0
    else:
        power = -1.0
    newtuple += (power, )

    #handling toughness
    if str(tupleboi[6]) != 'nan':
        try:
            toughness = float(tupleboi[6])
        except:
            toughness = 0.0
    else:
        toughness = -1.0
    newtuple += (toughness, )

    #handling rarity
    rarity_dict = sadness.rarity_dict.copy()
    if str(tupleboi[7]) != 'nan':
        rarity = str(tupleboi[7])
        rarity_dict[rarity] = 1.0
    else:
        pass
    newtuple += tuple(rarity_dict.values())
    

    #appending
    list4df.append((tupleboi[8], tupleboi[9]) + newtuple)

processed_values = pd.DataFrame(list4df)

processed_values.to_csv("data.csv", index=False, header=False)
""" card_data[["text"]].to_csv(r'data.txt', header=None, index=None, sep=' ')
card_data[['text']].to_csv("LSTMData.csv", index=False, columns=['text']) """