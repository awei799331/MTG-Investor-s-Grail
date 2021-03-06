# functions to operate on standard outdict
import pandas as pd
import datetime

def filter_dict(currency="USD", price_avg_floor=1.0):
    '''returns a function that filters the original dictionary'''
    def tmp(inp):
        output_dict = {}
        for uuid, value in inp.items():
            if value["currency"] == currency:
                prices = [price for date, price in value["prices"]]
                price_avg = sum(prices)/len(prices)

                if price_avg > price_avg_floor:
                    output_dict[uuid] = value
        return output_dict
    return tmp


def dfify(inp):
    '''
    dataframifys the input dictionary

    creates a dataframe with columns "uuid", "price", "date"
    from an input dictionary of format:
        {
            "uuid": {
                "currency": "string",
                "prices": [(datetime, float)]
            } 
        }
    '''

    columns = ["uuid", "price", "date"]

    data = []

    for uuid, values in inp.items():
        data.extend([[uuid, price, date] for date, price in values["prices"]])
    
    return pd.DataFrame(data, columns=columns)

def poopy_encoding(inp):
    ''' really poopy encoding of time xd, days since MTG was released: August 5, 1993'''
    d0 = datetime.date(1993, 8, 5)
    inp["date"] = inp["date"].map(lambda out: (out.date()-d0).days)

    return inp