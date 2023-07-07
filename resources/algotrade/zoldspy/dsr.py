#!/usr/bin/env python3

# dsr tests D SRing theory for W:L and R:R
# usage: na

from algo.tfx import *
from statistics import mean


def maxmin(df, bars):
    '''sets up sr for lookback of bars'''
    df['s'] = df.low.rolling(window=bars).min().shift(1)
    df['r'] = df.low.rolling(window=bars).max().shift(1)


def wl(df, pcf):
    '''determines win:loss'''
    win = los = 0
    for n in range(6, df.index.stop):
        goal = mean([df.s[n], df.r[n]])
        # support
        if df.low[n] < df.s[n]:
            los += 1
        elif df.high[n] > goal:
            win += 1

        # resistance
        if df.high[n] > df.r[n]:
            los += 1
        elif df.low[n] < goal:
            win += 1

    print(win, los, win/los)


# main script
def main():
    tfs = ['1D', '4H', '1H']
    for tf in tfs[:1]:
        for fil in fils(tf)[:1]:
            print()
            pcf = pcf_assign(fil)
            df = dfcsv(fil)
            df = cleanup(df)

            maxmin(df, 6)
            wl(df, pcf)


if __name__ == '__main__':
    main()
