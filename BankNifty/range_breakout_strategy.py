#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 09:24:59 2021

@author: nishant.gupta
"""

import pandas as pd

from add_stats import add_stats
from data_reader import data_reader 

from util import util

from range_breakout_strategy_util import range_breakout_strategy_util
from zerodha_ticker_id import name_zerodha_nse_id_dict
from zerodha_ticker_id import shortlisted_tickers_dict

num_two_months = 6
num_minute_data = "5"

atr_period = 60
target_pct = 0.8
sl_pct = 1.0

stock_metadata = {}
stock_buy_days = {}
stock_sell_days = {}
tickers_meta_data = {}
stock_transactions = {}
    
stock_pnl = {}
stock_capital = {}
stock_metadata = {}
stock_transactions = {}

test_dict = ({"2953217":"TCS"})
test_dict2 = ({"2955009":"COFORGE"})

for ticker_id, ticker_name in name_zerodha_nse_id_dict.items():
        num_months = num_two_months * 2
        buy_days = {}
        sell_days = {}
        
        stock_file_name = "1_YEAR_TICKER_DATA/" + ticker_name + "_" + str(num_months) +\
            "_MONTH_DAILY_DATA.xlsx"

        print("********************************************************************")
        print("Processing stock: ", ticker_name)
        daily_data = data_reader.read(stock_file_name)
        daily_data = add_stats.ATR(daily_data, atr_period)
        daily_data = add_stats.beyond_ATR(daily_data)
        stock_metadata[ticker_name] = daily_data
        
        for i in range(len(daily_data)):
            if (daily_data['CanBuy'][i] == True):
                buy_days[util.get_date(daily_data['Date'][i])] =\
                    daily_data['Close'][i-1] + daily_data['ATR'][i]
                
            # if (daily_data['CanSell'][i] == True):
            #     sell_days[util.get_date(daily_data['Date'][i])] =\
            #         daily_data['Close'][i-1] - daily_data['ATR'][i]
        
        stock_file_name = "1_YEAR_TICKER_DATA/" + ticker_name + "_" + str(num_months) + "_MONTH_" +\
            num_minute_data + "_MINUTE_DATA.xlsx"
        five_minute_data = data_reader.read(stock_file_name)
        
        stock_buy_days[ticker_name] = buy_days
        stock_sell_days[ticker_name] = sell_days
        tickers_meta_data[ticker_name] = five_minute_data
        
        transactions = pd.DataFrame(columns = ['Position', 'Buy Time', 'Buy Price', 'Sell Time', 'Sell Price',\
                                               'Pnl', 'Exit Method', 'Num Units', 'Current Capital(k)'])
        total_pnl, capital, five_minute_data['Status'], five_minute_data['Signal'],\
            transactions['Position'],\
            transactions['Buy Time'], transactions['Buy Price'], transactions['Sell Time'],\
                transactions['Sell Price'], transactions['Pnl'], transactions['Exit Method'],\
                    transactions['Num Units'], transactions['Current Capital(k)']= \
            range_breakout_strategy_util.implement_strategy(five_minute_data, target_pct, sl_pct, buy_days,\
                                                       sell_days)
            
        stock_pnl[ticker_name] = total_pnl
        stock_capital[ticker_name] = capital
        stock_metadata[ticker_name] = five_minute_data
        stock_transactions[ticker_name] = transactions