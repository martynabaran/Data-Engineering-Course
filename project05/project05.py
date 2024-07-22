# -*- coding: utf-8 -*-
"""lab05.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Nr1TiKB2s_Wo1zc5TFqOYdK2FR89SQ__

## Imports
"""

import pandas as pd
import numpy as np
import json


######### ZADANIE 1 ######
params = {}
with open('proj5_params.json') as f:
    params = json.load(f)
print(params)

df = pd.read_csv("proj5_timeseries.csv")

df.columns = df.columns.str.lower().str.replace(r"[^a-z]", "_", regex=True)



df['date'] = pd.to_datetime(df['date'], format='mixed')
df.set_index('date', inplace=True)

df = df.asfreq(params['original_frequency'])


df.to_pickle("proj5_ex01.pkl")
df_copy = df.copy()



####### ZADANIE 2 #######
df = df_copy.copy()
df = df.asfreq(params['target_frequency'])

df.to_pickle("proj5_ex02.pkl")


####### ZADANIE 3 ############
df = df_copy.copy()
df = df.resample(str(params['downsample_periods']) + params['downsample_units']).sum(min_count=params['downsample_periods'])

df.to_pickle("proj5_ex03.pkl")


######### ZADANIE 4 ##############
df = df_copy.copy()

df = df.resample(str(params['upsample_periods']) + params['upsample_units']).interpolate(params['interpolation'], order=params['interpolation_order'])


ratio = pd.Timedelta(params['upsample_periods'], params['upsample_units']) / pd.Timedelta(1, params['original_frequency'])
df *= ratio


df.to_pickle("proj5_ex04.pkl")


########## ZADANIE 5 ##############
df = pd.read_pickle("proj5_sensors.pkl")


df = df.pivot(columns='device_id', values='value')


new_index = pd.date_range(start=df.index.round("1min").min(), end=df.index.round("1min").max(), freq=str(params['sensors_periods']) + str(params['sensors_units']))
df = df.reindex(new_index.union(df.index)).interpolate()
df = df.reindex(new_index)


df = df.dropna()

df.to_pickle("proj5_ex05.pkl")
