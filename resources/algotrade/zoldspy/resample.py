#!/usr/bin/env python3

'''
resamples fx tickdata files and saves
set timeframe with tf variable
already done for 1H, 4H, 1D
'''

import os
import pandas as pd

# set tf
tf = '1H'

# create sorted the pair dirs in tfx
tfx = './tfx'
dirs = sorted(os.listdir(tfx))

for dir in dirs[1:]:
    dirpath = os.path.join(tfx, dir) # mk pair directory path
    files = sorted(os.listdir(dirpath)) # sort files in pair directory
    savepath = dirpath + '/' + dir.lower() + tf + '.csv' # set pathname
    print(savepath)
    for file in files:
        filepath = os.path.join(dirpath, file)
        df = pd.read_csv(filepath,
                         header=None,
                         usecols=[1, 2, 3],
                         index_col=0)

        # need to do it this way because <4H creates Float64Index issue
        try:
            df.index = pd.to_datetime(df.index)
        except TypeError:
            continue

        df[4] = .5*(df[2]+df[3])
        d1 = df[4].resample(tf).ohlc().dropna().round(5)

        d1.to_csv(savepath, mode='a', header=False)
    print(savepath + ' DONE!')
