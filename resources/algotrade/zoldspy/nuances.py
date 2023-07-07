#!/usr/bin/env python3

# nuances.py finds nu properties such as
# - distance in pips between nus
# usage: jri

from sys import exit
import os
import pandas as pd
import matplotlib.pyplot as plt

print()


def nu(df):
    '''
    finds nus

    uses maxmin of 5 candle hilo values
    '''
    span = 2
    beg = 2
    end = len(df)-span
    for i in range(beg, end):
        mx = max(df['high'][i-span:i+span+1])
        if df['high'][i] == mx:
            df.loc[i, 'n'] = mx
        mn = min(df['low'][i-span:i+span+1])
        if df['low'][i] == mn:
            df.loc[i, 'u'] = mn
    return df


def filenames():
    '''
    creates filename list
    '''
    sep = '/'
    bdir = './tfx'
    filenames = []

    # make filename list in the tfx directory
    for D in sorted(os.listdir(bdir)):
        filenames.append(sep.join([bdir, D, D.lower()+'1D.csv']))
    return filenames


# analyse each pair for nu properties
for F in filenames()[:2]:
    print(F)
    pcf = 100 if 'JPY' in F else 10000  # sets pip conversion factor

    # read csv data
    df = pd.read_csv(F,
                     names=['dt', 'open', 'high', 'low', 'close'],
                     parse_dates=['dt'])
    df['n'] = df['u'] = 0.0  # creates n,u columns
    df = nu(df)  # finds the nu levels

    # nus dataframe
    nus = df['n'] + df['u']  # creates it from n,u columns
    nus = nus.loc[(nus != 0)]  # removes all zero items
    nus = nus.reset_index().drop(columns=['index'])  # re-indexes the index
    nus.columns = ['nu_levels']  # names the nu levels columns
    nus['diffs'] = pcf*nus.diff().apply(abs)  # diffs using pcf and abs
    nus.dropna(inplace=True)  # removes NaN
    # removes outliers but doesn't make sense
    nus = nus[nus['diffs'] < 2*nus['diffs'].std()]
    print(nus['diffs'].describe())  # prints out diffs summary for pair
    plt.figure()
    plt.title(F.split('/')[2])
    nus['diffs'].hist(bins=100)

plt.show()

#
#
'''
old code
'''

# # simple candlestick plot ######
# fig, ax = plt.subplots(figsize=(10, 5))
# candlestick2_ohlc(ax, df.open, df.high, df.low, df.close,
#                   width=.6, colorup='green', colordown='red')

# adjacent confluence try ######

# # calculate mlines
# for m in [1, 2, 3]:
#     mpow = 6**m
#     mstr = 'm'+str(mpow)
#     df[mstr] = df['avg'].diff(mpow)/mpow

# # remove NaN
# df.dropna(inplace=True)

# # mline diff
# df['m6_diff'] = df['m6'].diff()

# # calculate movement
# df['mov'] = df['close'] - df['open']

# # task A: adjacent concurrency
# i = 0
# Tpp = Fpp = Tnn = Fnn = 0
# Tpp_m6 = Fpp_m6 = Tnn_m6 = Fnn_m6 = 0

# dfsize = len(df) - 1

# for i in range(1, dfsize):
#     pp = df['mov'].iloc[i-1] > 0 and df['mov'].iloc[i] > 0
#     nn = df['mov'].iloc[i-1] < 0 and df['mov'].iloc[i] < 0
#     pp_m6 = pp and df['m6_diff'].iloc[i] > 0
#     nn_m6 = nn and df['m6_diff'].iloc[i] < 0
#     if pp:
#         Tpp += 1
#     else:
#         Fpp += 1
#     if nn:
#         Tnn += 1
#     else:
#         Fnn += 1
#     if pp_m6:
#         Tpp_m6 += 1
#     else:
#         Fpp_m6 += 1
#     if nn_m6:
#         Tnn_m6 += 1
#     else:
#         Fnn_m6 += 1

# print()
# print('pp', Tpp, Fpp)
# print('nn', Tnn, Fnn)
# print('pp_m6', Tpp_m6, Fpp_m6)
# print('nn_m6', Tnn_m6, Fnn_m6)
