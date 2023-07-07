#!/usr/bin/env python3

'''
mlines determine price slopes from various bars
to the 1st bar. the slopes, interestingly, are
very close to the instantaneous slope of the ma
over that many bars.

TODO
interplay between mlines should be of interest in
at least the same way as for ma.
'''

from algo.tfx import *


def mlines(df, pcf):
    '''
    calculates mlines
    '''
    df['avg'] = .5*(df['high']+df['low'])
    for m in [1, 2, 3]:
        mpow = 6**m
        mstr = 'm'+str(mpow)
        df[mstr] = round(pcf*df['avg'].diff(mpow)/mpow)
    df.dropna(inplace=True)
    return df


# main script
def main():
    tfs = ['1D', '4H', '1H']
    for tf in tfs[:1]:
        for fil in fils(tf)[:1]:
            print()
            pcf = pcf_assign(fil)
            df = dfcsv(fil)
            df = cleanup(df)

            df = mlines(df, pcf)
            print(df)


if __name__ == '__main__':
    main()
