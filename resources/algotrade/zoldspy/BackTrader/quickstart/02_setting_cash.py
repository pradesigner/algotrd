'''
quickstart for backtrader
setting cash to other than 10k
'''

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import backtrader as bt

if __name__ == '__main__':
    cerebro = bt.Cerebro()  # instantiate cerebro engine
    cerebro.broker.setcash(100000.0)  # cash to 100k
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()  # run the cerebro instance
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
