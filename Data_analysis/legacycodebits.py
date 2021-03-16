fields = ["manaCost", "convertedManaCost", "type", "power", "toughness", "rarity"]

mapped_funcs = [pc.mana_cost, pc.cmc, pc.type_of_card, pc.power, pc.toughness, pc.rarity]

MTGdataset = MTGJson(datadir="data/cards.csv", fields=fields, mapped_funcs=mapped_funcs, mode="vecs", to_csv=False, csv_filename="", save_dicts=False, utildicts_path="")