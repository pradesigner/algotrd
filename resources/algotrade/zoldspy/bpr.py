#!/usr/bin/env python3

'''
bounsr penesr ratios
determines ratio bounsr:penesr at sr
'''

from algo.tfx import *
from collections import deque


def srstats(df, pcf, fil):
    '''
    determines stats for bounsr and penesr

    (note: fil, df, pcf used as global variables)
    2. go through df finding nu and assign as sr
    3. examine bounsr, penesr results
    '''

    def pips(srtype, srvalue, ind):
        '''counts pip movement over 6 bars for bounsr and penesr'''
        bpdfD = {'br': boundf, 'bs': boundf, 'pr': penedf, 'ps': penedf}

        bpdf = bpdfD[srtype]
        bpdfindx = bpdf.index.max()+1
        pipdiff = np.empty([1, 6], dtype=float)
        for i in range(6):
            indx = ind+i
            # compute pipdiff depending on srtype
            pipdiff[0, i] = \
                (srvalue - df['low'][indx])*pcf \
                if srtype in ['br', 'ps'] else \
                (df['high'][indx] - srvalue)*pcf
            # can also do with regular if-else
            # if srtype in ['br', 'ps']:  # br or ps
            #     pipdiff[0, i] = (srvalue - df['low'][indx])*pcf
            # else:  # otherwise bs or pr
            #     pipdiff[0, i] = (df['high'][indx] - srvalue)*pcf
        bpdf.loc[bpdfindx] = pipdiff[0]

    # setup variables
    m = 12/pcf  # sr delta width
    nozone = 7  # df nozone size for beg|end
    beg = nozone  # start df loop at 5
    end = df.index.stop - nozone  # stop at dfsize
    ndigits = int(log10(pcf)) - 1  # roundoff based on pair
    penelimit = 2  # how many penesr before removal of sr to nstack

    # set up r and s stacks
    rstack = deque()  # resistance
    sstack = deque()  # support
    nstack = deque()  # nulled

    # set up bounsr and penesr dataframes
    cols = ['bar1', 'bar2', 'bar3', 'bar4', 'bar5', 'bar6']
    boundf = pd.DataFrame(index=[0], columns=cols)
    penedf = pd.DataFrame(index=[0], columns=cols)

    boun = pene = 0
    for i in range(beg, end):  # i is the df index

        # identify nu progressing through df and put on srstacks
        mmi = i-2  # maxmin index is nusize away from i
        # catch n
        mx = max(df['high'][i-4:i+1])
        if df['high'][mmi] == mx:
            mx = round(mx, ndigits)
            df.loc[mmi, 'n'] = mx
            rstack.append([mx, 0])
        # catch u
        mn = min(df['low'][i-4:i+1])
        if df['low'][mmi] == mn:
            mn = round(mn, ndigits)
            df.loc[mmi, 'u'] = mn
            sstack.append([mn, 0])

        # set loch variables
        lo = df.low[i]
        cl = df.close[i]
        op = df.open[i]
        hi = df.high[i]

        # handle bounsr and penesr
        if rstack:
            r = rstack[-1][0]
            rm = r-m
            if (cl < rm < hi):  # rboun
                pips('br', r, i)
                boun += 1
            if (op < r < cl):  # rpene
                pips('pr', r, i)
                pene += 1
                rpop = rstack.pop()
                if rpop[1] == penelimit:
                    nstack.append(rpop)
                else:
                    rpop[1] += 1
                    sstack.append(rpop)
        if sstack:
            s = sstack[-1][0]
            sm = s+m
            if (lo < sm < cl):  # sboun
                pips('bs', s, i)
                boun += 1
            if (op > s > cl):  # spene
                pips('ps', s, i)
                pene += 1
                spop = sstack.pop()
                if spop[1] == penelimit:
                    nstack.append(spop)
                else:
                    spop[1] += 1
                    rstack.append(spop)

    # clear out nan
    boundf.dropna(inplace=True)
    penedf.dropna(inplace=True)

    # printouts
    prnt(fil, '{} {} {}'.format(
        boun, pene, round(boun/pene)))
    print()

    # print('\nbounsr summary')
    # print(boundf.describe())

    # print('\npenesr summary')
    # print(penedf.describe())
    # print('\n')


def nurt(lookbak):
    ''' finds real time nu from present'''
    sidesize = 2
    lbar = df.index.stop - 1
    fbar = lbar - lookbak
    for i in range(lbar, fbar, -1):
        mid = i-sidesize
        lef = mid-sidesize
        rig = i+1
        mn = df.low.iloc[mid]
        mx = df.high.iloc[mid]
        if mn == min(df.low[lef:rig]):
            df.loc[mid, 'u'] = mn
        if mx == max(df.high[lef:rig]):
            df.loc[mid, 'n'] = mx


# main script
def main():
    tfs = ['1D', '4H', '1H']
    for tf in tfs[:1]:
        for fil in fils(tf)[:1]:
            print()
            pcf = pcf_assign(fil)
            df = dfcsv(fil)
            df = cleanup(df)

            # nurt(33)

            srstats(df, pcf, fil)

        print()


if __name__ == '__main__':
    main()


'''
TODO
#1
early nu if c1,c2 C3 c4 passes C3 hilo?

#2
can we increase bpr by incorporating nu trends?
nu1 - most recent nu to current price
nu2 - adjacent nu to nu1

neg
u1<u2 -
n1<n2 --
nu1<nu2 ---

pos
n1>n2 +
u1>u2 ++
nu1>nu2 +++

neu
nu1=nu2
n1<n2 & u1>u2
n1>n2 & u1<u2

'''
