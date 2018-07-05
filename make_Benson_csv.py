import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time, date
from os.path import join

def make_Benson_csv(inputfilepath, outputfilepath):

    df1 = pd.read_csv(inputfilepath)
    print(df1.head(5))

    ## strip whitespace in column headers
    newcolumns = df1.columns.str.strip()
    df1.columns = newcolumns

    df1['DATETIME'] = df1['DATE'] + ' ' + df1['TIME']
    df1['DATETIME'] = pd.to_datetime(df1['DATETIME'])

    df1['WEEKDAY'] = df1['DATETIME'].dt.dayofweek

    df1['ENTRY_DIFFS'] = (df1
                        .sort_values(by=['STATION','UNIT', 'C/A', 'SCP'])[['STATION','UNIT', 'C/A', 'SCP', 'ENTRIES', 'EXITS', 'DATETIME']]
                        .groupby(['STATION', 'UNIT', 'C/A', 'SCP'])['ENTRIES']
                        .diff())
    df1['EXIT_DIFFS'] = (df1
                        .sort_values(by=['STATION','UNIT', 'C/A', 'SCP'])[['STATION','UNIT', 'C/A', 'SCP', 'ENTRIES', 'EXITS', 'DATETIME']]
                        .groupby(['STATION', 'UNIT', 'C/A', 'SCP'])['EXITS']
                        .diff())

    ## purge values that don't make any sense in ENTRY_DIFFS and EXIT_DIFFS
    df1.loc[df1['ENTRY_DIFFS'] < 0, 'ENTRY_DIFFS'] = float('nan')
    df1.loc[df1['ENTRY_DIFFS'] > 100000, 'ENTRY_DIFFS'] = float('nan')
    df1.loc[df1['EXIT_DIFFS'] < 0, 'EXIT_DIFFS'] = float('nan')
    df1.loc[df1['EXIT_DIFFS'] > 100000, 'EXIT_DIFFS'] = float('nan')

    df1['TOTAL_TRAFFIC'] = df1['EXIT_DIFFS'] + df1['ENTRY_DIFFS']

    def get_ddate(row):
        if row['DATETIME'].time() == time(0,0):
            return row['DATETIME'].date() - timedelta(days=1)
        else:
            return row['DATETIME'].date()
    df1['DDATE'] = df1.apply(get_ddate, axis=1)
    df1['DWEEKDAY'] = pd.to_datetime(df1['DDATE']).dt.dayofweek

    df1.to_csv(outputfilepath)