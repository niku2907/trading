#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 20:25:18 2021

@author: nishant.gupta
"""

import pandas as pd

from add_stats import add_stats
from data_reader import data_reader 

from util import util

from zerodha_ticker_id import name_zerodha_nse_id_dict
from zerodha_ticker_id import buy_stocks_dict

num_two_months = 6
atr_period = 60

stock_buy_levels = {}
for ticker_id, ticker_name in buy_stocks_dict.items():
        num_months = num_two_months * 2
        stock_file_name = "1_YEAR_TICKER_DATA/" + ticker_name + "_" + str(num_months) +\
            "_MONTH_DAILY_DATA.xlsx"

        print("********************************************************************")
        print("Processing stock: ", ticker_name)
        daily_data = data_reader.read(stock_file_name)
        daily_data = add_stats.ATR(daily_data, atr_period)
        
        buy_level = daily_data['ATR'][len(daily_data) - 1] + daily_data['Close'][len(daily_data) - 1]
        sell_level = daily_data['Close'][len(daily_data) - 1] - daily_data['ATR'][len(daily_data) - 1]
        stock_buy_levels[ticker_name] = buy_level

trigger = pd.DataFrame(stock_buy_levels.items(), columns=['Ticker', 'Trigger Price'])