#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 17:30:10 2021

@author: nishant.gupta
"""


# This class add the stats for the passed DF 'Close Price' column based
# request params if any.

import numpy as np

date = "Date"
open_price = "Open"
high_price = "High"
low_price = "Low"
close_price = "Close"

class add_stats:
    def ema(DF, period):
        df = DF.copy()
        col_name = 'EMA' + str(period)
        df[col_name] = df[close_price].ewm(span = period, min_periods = period).mean()
        return DF.merge(df.loc[:, [date, col_name]], how = "outer", on = date)
    
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
        return DF.merge(df.loc[:, [date, 'RSI']], how = "outer", on = date)