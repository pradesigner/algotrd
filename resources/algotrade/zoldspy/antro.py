#!/usr/bin/env python3

'''
demos various things for reference
tickdata -> pandas -> matplotlib

nu forward and reverse functions created
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ohlc

# read in csv data
df = pd.read_csv('/zata/truefx/USDCAD/USDCAD-2018-10.csv',
                 names=['pair', 'date', 'bid', 'ask'],
                 usecols=['date', 'bid', 'ask'],
                 parse_dates=['date'])

# setup spread and average columns
df['spread'] = df['ask']-df['bid']
df['average'] = .5*(df['ask']+df['bid'])

# make date the index
df.set_index('date', inplace=True)

# trim excess columns
# df = df['average']

# resample as ohlc removing NaN rows
d1 = df['average'].resample('1D').ohlc().dropna()
# h4 = df.resample('4h').ohlc().dropna()
# h1 = df.resample('1h').ohlc().dropna()

# # simple scatter plot
# fig, ax = plt.subplots()
# ax.scatter(df.index, df['average'], s=3)


def nu_reverse(bars):
    sz = 2
    beg = -4
    end = -(len(bars)-sz)
    mxs = []
    for i in range(beg, end, -1):
        mx = max(bars[i-sz:i+sz+1])
        if bars[i] == mx:
            mxs.append(mx)
    return mxs


def nu(bars):
    sz = 2
    beg = 2
    end = len(bars)-sz
    mxs = []
    for i in range(beg, end):
        mx = max(bars[i-sz:i+sz+1])
        if bars[i] == mx:
            mxs.append((i, mx))
    return mxs


maxs = np.array(nu(d1['high']), dtype=float)

# simple candlestick plot
fig, ax = plt.subplots(figsize=(10, 5))
candlestick2_ohlc(ax, d1.open, d1.high, d1.low, d1.close,
                  width=.6, colorup='green', colordown='red')
for itm in maxs:
    plt.hlines(itm[1], xmin=itm[0], xmax=22)

# simple candlestick plot
fig, ax = plt.subplots(figsize=(10, 5))
candlestick2_ohlc(ax, d1.open, d1.high, d1.low, d1.close,
                  width=.6, colorup='green', colordown='red')
for i in maxs:
    plt.hlines(i, xmin=0, xmax=22)


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


##########################
# whatever ...
# In [1]: /home/pradmin/.local/lib/python3.7/site-packages/pandas/plotting/_matplotlib/converter.py:103: FutureWarning: Using an implicitly registered datetime converter for a matplotlib plotting method. The converter was registered by pandas on import. Future versions of pandas will require you to explicitly register matplotlib converters.

# To register the converters:
# 	>>> from pandas.plotting import register_matplotlib_converters
# 	>>> register_matplotlib_converters()
#   warnings.warn(msg, FutureWarning)
