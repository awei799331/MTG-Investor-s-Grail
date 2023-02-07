import json
import os
import pandas as pd
import numpy as np
from . import sadness


def parse_json(directory="JsonAll"):

    listyboi = []
    '''
    for filename in os.listdir(directory):
        with open(directory + '/' + filename, 'r+', encoding='utf8') as fileboi:
            jason = json.load(fileboi)
            for each in jason['data']:
                if each['legalities']['standard'] == 'legal':
                    listyboi.append(each)
                else:
                    continue
    '''

    with open(directory + '/' + 'CD.json', 'r+', encoding='utf8') as fileboi:
        jason = json.load(fileboi)
        for each in jason['data']:
            listyboi.append(each)


    wowdf = pd.DataFrame.from_records(listyboi)
    wowdf = wowdf[["mana_cost", "cmc", "type_line", "oracle_text", "power", "toughness", "rarity", "booster", "prices"]]

    list4df = []

    for tupleboi in wowdf.itertuples():

        #1st index is index

        #Handling Mana Cost
        color_dict = sadness.color_dict.copy()
        generic_mana = 0.0
        if tupleboi[1] != 'nan':
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
                        color_dict[yoch] += 0.5
            else:
                try:
                    float(each)
                    generic_mana = each
                except:
                    if each in color_dict:
                        color_dict[each] += 1
        newtuple = (generic_mana,) + tuple(color_dict.values())
        
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
        
        #handling booster
        if str(tupleboi[8]) != 'nan':
            booster = str(tupleboi[8])
            if booster == "TRUE":
                booster = 1.0
            else:
                booster = 0.0
        else:
            booster = -1.0
        newtuple += (booster, )

        #handling price
        if str(tupleboi[9]) != 'nan':
            price = str(tupleboi[9])
            price = price.replace("'", "\"").replace('None', "-1")
            priced = json.loads(price)
            price = float(priced['usd'])
            if price == -1:
                price = float(priced['usd_foil'])
        else:
            price = -1.0
        newtuple += (price,)

        #appending
        list4df.append(newtuple)

    wowdf = pd.DataFrame(list4df)

    wowdf.to_csv('CD.csv', index=False, header=False)