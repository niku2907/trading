#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 17:31:17 2021

@author: nishant.gupta
"""

import pandas as pd

from add_stats import add_stats
from data_reader import data_reader 
from simple_ma_strategy_util import simple_ma_strategy_util

from zerodha_ticker_id import name_zerodha_nse_id_dict
from zerodha_ticker_id import shortlisted_tickers_dict

have_cut_off_time_check = 1
num_two_months = 12
ma_period = 44
slope_period = 10 
target_pct = 0.8
sl_pct = 0.4

pick_15_data = 0
pick_5_min_data = 1

test_dict = ({"2953217":"TCS"})
test_dict2 = ({"2955009":"COFORGE"})


tickers_meta_data = {}
date = []

stock_pnl = {}
stock_capital = {}
stock_metadata = {}
stock_transactions = {}
for ticker_id, ticker_name in test_dict2.items():
        num_months = num_two_months * 2
        if (pick_15_data):
            num_minute_data = "15"
        else:
            num_minute_data = "5"
        
        stock_file_name = "2_YEAR_TICKER_DATA/" + ticker_name + "_" + str(num_months) + "_MONTH_" +\
            num_minute_data + "_MINUTE_DATA.xlsx"
        print("********************************************************************")
        print("Processing stock: ", ticker_name)
        five_minute_data = data_reader.read(stock_file_name)
        five_minute_data = add_stats.ema(five_minute_data, ma_period)
        five_minute_data = add_stats.simple_ma(five_minute_data, ma_period)
        sma_column_name = 'SMA' + str(ma_period)
        ema_column_name = 'EMA' + str(ma_period)
        five_minute_data['SMA Slope'] = add_stats.slope(five_minute_data[sma_column_name], slope_period)
        five_minute_data['EMA Slope'] = add_stats.slope(five_minute_data[ema_column_name], slope_period)
        five_minute_data = simple_ma_strategy_util.add_signal(five_minute_data)
        tickers_meta_data[ticker_name] = five_minute_data
        
        transactions = pd.DataFrame(columns = ['Position', 'Buy Time', 'Buy Price', 'Sell Time', 'Sell Price',\
                                               'Pnl', 'Exit Method', 'Num Units', 'Current Capital(k)'])
        total_pnl, capital, five_minute_data['Status'], five_minute_data['Signal'],\
            transactions['Position'],\
            transactions['Buy Time'], transactions['Buy Price'], transactions['Sell Time'],\
                transactions['Sell Price'], transactions['Pnl'], transactions['Exit Method'],\
                    transactions['Num Units'], transactions['Current Capital(k)']= \
            simple_ma_strategy_util.implement_strategy(five_minute_data, target_pct, sl_pct)
            
        stock_pnl[ticker_name] = total_pnl
        stock_capital[ticker_name] = capital
        stock_metadata[ticker_name] = five_minute_data
        stock_transactions[ticker_name] = transactions

# date_ticker_dict = {}
# for i in range(len(date)):
#     current_date = date[i]
#     ticker_list = []
#     open_price_list = []
#     high_price_list = []
#     low_price_list = []
#     close_price_list = []
#     sma_list = []
#     ema_list = []
#     sma_slope_list = []
#     ema_slope_list = []
#     signal_list = []
#     action_list = []
#     for ticker_name, ticker_tickers_meta_data in tickers_meta_data.items():
#         ticker_date = ticker_tickers_meta_data['Date']
#         for j in range(len(ticker_date)):
#             if (current_date == ticker_date[j]):
#                ticker_list.append(ticker_name)
#                open_price_list.append(ticker_tickers_meta_data['Open'][j])
#                high_price_list.append(ticker_tickers_meta_data['High'][j])
#                low_price_list.append(ticker_tickers_meta_data['Low'][j])
#                close_price_list.append(ticker_tickers_meta_data['Close'][j])
               
#                sma_column_name = 'SMA' + str(ma_period)
#                sma_list.append(ticker_tickers_meta_data[sma_column_name][j])
               
#                ema_column_name = 'EMA' + str(ma_period)
#                ema_list.append(ticker_tickers_meta_data[ema_column_name][j])
               
#                sma_slope_list.append(ticker_tickers_meta_data['SMA Slope'][j])
#                ema_slope_list.append(ticker_tickers_meta_data['EMA Slope'][j])
#                signal_list.append(ticker_tickers_meta_data['Signal'][j])
#                action_list.append(ticker_tickers_meta_data['Action'][j])
#                break
    
#     df = pd.DataFrame(columns = ['Ticker', 'Open', 'High', 'Low', 'Close',\
#                                  'EMA', 'EMA Slope', 'SMA', 'SMA Slope', 'Signal', 'Action'])
#     df['Ticker'] = ticker_list
#     df['Open'] = open_price_list
#     df['High'] = high_price_list
#     df['Low'] = low_price_list
#     df['Close'] = close_price_list
#     df['EMA'] = ema_list
#     df['EMA Slope'] = ema_slope_list
#     df['SMA'] = sma_list
#     df['SMA Slope'] = sma_slope_list
#     df['Signal'] = signal_list
#     df['Action'] = action_list
    
#     date_ticker_dict[current_date] = df
   
# simple_ma_strategy_util.implement_strategy(date_ticker_dict, tickers_meta_data, target_pct, sl_pct, date)