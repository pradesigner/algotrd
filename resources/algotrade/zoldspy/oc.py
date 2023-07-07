#!/usr/bin/env python3

# ocm uses oc and m6 on prior candle as direction determiners
# to gain 6,12 pips on present candle
# usage: na

from algo.tfx import *


def mlines(df, pcf):
    '''
    calculates mlines for hilo
    '''
    for m in [1]:
        mpow = 6**m
        mstr = 'm'+str(mpow)
        df['h'+mstr] = round(pcf*df.high.diff(mpow)/mpow)
        df['l'+mstr] = round(pcf*df.low.diff(mpow)/mpow)
    df.dropna(inplace=True)
    return df


def oc(df, pcf, mnmv):
    '''
    prior candle oc -> h-o, o-l results

    +oc -> oh > +mnmv?
    -oc -> ol < -mnmv?
    '''

    # initialize holo columns
    df['hop'] = 0  # oh when +oc
    df['lon'] = 0  # ol when -oc
    df['hopm'] = 0  # oh when +oc
    df['lonm'] = 0  # ol when -oc

    # define coholo
    df['co'] = pcf*(df.close - df.open)  # oc movement
    df['ho'] = pcf*(df.high - df.open)  # oh movement
    df['lo'] = pcf*(df.low - df.open)  # ol movement

    # loop to find if pre-condition results in success
    for i in df.index[1:-1]:
        # pre-conditions
        cop = df.co[i-1] > 0
        m6p = df.hm6[i-1] > 0 and df.lm6[i-1] > 0
        con = df.co[i-1] < 0
        m6n = df.hm6[i-1] < 0 and df.lm6[i-1] < 0

        # results
        hop = df.ho[i] > +mnmv
        lon = df.lo[i] < -mnmv

        # co
        if cop and hop:
            df.loc[i, 'hop'] = df.ho[i]
        if con and lon:
            df.loc[i, 'lon'] = df.lo[i]

        # co with m
        if cop and m6p and hop:
            df.loc[i, 'hopm'] = df.ho[i]
        if con and m6n and lon:
            df.loc[i, 'lonm'] = df.lo[i]

    # co rate
    co_success = df.hop[(df.hop > 0)].count() + df.lon[(df.lon < 0)].count()
    co_attempts = df.co[(df.co > 0)].count() + df.co[(df.co < 0)].count()
    co_rate = co_success / co_attempts
    print('co_rate = {0:.0f}%'.format(100*co_rate),
          'hop mean = {0:.1f}'.format(df.hop.mean()),
          'lon mean = {0:.1f}'.format(df.lon.mean()))

    # com rate

    com_success = df.hopm[(df.hopm > 0)].count() + \
        df.lonm[(df.lonm < 0)].count()
    com_attempts = df.co[(df.co > 0) & (df.hm6 > 0) & (df.lm6 > 0)].count() + \
        df.co[(df.co < 0) & (df.hm6 < 0) & (df.lm6 < 0)].count()
    com_rate = com_success / com_attempts
    print('com_rate = {0:.0f}%'.format(100*com_rate),
          'hopm mean = {0:.1f}'.format(df.hopm.mean()),
          'lonm mean = {0:.1f}'.format(df.lonm.mean()))


# main script
def main():
    tfs = ['1D', '4H', '1H']
    mnmvs = [6, 12]
    for tf in tfs[:1]:
        for fil in fils(tf)[:1]:
            print()
            pcf = pcf_assign(fil)
            df = dfcsv(fil)
            df = cleanup(df)

            mlines(df, pcf)
            for mnmv in mnmvs:
                print('\n', fil.split('/')[3], ' @ ', mnmv)
                oc(df, pcf, mnmv)


if __name__ == '__main__':
    main()
