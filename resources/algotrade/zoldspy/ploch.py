#!/usr/bin/env python3

'''
best way to enter new days candle might be
in the first half-hour of sidney open
because new york is still open so spread is low
but it is unlikely price will move much till 
new candle starts at 2pm
this is a non-issue when working with lower tf
'''

# ploch.py patterns of loch
# utilizes prior candle loch pattern to predict present candle pa
# usage: na

from algo.tfx import *

# main script #
for fil in fils('1D')[:1]:
    print('\n', fil)
    pcf = pcf_assign(fil)
    df = dfcsv(fil)
    df = cleanup(df)
