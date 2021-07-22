#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 01:32:18 2021

@author: nishant.gupta
"""


from add_stats import add_stats

from data_reader import data_reader 

fast_ema = 10
slow_ema = 50

one_minute_data = data_reader.read("NIFTYBANK_ONE_YEAR_DATA.xlsx")
five_minute_data = one_minute_data.iloc[::5]
fifteen_minute_data = one_minute_data.iloc[::15]

one_minute_data = add_stats.ema(one_minute_data, fast_ema)
one_minute_data = add_stats.ema(one_minute_data, slow_ema)
one_minute_data = add_stats.rsi(one_minute_data, 14)
one_minute_data.set_index('Date', inplace=True)
one_minute_data.dropna(inplace = True)

five_minute_data = add_stats.ema(five_minute_data, fast_ema)
five_minute_data = add_stats.ema(five_minute_data, slow_ema)
five_minute_data = add_stats.rsi(five_minute_data, 14)
five_minute_data.set_index('Date', inplace=True)
five_minute_data.dropna(inplace = True)

fifteen_minute_data = add_stats.ema(fifteen_minute_data, fast_ema)
fifteen_minute_data = add_stats.ema(fifteen_minute_data, slow_ema)
fifteen_minute_data = add_stats.rsi(fifteen_minute_data, 14)
fifteen_minute_data.set_index('Date', inplace=True)