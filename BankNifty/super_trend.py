#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 19:21:24 2021

@author: nishant.gupta
"""

import pandas as pd

from add_stats import add_stats
from data_reader import data_reader 
from super_trend_utils import super_trend_utils

from zerodha_ticker_id import name_zerodha_nse_id_dict
from zerodha_ticker_id import shortlisted_tickers_dict

# ema_period = 50
have_cut_off_time_check = 1
# st_lookback_period = 20
# st_multiplier = 1.8
# target_pct = 1.5
# sl_pct = 0.5

num_two_months = 6
num_minute_data = "5"
fast_ma_period = 12
slow_ma_period = 26
signal_period = 9

class experiment_params:
    def __init__(self, ema_period, st_period, st_multiplier, target_pct, sl_pct):
        self.ema_period = ema_period
        self.st_period = st_period
        self.st_multiplier = st_multiplier
        self.target_pct = target_pct
        self.sl_pct = sl_pct

params = []
# EMA experiments.
# params.append(experiment_params(ema_period = 20, st_period = 20, st_multiplier = 1.8,\
#                                 target_pct = 1.5, sl_pct = 0.5))
# params.append(experiment_params(ema_period = 50, st_period = 20, st_multiplier = 1.8,\
#                                 target_pct = 1.5, sl_pct = 0.5))
params.append(experiment_params(ema_period = 100, st_period = 20, st_multiplier = 1.8,\
                                target_pct = 2.5, sl_pct = 0.8))
# params.append(experiment_params(ema_period = 200, st_period = 20, st_multiplier = 1.8,\
#                                 target_pct = 1.5, sl_pct = 0.5))

# ST period experiments.
# params.append(experiment_params(ema_period = 100, st_period = 10, st_multiplier = 3,\
#                                 target_pct = 1.5, sl_pct = 0.5))
# params.append(experiment_params(ema_period = 100, st_period = 25, st_multiplier = 1.2,\
#                                 target_pct = 1.5, sl_pct = 0.5))
# params.append(experiment_params(ema_period = 100, st_period = 30, st_multiplier = 1,\
#                                 target_pct = 1.5, sl_pct = 0.5))

# Target experiments.
# params.append(experiment_params(ema_period = 100, st_period = 20, st_multiplier = 1.8,\
#                                 target_pct = 0.5, sl_pct = 0.5))
# params.append(experiment_params(ema_period = 100, st_period = 20, st_multiplier = 1.8,\
#                                 target_pct = 0.8, sl_pct = 0.5))
# params.append(experiment_params(ema_period = 100, st_period = 20, st_multiplier = 1.8,\
#                                 target_pct = 1.0, sl_pct = 0.5))
# params.append(experiment_params(ema_period = 100, st_period = 20, st_multiplier = 1.8,\
#                                 target_pct = 1.5, sl_pct = 0.5))

# SL experiments.
# params.append(experiment_params(ema_period = 100, st_period = 20, st_multiplier = 1.8,\
#                                 target_pct = 1.5, sl_pct = 0.4))
# params.append(experiment_params(ema_period = 100, st_period = 20, st_multiplier = 1.8,\
#                                 target_pct = 1.5, sl_pct = 0.7))
# params.append(experiment_params(ema_period = 100, st_period = 20, st_multiplier = 1.8,\
#                                 target_pct = 1.5, sl_pct = 0.8))
# params.append(experiment_params(ema_period = 100, st_period = 20, st_multiplier = 1.8,\
#                                 target_pct = 1.5, sl_pct = 1.0))

experiment_results_pnl = {}
experiment_results_capital = {}
experiment_results_metadata = {}
experiment_results_transactions = {}

pick_daily_data = 0
pick_hourly_data = 0
pick_30_min_data = 0
test_dict = ({"2953217":"TCS"})
test_dict2 = ({"119553":"HDFCLIFE"})
test_dict3 = ({"779521":"SBIN"})

for i in range(len(params)):
    stock_pnl = {}
    stock_capital = {}
    stock_metadata = {}
    stock_transactions = {}
    current_params = params[i]
    st_lookback_period = current_params.st_period
    st_multiplier = current_params.st_multiplier
    ema_period = current_params.ema_period
    target_pct = current_params.target_pct
    sl_pct = current_params.sl_pct
    for ticker_id, ticker_name in name_zerodha_nse_id_dict.items():
        num_months = num_two_months * 2
        stock_file_name = "1_YEAR_TICKER_DATA/" + ticker_name + "_" + str(num_months) + "_MONTH_" +\
            num_minute_data + "_MINUTE_DATA.xlsx"
        print("********************************************************************")
        print("Processing stock: ", ticker_name)
        five_minute_data = data_reader.read(stock_file_name)
        five_minute_data = add_stats.ema(five_minute_data, ema_period)
        
        if (pick_daily_data == 1):
            longer_tf_file_name = "1_YEAR_TICKER_DATA/" + ticker_name + "_" + str(num_months) +\
            "_MONTH_DAILY_DATA.xlsx"
        elif (pick_hourly_data == 1):
            longer_tf_file_name = "1_YEAR_TICKER_DATA/" + ticker_name + "_" +\
            str(num_months) + "_MONTH_60_MINUTE_DATA.xlsx"
        elif (pick_30_min_data == 1):
            longer_tf_file_name = "1_YEAR_TICKER_DATA/" + ticker_name + "_" +\
            str(num_months) + "_MONTH_30_MINUTE_DATA.xlsx"
        else:
            longer_tf_file_name = "1_YEAR_TICKER_DATA/" + ticker_name + "_" +\
            str(num_months) + "_MONTH_15_MINUTE_DATA.xlsx"
        
        longer_tf_data = data_reader.read(longer_tf_file_name)
        longer_tf_data = add_stats.MACD(longer_tf_data, fast_ma_period, slow_ma_period, signal_period)
        
        five_minute_data['st'], five_minute_data['st_upt'], five_minute_data['st_dt'] = \
            super_trend_utils.get_supertrend(five_minute_data['High'], five_minute_data['Low'],
                           five_minute_data['Close'], st_lookback_period, st_multiplier)
        
        five_minute_data = five_minute_data[1:]
        
        transactions = pd.DataFrame(columns = ['Position', 'Buy Time', 'Buy Price', 'Sell Time', 'Sell Price',\
                                               'Pnl', 'Exit Method', 'Num Units', 'Current Capital(k)'])
        total_pnl, capital, five_minute_data['Status'], five_minute_data['Signal'],\
            transactions['Position'],\
            transactions['Buy Time'], transactions['Buy Price'], transactions['Sell Time'],\
                transactions['Sell Price'], transactions['Pnl'], transactions['Exit Method'],\
                    transactions['Num Units'], transactions['Current Capital(k)']= \
            super_trend_utils.implement_st_strategy(five_minute_data, have_cut_off_time_check,\
                                                    ema_period, target_pct, sl_pct, longer_tf_data)
        
        transactions.set_index("Position", inplace=True)
        stock_pnl[ticker_name] = total_pnl
        stock_capital[ticker_name] = capital
        stock_metadata[ticker_name] = five_minute_data
        stock_transactions[ticker_name] = transactions
        
        #super_trend_utils.plot_super_trend_band(five_minute_data)
    
    dict_key = "EMA:" + str(current_params.ema_period) + "_" + "PER:" + str(current_params.st_period) + "_"\
        + "MULT:" + str(current_params.st_multiplier) + "_" + "T:" + str(current_params.target_pct) + "_"\
            + "SL:" + str(current_params.sl_pct)
    experiment_results_pnl[dict_key] = stock_pnl
    experiment_results_capital[dict_key] = stock_capital
    experiment_results_metadata[dict_key] = stock_metadata
    experiment_results_transactions[dict_key] = stock_transactions