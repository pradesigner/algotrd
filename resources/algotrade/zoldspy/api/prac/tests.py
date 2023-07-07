#!/usr/bin/env python3

# various testing
# usage: na

from configs import *
import pandas as pd

# accts = accounts()
# details = details()
# summary = summary()
# instruments = instruments()

# TODO get candles into decent pandas format
# get time column properly formatted
# get loch done right
# drop complete column

df = get_candles('EUR_USD', 10, 'H4')


# cd = getEURUSD(acct03)
# df = pd.read_json(json.dumps(cd))
# df_data = pd.io.json.json_normalize(df.candles)
# df_data.time = pd.to_datetime(df_data.time)


#############################
'''useful code fragments'''
# json formated instruments
# print(json.dumps(instruments, sort_keys=True, indent=4))

# sorted instruments
# print(sorted([itm['name']
#               for itm in instruments['instruments']
#               if itm['type'] == 'CURRENCY']))

# items in mylist, but not sorted
# mylist = ['AUD_USD', 'EUR_USD', 'GBP_USD', 'USD_CAD', 'USD_JPY']
# print(json.dumps([itm
#                   for itm in instruments['instruments'] if itm['name'] in mylist], indent=4))
