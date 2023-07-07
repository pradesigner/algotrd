#!/usr/bin/env python3

'''
adjacent movement for bars
uu/ud and dd/du ratios
result for 1H, 4H, 1D:
A. all near 1 with no constraints
'''

from algo.tfx import *


def adjmov(fil, df):
    '''
    determines adjacent movement ratios
    '''
    # calculate movement
    df['mov'] = df['close'] - df['open']

    # adjacent concurrency A acc, u up, d down
    i = 0
    Auu = Aud = Add = Adu = 0
    dfsize = len(df) - 1

    for i in range(2, dfsize):
        # adjacent behaviors
        uu = df['mov'].iloc[i-1] > 0 and df['mov'].iloc[i] > 0
        ud = df['mov'].iloc[i-1] > 0 and df['mov'].iloc[i] < 0
        dd = df['mov'].iloc[i-1] < 0 and df['mov'].iloc[i] < 0
        du = df['mov'].iloc[i-1] < 0 and df['mov'].iloc[i] > 0

        if uu:
            Auu += 1
        if ud:
            Aud += 1
        if dd:
            Add += 1
        if du:
            Adu += 1

    print(fil)
    fstr = '{}/{}={:1.2f} {}/{}={:1.2f}'
    print(fstr.format(Auu, Aud, Auu/Aud, Add, Adu, Add/Adu))


# main script
def main():
    tfs = ['1D', '4H', '1H']
    for tf in tfs[:]:
        for fil in fils(tf)[:]:
            print()
            pcf = pcf_assign(fil)
            df = dfcsv(fil)
            df = cleanup(df)

            adjmov(fil, df)


if __name__ == '__main__':
    main()
