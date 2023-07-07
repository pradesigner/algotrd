import datetime as dt
import pandas as pd
import fxcmpy
print('fxcmpy version: ', fxcmpy.__version__)

# make the connection using the cfg file which keeps the token
con = fxcmpy.fxcmpy(config_file='fxcmdemo.cfg', server='demo')

# view all instruments that you can subscribe to on your account,
all_instruments = con.get_instruments()
print('All available instruments\n', all_instruments)

# view currently subscribed instruments
current_instruments = con.get_instruments_for_candles()
print('Currently subscribed instruments\n', current_instruments)

# pull historical prices as pandas dataframe by number
data36 = con.get_candles('GBP/JPY',
                         period='D1',
                         number=36)
print('List columns\n', data36.columns)
print('Print head\n', data36.head())
print('Print tail\n', data36.tail())

# pull historical prices as pandas dataframe by time period
dataPER = con.get_candles('GBP/JPY',
                          period='D1',
                          start=dt.datetime(2018, 1, 1),
                          stop=dt.datetime(2018, 1, 30))
print('List columns\n', dataPER.columns)
print('Print head\n', dataPER.head())
print('Print tail\n', dataPER.tail())

# streaming real-time prices
con.subscribe_market_data('EUR/USD')
eurusd = con.get_prices('EUR/USD')
con.unsubscribe_market_data('EUR/USD')

# checking open positions
open_postions = con.get_open_positions()
cols = len(open_postions.columns)
pd.set_option('display.max_columns', cols)

# creating basic market orders
con.create_market_sell_order('AUD/USD', 10)
audusd_trade_id = open_postions.loc[open_postions['currency']
                                    == 'AUD/USD', 'tradeId'].item()
con.change_trade_stop_limit(trade_id=audusd_trade_id,
                            is_stop=True,
                            rate=-60)
con.change_trade_stop_limit(trade_id=audusd_trade_id,
                            is_stop=False,
                            rate=60)

# creating more complex market orders
con.open_trade(symbol='GBP/USD',  # instrument
               is_buy=True,  # buy or sell
               rate=1.307,  # entry point
               is_in_pips=False,  # sl is not in pips
               amount=10,  # lots
               time_in_force='GTC',  # good till cancelled
               order_type='AtMarket',  # or MarketRange
               limit=1.330,  # limit point
               stop=1.300  # stop point
               )

# creating entry orders
con.create_entry_order(symbol='GBP/JPY', is_buy=True,
                       amount=10,
                       limit=150,
                       is_in_pips=False,
                       time_in_force='GTC',
                       rate=105)

# modifying entry orders
id = con.get_order_ids()[-1]
con.change_order_stop_limit(order_id=id, limit=140)
con.change_order(order_id=id, amount=100, rate=110)
con.get_orders()
con.delete_order(id)

# close existing orders
pos = con.get_open_position(id)
pos.close()
con.close_all_for_symbol('GBP/JPY')
con.close_all()


'''
plt.style.use('seaborn')
data['askclose'].plot(figsize=(10, 6))
plt.show()
con.get_accounts().T
con.get_offers(kind='dataframe')
con.get_offers(kind='dataframe')
con.get_offers(kind='dataframe')
con.get_orders().T
con.get_orders().T
con.get_open_positions_summary().T
con.get_accounts_summary().T
con.get_summary().T
con.get_summary().T
con.get_accounts_summary().T
con.get_open_positions().T
con.get_orders().T
con.get_candles('USD/JPY', period='D1')
con.get_candles('USD/JPY', period='D1', columns='bidclose')
con.get_candles('USD/JPY', period='D1', columns=['bidclose'])
con.get_candles('USD/JPY', period='D1').plot()
plot.show()
plt.show()
plt.style.use('seaborn')
plt.show()
con.get_candles('USD/JPY', period='D1')
con.get_candles('USD/JPY', period='D1').plot()
plt.show()
con.get_candles('USD/JPY', period='D1', columns=['bids']).plot()
plt.show()
order = con.create_market_buy_order('USD/JPY', 200)
con.get_orders().T
con.get_open_positions().T
con.get_open_position()['tradeId']
con.get_open_positions()['tradeId']
con.get_open_trade_ids()
tradeId = con.get_open_trade_ids()[-1]
tradeId
con.change_trade_stop_limit(
    tradeId, is_in_pips=False, is_stop=True, rate=113.5)
con.change_trade_stop_limit(
    tradeId, is_in_pips=False, is_stop=False, rate=114.5)
con.get_open_positions().T
con.change_trade_stop_limit(tradeId, is_in_pips=False, is_stop=False, rate=114)
con.close_trade(trade_id=tradeId, amount=2000)
con.close_trade(trade_id=tradeId, amount=200)
con.get_open_positions()
con.get_closed_positions()
con.get_closed_positions().T
con.open_pos{}
con.open_pos()
con.open_pos
order = con.create_market_sell_order('EUR/USD', 100)
con.open_pos
order = con.create_market_sell_order('GBP/USD', 200)
con.open_pos
ops = con.open_pos
ops.keys
ops.keys()

# 5.6 summaries using some loops
for id in ops.keys():
    print(con.get_open_position(id))

for id in ops.keys():
    print(con.get_open_position(id)['open'])


for id in ops.keys():
    print(con.get_open_position(id).get_amount())

for id in ops.keys():
    print(con.get_open_position(id).get_currency())


con.close_all
con.close_all()
'''
