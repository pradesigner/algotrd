import fxcmpy
import pandas as pd
import numpy as np
import datetime as dt
# import funcs
from pyti.bollinger_bands import upper_bollinger_band as ubb
from pyti.bollinger_bands import middle_bollinger_band as mbb
from pyti.bollinger_bands import lower_bollinger_band as lbb
from pyti.bollinger_bands import percent_bandwidth as percent_b
# import plots and styling
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 111)

# get the api access
socket = fxcmpy.fxcmpy(config_file='fxcmdemo.cfg')
print(socket.get_instruments_for_candles())

# get prices into dataframe
data = socket.get_candles(instrument='EUR/GBP',
                          period='D1',
                          start=dt.datetime(2016, 1, 1),
                          end=dt.datetime(2018, 6, 10))

# drop unnecessary columns
data.drop(['bidopen', 'bidclose', 'bidhigh', 'bidlow',
           'askhigh', 'asklow'], axis=1, inplace=True)

# define variables for the strategy
data['upper_band'] = ubb(data['askclose'], period=20)
data['mid_band'] = mbb(data['askclose'], period=20)
data['lower_band'] = lbb(data['askclose'], period=20)
data['percent_b'] = percent_b(data['askclose'], period=20)

# view the price and bands
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(111, xlabel='Date', ylabel='Close')

data['askclose'].plot(ax=ax1, color='r', lw=1)
data['upper_band'].plot(ax=ax1, color='b', lw=1)
data['mid_band'].plot(ax=ax1, color='g', lw=1)
data['lower_band'].plot(ax=ax1, color='y', lw=1)

# isolate and plot the percent B line
band_fig = plt.figure(figsize=(12, 8))
ax2 = band_fig.add_subplot(111,  ylabel='%B')
data['percent_b'].plot(ax=ax2, color='b', lw=1)

# backtest idea
data['signal'] = np.where((data['percent_b'] <= .2), 1, 0)
data['position'] = data['signal'].diff()

pip_cost = 1
lot_size = 10

# Gets the number of pips that the market moved during the day
data['pip_diff'] = (data['askclose'] - data['askopen']) * 100

# Calculates the daily return while a position is active
# 'Total' column records our running profit / loss for the strategy
returns = 0
CountPL = False
for i, row in data.iterrows():
    if CountPL:
        returns += (row['pip_diff'] * pip_cost * lot_size)
        data.loc[i, 'total'] = returns
    else:
        data.loc[i, 'total'] = returns

    if row['signal'] == 1:
        CountPL = True
    else:
        CountPL = False

# visualize
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(111, ylabel='Profits in $')

data['total'].plot(ax=ax1, color='r', lw=1.)

# Placing markers for our position entry
ax1.plot(data.loc[data.position == 1.0].index,
         data.total[data.position == 1.0],
         '^', markersize=10, color='m')

# Placing markers for our position exit

ax1.plot(data.loc[data.position == -1.0].index,
         data.total[data.position == -1.0],
         'v', markersize=10, color='k')

plt.show()
