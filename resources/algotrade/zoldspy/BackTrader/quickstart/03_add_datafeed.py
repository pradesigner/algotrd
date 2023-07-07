'''
quickstart for backtrader
adding datafeed
'''

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import datetime  # for datetime objects
import os.path  # to manage paths
import sys  # to find script name in argv[0]

# import backtrader platform
import backtrader as bt


# create strategy
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        '''Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        '''keep ref to the close lin in dataseries'''
        self.dataclose = self.datas[0].close

    def next(self):
        '''log the closing price of series from ref'''
        self.log('Close, %.2f' % self.dataclose[0])


if __name__ == '__main__':
    # create cerebro entity
    cerebro = bt.Cerebro()

    # add strategy
    cerebro.addstrategy(TestStrategy)

    # find datapath for datas
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '../datas/orc1-1995-2014.txt')

    # create a datafeed
    data = bt.feeds.YahooFinanceCSVData(
        dataname='/home/pradmin/backtrader/datas/orcl-1995-2014.txt',
        # no values before or after these dates
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2000, 12, 31),
        reverse=False)

    # add datafeed to cerebro
    cerebro.adddata(data)

    # set cash
    cerebro.broker.setcash(100000.0)

    # print starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.get_value())

    # run over everything
    cerebro.run()

    # print final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.get_value())
