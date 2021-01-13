from . import sadness

'''functions for processing the string input of each field to 
numerical representations. Output as tuples'''

def mana_cost(inp):
    '''(str) -> tuple
    converts string representation of mana cost to tuple
    with format of (generic, w, u, b, r, g)'''
    jankydict = sadness.jankydict.copy()
    generic_mana = 0.0
    if str(inp) != 'nan':
        mana_cost = str(inp)
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
                    generic_mana += 0.5*yoch
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
    return (generic_mana,) + tuple(jankydict.values())

def cmc(inp):
    '''(str) -> tuple
    converts string representation of cmc to tuple
    with format of (cmc)'''

    if str(inp) != 'nan':
        cmc = inp
    else:
        cmc = -1.0
    return (float(cmc),)

def type_of_card(inp):
    if str(inp) != 'nan':
        type_of_card = str(inp)
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
    return (legendary,) + \
            tuple(card_types.values())
            # + tuple(creature_types.values()) + \
            #tuple(artifact_types.values()) + tuple(planeswalker_types.values())

def oracle_text(inp):
    if str(inp) != 'nan':
        oracle_text = str(inp)
    else:
        oracle_text = ''
    mode = "stupid"
    if mode == "stupid":
        char_dict = sadness.char_dict.copy()
        for char in oracle_text:
            if char in char_dict:
                char_dict[char] += 1
    return tuple(char_dict.values())

def power(inp):
    if str(inp) != 'nan':
        try:
            power = float(inp)
        except:
            power = 0.0
    else:
        power = -1.0
    return (power, )

def toughness(inp):
    if str(inp) != 'nan':
        try:
            toughness = float(inp)
        except:
            toughness = 0.0
    else:
        toughness = -1.0
    return (toughness, )

def rarity(inp):
    rarity_dict = sadness.rarity_dict.copy()
    if str(inp) != 'nan':
        rarity = str(inp)
        rarity_dict[rarity] = 1.0
    else:
        pass
    return tuple(rarity_dict.values())

def pass_through(inp): return (inp,)