#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 17:30:10 2021

@author: nishant.gupta
"""


# This class add the stats for the passed DF 'Close Price' column based
# request params if any.

import numpy as np

from data_reader import data_reader 

close_price = "Close Price"
TS = "TS"

class add_stats:
    def ema(DF, period):
        df = DF.copy()
        col_name = 'EMA' + str(period)
        df[col_name] = df[close_price].ewm(span = period, min_periods = period).mean()
        #df_copy.dropna(inplace = True)
        #return df_copy
        return DF.merge(df.loc[:, [TS, col_name]], how = "outer", on = TS)
    
    def rsi(DF, n):
        df = DF.copy()
        df['delta'] = df[close_price] - df[close_price].shift(1)
        df['gain'] = np.where(df['delta'] >= 0, df['delta'], 0)
        df['loss']= np.where(df['delta'] < 0, abs(df['delta']), 0)
        avg_gain = []
        avg_loss = []
        gain = df['gain'].tolist()
        loss = df['loss'].tolist()
        for i in range(len(df)):
            if i < n:
                avg_gain.append(np.NaN)
                avg_loss.append(np.NaN)
            elif i == n:
                avg_gain.append(df['gain'].rolling(n).mean().tolist()[n])
                avg_loss.append(df['loss'].rolling(n).mean().tolist()[n])
            elif i > n:
                avg_gain.append(((n-1)*avg_gain[i-1] + gain[i])/n)
                avg_loss.append(((n-1)*avg_loss[i-1] + loss[i])/n)
        df['avg_gain'] = np.array(avg_gain)
        df['avg_loss'] = np.array(avg_loss)
        df['RS'] = df['avg_gain']/df['avg_loss']
        df['RSI'] = 100 - (100/(1+df['RS']))
        return DF.merge(df.loc[:, [TS, 'RSI']], how = "outer", on = TS)
    
df = data_reader.read("Historical_data.xlsx", "June21")
df = add_stats.ema(df, 3)
df = add_stats.ema(df, 5)
df = add_stats.rsi(df, 5)
        