import torch 
import numpy as np
import pandas as pd
from torch.utils.data import Dataset

import os
import json
import datetime
import pickle
from . import parse_csv
from . import parse_json


class MTGJson(Dataset):
    '''dataset for MTGjson.com, a mixture of csv inputs and json inputs, 
        all stored in the data folder,

        Currently, file tree looks like:
            data
                AllPrices.json
                AllPrintings.json
                cards.csv
                sets.csv

        Inputs:
            datadir: path to cards.csv, e.g. "data/cards.csv"
            fields: list of fields to search for, column headers in cards.csv
            mapped_funcs: list of functions that are applied to each element of columns in fields
            mode: default "vecs", mode of operation
            to_csv: default False, whether to save the processed data in a csv
            csv_filename: default "data.csv", filename and path for csv
            save_dicts: default False, saving utility dictionaries
            utildicts_path: path to a pickled UtilDicts object
    '''

    def __init__(self, 
                datadir, 
                fields, 
                mapped_funcs,
                mode="vecs", 
                to_csv=False, 
                csv_filename="data.csv", 
                save_dicts=False, 
                utildicts_path="",
                # price input arguments
                price_transforms=[], 
                price_filename="data\AllPrices.json", 
                platform="paper", 
                site="tcgplayer", 
                buylist="retail", 
                foil="normal"):
        
        self.mode = mode

        self.card_data_full = pd.read_csv(datadir)
        
        if self.mode == "vecs":
            self._create_vecs(fields, mapped_funcs, to_csv, csv_filename)
        if self.mode == "prices":
            self._create_price_vecs(fields, mapped_funcs, price_transforms, to_csv, 
                csv_filename, price_filename, platform, site, buylist, foil)
        
        # logic for setting utildicts
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

        # definitions for class attributes that may or may not be used for each instance of the class
        # depends on mode

        self.card_prices = None

    def _create_vecs(self, fields, mapped_funcs, to_csv, csv_filename):
        '''
        creates a dataframe of vectors, with uuid as the index

        Inputs:
            fields: list of fields to search for, column headers in cards.csv
            mapped_funcs: list of functions that are applied to each element of columns in fields
            to_csv: default False, whether to save the processed data in a csv
            csv_filename: default "data.csv", filename and path for csv
        Outputs:
            None
            Saves self.card_data with vector info
        '''
        self.card_data = self.card_data_full[fields] # getting only fields

        list4df = []
        uuids = self.card_data_full["uuid"] #isolating uuid

        # mapping functions to each item in dataframe
        for rowtuple in self.card_data.itertuples():

            #1st index is index
            output = ()
            for i in range(0, len(rowtuple) - 1):
                output += mapped_funcs[i](rowtuple[i+1])
            list4df.append(output)
        
        processed_values = pd.DataFrame(list4df, index=uuids)
        
        self.card_data = processed_values
        # saving to csv
        if to_csv:
            processed_values.to_csv(csv_filename, index=False, header=False)
        
    def _load_prices(self, filename="data\AllPrices.json", platform="paper", site="tcgplayer", buylist="retail", foil="normal"):
        ''' creates a card_prices attribute'''
        with open(filename) as f:
            self.card_prices = parse_json.parse_price(json.load(f), platform, site, buylist, foil)
    
    def _create_price_vecs(self, fields, mapped_funcs, price_transforms, to_csv, 
                            csv_filename, price_filename, platform, site, buylist, foil):
        '''
        creates price vectors according to price_transforms
        First calls internal method create vecs
        
        Outputs:
            None
            Internal var changes:
                self.price_vecs = dataframe with "uuid", "price" columns, and rest of relevant numbers
        
        '''
        self._create_vecs(fields, mapped_funcs, to_csv, csv_filename) # creates and populates self.card_data
        
        self._load_prices(price_filename, platform, site, buylist, foil) # creates and populates self.card_prices

        output = self.card_prices
        
        for transform in price_transforms:
            output = transform(output)
        
        self.price_vecs = output

    def __len__(self):  
        if self.mode == "vecs":
            return len(self.card_data)

        if self.mode == "prices":
            return len(self.price_vecs)
        
    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        if self.mode == "vecs":
            sample = {"uuid": self.card_data.index[idx], "vec": torch.tensor(self.card_data.iloc[idx, :].to_numpy(dtype=np.float32))}
        
        if self.mode == "prices":
            #simple concatenation of context vector to the end of price vector
            # price is just price, in dollars of whatever currency that was put in
            sample = {
                        "price": torch.tensor(self.price_vecs.loc[idx, "price"], dtype=torch.float32), 
                        "vec": torch.tensor(
                                np.concatenate((self.price_vecs.drop(columns=["uuid", "price"]).loc[idx, :].to_numpy(dtype=np.float32), 
                                                self.card_data.loc[self.price_vecs.loc[idx, "uuid"], :].to_numpy(dtype=np.float32)), 
                                                axis=0
                                                )
                                            )
                    }

        return sample
    
    def get_num_features(self):
        ''' 
        Method to get the number of features in the input vec
        
        output: int
        internal variable changes:
            self.num_features: updated with new num of features

        '''
        
        if self.mode == "vecs":
            self.num_features = self[0]["vec"].shape[0]
        
        if self.mode == "prices":
            self.num_features = self[0]["vec"].shape[0]

        return self.num_features



class UtilDicts():
    '''
    an object to store utility dictionaries for internal usage
    Inputs:
        card_data_full: a dataframe of cards.csv
    '''
    def __init__(self, card_data_full):
        self.card_data_full = card_data_full

        # potential dictionaries
        # TODO describe dictionaries
        self.uuid2cardName = None
        self.uuid2scryfallId = None
        self.uuid2set = None
        self.set_data = None
        self.set2date = None
        self.uuid2date = None
    
    def create_dictionaries(self, save_dicts=False, save_path="utildicts.p"):


        #creating uuid 2 card name dictionary
        self.uuid2cardName = {vec[1]: vec[2] for vec in self.card_data_full[["uuid", "name"]].itertuples()}
        #creating uuid 2 scryfall id dictionary
        self.uuid2scryfallId = {vec[1]: vec[2] for vec in self.card_data_full[["uuid", "scryfallId"]].itertuples()}

        #creating uuid to release date
        self.uuid2set = {vec[1]: vec[2] for vec in self.card_data_full[["uuid", "setCode"]].itertuples()}
        
        self.set_data = pd.read_csv("data/sets.csv") # UNHARDCODETHIS TODO FIX TESTER
        self.set2date = {vec[1]: datetime.datetime.strptime(vec[2], 
                                                            '%Y-%m-%d') for vec in self.set_data[["code", "releaseDate"]].itertuples()}
        self.uuid2date = {key : self.set2date[value] for key, value in self.uuid2set.items()}

        if save_dicts is True:
            with open(save_path, "wb") as f:
                pickle.dump(self, f)