#!/usr/bin/env python3

'''
compute various characteristics for each bar type
look for effect on next bar


TODO
see prev candle has any bearing on next one - some patterns?
examine diff and graph +- histograms of close or avg prices? 
relate to ticks?
classify pa based on clop, bias, as well as comb possibilities
since clop0-clop1 corr is .97, is there a pattern to when that is broken?
strong corr may not be necessary if we are looking for pips perhaps
'''

from algo.tfx import *


def fillcols(df, pcf):
    '''fills columns with computations'''
    # clop give cl - op thereby also determining direction
    df['clop'] = (df['close'] - df['open'])*pcf

    # hilo gives size of bar and is always +ve
    df['hilo'] = (df['high'] - df['low'])*pcf

    # bias determines where the close finishes
    # +1 is a very high finish
    # 0 being the middle thereby a doji
    # -1 is a very low finish
    hcl = pcf*((df['close']-df['low'])-(df['high']-df['close']))
    df['bias'] = hcl/df['hilo']

    # Dadj is the difference of closes between adjacent bars
    df['cladj'] = df['close'].diff()*pcf


def correlate(df):
    '''determines various correlations'''
    print('clopcladj {:.3f}'.format(df.clop.corr(df.cladj)))
    print('biascladj {:.3f}'.format(df.bias.corr(df.cladj)))


def main():
    tfs = ['1D', '4H', '1H']
    for tf in tfs[:]:
        print('\n', tf)
        for fil in fils(tf)[12:13]:
            print('\n', fil.split('/')[-1])
            pcf = pcf_assign(fil)
            df = dfcsv(fil)
            df = cleanup(df)

            fillcols(df, pcf)
            correlate(df)


if __name__ == '__main__':
    main()


'''
pa goes strange near closing time especially at the end of a week.
we wish to see what sorts of behaviors take place using the 1H

attempt to code a bar somehow so we can detect patterns

set up various descriptors for bars calculated in columns
1. move: cl-op
2. trav: hi-lo
3. bias: cl-lo / hi-cl
4. diff: cl->cl

'''
