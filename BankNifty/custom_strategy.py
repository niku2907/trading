#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 21:23:38 2021

@author: nishant.gupta
"""

import pandas as pd

from add_stats import add_stats
from data_reader import data_reader 

from util import util

from custom_strategy_util import custom_strategy_util
from zerodha_ticker_id import name_zerodha_nse_id_dict
from zerodha_ticker_id import shortlisted_tickers_dict
from zerodha_ticker_id import buy_stocks_dict
from zerodha_ticker_id import sell_stocks_dict

num_two_months = 6
num_minute_data = "5"

stock_metadata = {}
stock_buy_days = {}
stock_sell_days = {}
tickers_meta_data = {}
stock_transactions = {}

stock_stats = {}
stock_pnl = {}
stock_capital = {}
stock_metadata = {}
stock_transactions = {}

test_dict = ({"5215745":"COALINDIA"})
test_dict2 = ({"2955009":"COFORGE"})
    
# Buy params
atr_period = 60
buy_sl_pct = 1.0

# Sell params
fast_ma_period = 12
slow_ma_period = 26
signal_period = 9
st_lookback_period = 20
st_multiplier = 1.8
ema_period = 100
sell_sl_pct = 1.0

buy_allowed = 0
sell_allowed = 1
for ticker_id, ticker_name in sell_stocks_dict.items():
        num_months = num_two_months * 2
        buy_days = {}
        
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
        
        stock_file_name = "1_YEAR_TICKER_DATA/" + ticker_name + "_" + str(num_months) + "_MONTH_" +\
            num_minute_data + "_MINUTE_DATA.xlsx"
        five_minute_data = data_reader.read(stock_file_name)
        five_minute_data = add_stats.ema(five_minute_data, ema_period)
        
        longer_tf_file_name = "1_YEAR_TICKER_DATA/" + ticker_name + "_" +\
            str(num_months) + "_MONTH_60_MINUTE_DATA.xlsx"
        longer_tf_data = data_reader.read(longer_tf_file_name)
        longer_tf_data = add_stats.MACD(longer_tf_data, fast_ma_period, slow_ma_period, signal_period)
        
        five_minute_data['st'], five_minute_data['st_upt'], five_minute_data['st_dt'] = \
            custom_strategy_util.get_supertrend(five_minute_data['High'], five_minute_data['Low'],
                           five_minute_data['Close'], st_lookback_period, st_multiplier)
        
        five_minute_data = five_minute_data[1:]
        
        stock_buy_days[ticker_name] = buy_days
        tickers_meta_data[ticker_name] = five_minute_data
        
        transactions = pd.DataFrame(columns = ['Position', 'Buy Time', 'Buy Price', 'Sell Time', 'Sell Price',\
                                               'Pnl', 'Exit Method', 'Num Units', 'Current Capital(k)'])
        total_pnl, num_buys, num_buy_wins, num_sells, num_sell_wins, capital,\
            five_minute_data['Status'], five_minute_data['Signal'],\
            transactions['Position'],\
            transactions['Buy Time'], transactions['Buy Price'], transactions['Sell Time'],\
                transactions['Sell Price'], transactions['Pnl'], transactions['Exit Method'],\
                    transactions['Num Units'], transactions['Current Capital(k)']= \
            custom_strategy_util.implement_strategy(five_minute_data, buy_sl_pct, buy_days,\
                                                       ema_period, sell_sl_pct, longer_tf_data,\
                                                       buy_allowed, sell_allowed)
        
        stats = {}
        stats['Pnl'] = total_pnl
        stats['Num Trans'] = len(transactions)
        stats['Num Buys'] = num_buys
        stats['Buy Wins'] = num_buy_wins
        stats['Num Sells'] = num_sells
        stats['Sell Wins'] = num_sell_wins
        
        stock_stats[ticker_name] = stats
        stock_pnl[ticker_name] = total_pnl
        stock_capital[ticker_name] = capital
        stock_metadata[ticker_name] = five_minute_data
        stock_transactions[ticker_name] = transactions

ticker_list = []
stat_list_dict = {}
stat_list_dict['Pnl'] = []
stat_list_dict['Num Trans'] = []
stat_list_dict['Num Buys'] = []
stat_list_dict['Buy Wins'] = []
stat_list_dict['Num Sells'] = []
stat_list_dict['Sell Wins'] = []

for ticker_name, value in stock_stats.items():
    ticker_list.append(ticker_name)
    for metric, stat in value.items():
        stat_list_dict[metric].append(stat)

df = pd.DataFrame(columns = ['Ticker', 'Pnl', 'Num Trans', 'Num Buys', 'Buy Wins',\
                             'Num Sells', 'Sell Wins'])
df['Ticker'] = ticker_list
df['Pnl'] = stat_list_dict['Pnl']
df['Num Trans'] = stat_list_dict['Num Trans']
df['Num Buys'] = stat_list_dict['Num Buys']
df['Buy Wins'] = stat_list_dict['Buy Wins']
df['Num Sells'] = stat_list_dict['Num Sells']
df['Sell Wins'] = stat_list_dict['Sell Wins']

daily_transaction_dict = {}
for ticker_name, value in stock_transactions.items():
    for i in range(len(value['Buy Time'])):
        if (daily_transaction_dict.__contains__(util.get_date(value['Buy Time'][i])) == 0):
            daily_transaction_dict[util.get_date(value['Buy Time'][i])] = []
        daily_transaction_dict[util.get_date(value['Buy Time'][i])].append(ticker_name)