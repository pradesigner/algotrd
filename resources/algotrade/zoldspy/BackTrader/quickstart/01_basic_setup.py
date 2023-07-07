'''
quickstart for backtrader
primary concepts:
    1. lines
    2. index 0
'''

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import backtrader as bt

if __name__ == '__main__':
    cerebro = bt.Cerebro()  # instantiate cerebro engine
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()  # run the cerebro instance
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
