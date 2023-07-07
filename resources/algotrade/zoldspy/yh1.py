'''
based on  session 1
https://gist.github.com/yhilpisch/e802541f8def69a299032c359d0f1008
uses daily candles from eurusd
'''

import pandas as pd
import numpy as np
import datetime as dt
import mplfinance as mpf

# import plots and styling
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import style

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 111)

# read data
colnames = ['Date', 'Open', 'High', 'Low', 'Close']
data = pd.read_csv('/zata/truefx/AUDJPY/audjpy1D.csv', names=colnames, index_col=0, parse_dates=True)

# visualize data
plt.style.use('ggplot')
plt.style.use('seaborn')
data['CloseAsk'].plot(figsize=(10, 6), lw=0.8)

# adding statistics
data = data.loc['2014-1-1':]
data['CloseAsk'].plot(figsize=(10, 6), lw=0.8)
data['CloseMid'] = data[['CloseBid', 'CloseAsk']].mean(axis=1)
data['SMA1'] = data['CloseMid'].rolling(10).mean()
data['SMA2'] = data['CloseMid'].rolling(60).mean()
data.dropna(inplace=True)
data[['CloseMid', 'SMA1', 'SMA2']].plot(figsize=(10, 6), lw=0.8)

# deriving positions
data['Positions'] = np.where(data['SMA1'] > data['SMA2'], 1, -1)
data[['CloseMid', 'SMA1', 'SMA2', 'Positions']].plot(
    figsize=(10, 6), secondary_y='Positions', lw=0.8)

# backtesting the strategy
data['Returns'] = np.log(data['CloseMid'] / data['CloseMid'].shift(1))
data
data['Strategy'] = data['Positions'].shift(1) * data['Returns']
data
data[['Returns', 'Strategy']].dropna().cumsum().apply(
    np.exp).plot(figsize=(10, 6), lw=0.8)


# candlestick plot
mpf.plot(data.head(30), type='candle', style='charles')
