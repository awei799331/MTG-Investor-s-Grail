import torch 
import numpy as np
import pandas as pd
from torch.utils.data import Dataset

import os
import json
import datetime
import pickle
from . import parse_csv

class MTGJson(Dataset):
    '''dataset for MTG json'''

    def __init__(self, datadir, fields, mapped_funcs, mode="vecs", to_csv=False, csv_filename="", save_dicts=False, utildicts_path=""):
        
        self.mode = mode

        self.card_data_full = pd.read_csv(datadir)

        self.create_vecs(fields, mapped_funcs, to_csv, csv_filename)
        
        if utildicts_path:
            if save_dicts:
                self.utildicts = UtilDicts(self.card_data_full)
                self.utildicts.create_dictionaries(save_dicts, utildicts_path)
            else:
                with open(utildicts_path, "rb") as f:
                    self.utildicts = pickle.load(f)
        else:
            self.utildicts = UtilDicts(self.card_data_full)
            self.utildicts.create_dictionaries(save_dicts, utildicts_path)

    def create_vecs(self, fields, mapped_funcs, to_csv, csv_filename):
        self.card_data = self.card_data_full[fields]

        list4df = []

        for rowtuple in self.card_data.itertuples():

            #1st index is index
            output = ()
            for i in range(0, len(rowtuple) - 1):
                output += mapped_funcs[i](rowtuple[i+1])
            list4df.append(output)

        processed_values = pd.DataFrame(list4df)
        #TESTER
        processed_values.head()

        self.card_data = processed_values
        if to_csv:
            processed_values.to_csv(csv_filename, index=False, header=False)

    def __len__(self):  
        return len(self.card_data)
        
    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        if self.mode == "vecs":
            sample = {"uuid": self.card_data.iloc[idx, 0], "vec": torch.tensor(self.card_data.iloc[idx, 1:].to_numpy(dtype=np.float32))}

        return sample

class UtilDicts():
    def __init__(self, card_data_full):
        self.card_data_full = card_data_full
    
    def create_dictionaries(self, save_dicts=False, save_path="utildicts.p"):
        #creating uuid 2 card name dictionary
        self.uuid2cardName = {vec[1]: vec[2] for vec in self.card_data_full[["uuid", "name"]].itertuples()}
        #creating uuid 2 scryfall id dictionary
        self.uuid2scryfallId = {vec[1]: vec[2] for vec in self.card_data_full[["uuid", "scryfallId"]].itertuples()}

        #creating uuid to release date
        self.uuid2set = {vec[1]: vec[2] for vec in self.card_data_full[["uuid", "setCode"]].itertuples()}
        
        self.set_data = pd.read_csv("data/sets.csv") # UNHARDCODETHIS TODO FIX TESTER
        self.set2date = {vec[1]: datetime.datetime.strptime(vec[2], '%Y-%m-%d') for vec in self.set_data[["code", "releaseDate"]].itertuples()}
        self.uuid2date = {key : self.set2date[value] for key, value in self.uuid2set.items()}

        if save_dicts is True:
            with open(save_path, "wb") as f:
                pickle.dump(self, f)