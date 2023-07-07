#!/usr/bin/env python3

# calculates the dervatives of pa
# usage: na

from os import listdir
import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ohlc


def candles(df):
    '''
    displays candlestick chart
    '''
    fig, ax = plt.subplots(figsize=(10, 5))
    candlestick2_ohlc(ax, df.open, df.high, df.low, df.close,
                      width=.6, colorup='green', colordown='red')
    # plt.show(block=True)


def pcf(F):
    '''
    sets the pip conversion factor for pair
    '''
    return 100 if 'JPY' in F else 10000


def filenames():
    '''
    creates filename list in the tfx directory
    '''
    sep = '/'
    bdir = './tfx'
    filenames = []
    for D in sorted(listdir(bdir)):
        filenames.append(sep.join([bdir, D, D.lower()+'1D.csv']))
    return filenames


def dfcsv(filename):
    '''
    setup a dataframe from csv file
    '''
    df = pd.read_csv(filename,
                     names=['dt', 'open', 'high', 'low', 'close'],
                     parse_dates=['dt'])
    return df


def cleanup(df):
    '''
    replaces outrageous ohlc values with sensible ones
    '''
    df['hilo'] = df['high']-df['low']
    inds = df[df['hilo'] > df['hilo'].mean()+6*df['hilo'].std()].index.values
    for i in inds:
        # avgOC diff HL +- avgOC
        if df['high'][i] > df['high'].mean()+6*df['high'].std():
            df.loc[i, 'high'] = df['open'][i]+df['close'][i] + df['low'][i]
        if df['low'][i] < df['low'].mean()-6*df['low'].std():
            df.loc[i, 'low'] = df['open'][i]+df['close'][i] - df['high'][i]
    return df


for F in filenames()[:1]:
    print()
    pcf = pcf(F)
    print(F, pcf)
    df = dfcsv(F)
    df = cleanup(df)
    df['hilo'] = pcf*df['hilo']

    df['avg'] = 0.5*(df['high']+df['low'])

    df['avg1'] = pcf*df['avg'].diff()
    df['avg2'] = df['avg1'].diff()
    # df.dropna(inplace=True)

    candles(df)
    df['avg'].plot()

plt.show()
