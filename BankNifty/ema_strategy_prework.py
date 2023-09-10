# -*- coding: utf-8 -*-
"""
Created on Wed May  3 16:50:59 2023

@author: NishantGupta
"""

import pandas as pd

from add_stats import add_stats
from data_reader import data_reader 

from util import util
from ema_strategy_utils import ema_strategy_util

num_minute_data = "5"

# Change this expand/shorten the time window under consideration
prev_num_years = 1
num_two_months = prev_num_years * 6

file_prefix = str(int(prev_num_years)) + "_YEAR_TICKER_DATA/"
test_dict3 = ({"260105":"BANKNIFTY"})
    

start_execution_error_pct = 0.001
sl_buffer_pct = 0.001

ema_period = 3
buy_sl_pct = 0

buy_allowed = 0
sell_allowed = 1
start_capital = 200000
cash_out_limit = 3000000

stock_metadata = {}
stock_buy_days = {}
stock_sell_days = {}
tickers_meta_data = {}
stock_transactions = {}

stock_stats = {}
stock_pnl = {}
stock_capital = {}
stock_reserves = {}
stock_metadata = {}
stock_transactions = {}
stock_monthly_cash_out_stats = {}

for ticker_id, ticker_name in test_dict3.items():
        num_months = num_two_months * 2
        buy_days = {}
        
        stock_file_name = file_prefix + ticker_name + "_" + str(num_months) + "_MONTH_" +\
            num_minute_data + "_MINUTE_DATA.xlsx"
        five_minute_data = data_reader.read(stock_file_name)
        five_minute_data = add_stats.ema(five_minute_data, ema_period)

        print("********************************************************************")
        print("Processing stock: ", ticker_name)
        transactions = pd.DataFrame(columns = ['Position', 'Buy Time', 'Buy Price', 'Sell Time', 'Sell Price',\
                                               'Pnl', 'Exit Method', 'Num Units', 'Current Capital(k)',\
                                               'Pnl %', 'Total Pnl%', 'Target Price'])
        
        prices = five_minute_data['Close']
        date = five_minute_data['Date']
        ema = five_minute_data['EMA' + str(ema_period)]
        high_prices = five_minute_data['High']
        low_prices = five_minute_data['Low']
        open_prices = five_minute_data['Open']
        
        start_time = '09:15:00'