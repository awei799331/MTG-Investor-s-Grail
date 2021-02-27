####################################################################################
#                                                                                  #
#            Functions that are called on python representations of                #
#            json files (dicts), and return something else :D                      #
#                                                                                  #
####################################################################################
import datetime


def parse_price(inp, platform="paper", site="tcgplayer", buylist="retail", foil="normal"):
    '''
    Function that parses price information, returns a dictionary with the format
    given below

    inputs:
        inp: dict, a dict-like object representing a json from AllPrices.json

    
    outputs:
        out: dict, with format:
        {
            "uuid": {
                "currency": "string",
                "prices": [(datetime, float)]
            } 
        }

    TODO
        sort price info by ascending time
    '''
    output = {}

    for uuid, values in inp["data"].items():
        if platform in values:
            if site in values[platform]:
                if buylist in values[platform][site]:
                    if foil in values[platform][site][buylist]:
                        try:
                            output[uuid] = {
                                "currency": values[platform][site]["currency"],
                                "prices": [(datetime.datetime.strptime(date, "%Y-%m-%d"), price) for date, price in values[platform][site][buylist][foil].items()]
                            }
                        except:
                            print(values)

    return output
