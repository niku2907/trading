# -*- coding: utf-8 -*-
"""
Created on Fri May 26 18:32:58 2023

@author: NishantGupta
"""

import pandas as pd
import talib

from add_stats import add_stats
from data_reader import data_reader 

from util import util
from traffic_light_strategy_utils_v2 import traffic_light_strategy_util_v2
from traffic_light_strategy_utils import traffic_light_strategy_util

from zerodha_ticker_id import name_zerodha_nse_id_dict
from zerodha_ticker_id import shortlisted_tickers_dict
from zerodha_ticker_id import buy_stocks_dict
from zerodha_ticker_id import sell_stocks_dict
from zerodha_ticker_id import mid_cap_stocks_dict
from zerodha_ticker_id import mid_cap_sell_stocks_dict
from zerodha_ticker_id import next_fifty_stocks_dict
from zerodha_ticker_id import buy_stocks_dict_low_capital
from zerodha_ticker_id import sell_stocks_dict_low_capital
from zerodha_ticker_id import sell_stocks_dict_low_capital_new
from zerodha_ticker_id import name_zerodha_nse_fno_dict
from zerodha_ticker_id import fno_shortlists_dict

test_dict3 = ({})

num_minute_data = "15"

# Change this expand/shorten the time window under consideration
prev_num_years = 6
num_two_months = prev_num_years * 6

file_prefix = str(int(prev_num_years)) + "_YEAR_TICKER_DATA/"

#num_two_months = 6
bank_nifty_simulation = 1
nifty_simulation = 0

ticker_name = ""
if bank_nifty_simulation == 1:
    test_dict3 = ({"260105":"BANKNIFTY"})
    price_per_lot = 150000
    lot_size = 25
    ticker_name = "BANKNIFTY"
elif nifty_simulation == 1:
    test_dict3 = ({"256265":"NIFTY"})
    price_per_lot = 110000
    lot_size = 50
    ticker_name = "NIFTY"
else:
    test_dict3 = {**name_zerodha_nse_id_dict, **mid_cap_stocks_dict, **next_fifty_stocks_dict}
    test_dict3 = ({"341249":"HDFCBANK"})
    price_per_lot = -1
    lot_size = -1
    

start_execution_error_pct = 0.001
sl_buffer_pct = 0.001

ema_period = 8

sell_sl_pct = 5
buy_sl_pct = 5

buy_allowed = 1
sell_allowed = 1

start_capital = 500000
cash_out_limit = 300000000

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

is_v2_enabled = 1
for ticker_id, ticker_name in test_dict3.items():
        num_months = num_two_months * 2
        buy_days = {}
        
        stock_file_name = file_prefix + ticker_name + "_" + str(num_months) + "_MONTH_" +\
            num_minute_data + "_MINUTE_DATA.xlsx"
        five_or_fifteen_minute_data = data_reader.read(stock_file_name)
        five_or_fifteen_minute_data = \
            add_stats.ema(five_or_fifteen_minute_data, ema_period)


        print("********************************************************************")
        print("Processing stock: ", ticker_name)
        transactions = pd.DataFrame(columns = ['Position', 'Buy Time', 'Buy Price', 'Sell Time', 'Sell Price',\
                                               'Pnl', 'Exit Method', 'Num Units', 'Current Capital(k)',\
                                               'Pnl %', 'Total Pnl%', 'Target Price'])
        if is_v2_enabled == 1:
            traffic_light_strategy = traffic_light_strategy_util_v2(five_or_fifteen_minute_data,\
                                                                    start_capital,\
                                                                    price_per_lot,\
                                                                    lot_size,\
                                                                    buy_allowed,\
                                                                    sell_allowed,
                                                                    cash_out_limit)
            total_pnl, num_buys, num_buy_wins, num_sells, num_sell_wins, capital, reserves,\
                five_or_fifteen_minute_data['Status'], five_or_fifteen_minute_data['Signal'],\
                transactions['Position'],\
                transactions['Buy Time'], transactions['Buy Price'], transactions['Sell Time'],\
                transactions['Sell Price'], transactions['Pnl'], transactions['Exit Method'],\
                transactions['Num Units'], transactions['Current Capital(k)'], \
                transactions['Pnl %'], transactions['Total Pnl%'], transactions['Target Price'],\
                pnl_per_day_of_month_dict, monthly_cash_out_stats, monthly_pos_exit_stats_dict_buy,\
                daily_pos_exit_stats_dict_buy, monthly_pos_exit_stats_dict_sell,\
                daily_pos_exit_stats_dict_sell = \
                    traffic_light_strategy.implement_strategy()
        else:
            total_pnl, num_buys, num_buy_wins, num_sells, num_sell_wins, capital, reserves,\
                five_or_fifteen_minute_data['Status'], five_or_fifteen_minute_data['Signal'],\
                transactions['Position'],\
                transactions['Buy Time'], transactions['Buy Price'], transactions['Sell Time'],\
                transactions['Sell Price'], transactions['Pnl'], transactions['Exit Method'],\
                transactions['Num Units'], transactions['Current Capital(k)'], \
                transactions['Pnl %'], transactions['Total Pnl%'], transactions['Target Price'],\
                pnl_per_day_of_month_dict, monthly_cash_out_stats, monthly_pos_exit_stats_dict_buy,\
                daily_pos_exit_stats_dict_buy, monthly_pos_exit_stats_dict_sell,\
                daily_pos_exit_stats_dict_sell = \
                    traffic_light_strategy_util.implement_strategy(five_or_fifteen_minute_data,\
                                                                    buy_sl_pct,\
                                                                    ema_period,\
                                                                    sell_sl_pct,\
                                                                    buy_allowed,\
                                                                    sell_allowed,\
                                                                    start_capital,\
                                                                    cash_out_limit,\
                                                                    start_execution_error_pct,\
                                                                    sl_buffer_pct,\
                                                                    price_per_lot,\
                                                                    lot_size)
        
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
        stock_reserves[ticker_name] = reserves
        stock_metadata[ticker_name] = five_or_fifteen_minute_data
        stock_transactions[ticker_name] = transactions
        stock_monthly_cash_out_stats[ticker_name] = monthly_cash_out_stats

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
        
stock_capital_list = []
for ticker_name, value in stock_capital.items():
    stock_capital_list.append(value)

stock_reserves_list = []
for ticker_name, value in stock_reserves.items():
    stock_reserves_list.append(value/pow(10, 5))

df = pd.DataFrame(columns = ['Ticker', 'Pnl', 'Num Trans', 'Num Buys', 'Buy Wins',\
                             'Num Sells', 'Sell Wins', 'Capital', 'Reserves(Lakhs)'])
df['Ticker'] = ticker_list
df['Pnl'] = stat_list_dict['Pnl']
df['Num Trans'] = stat_list_dict['Num Trans']
df['Num Buys'] = stat_list_dict['Num Buys']
df['Buy Wins'] = stat_list_dict['Buy Wins']
df['Num Sells'] = stat_list_dict['Num Sells']
df['Sell Wins'] = stat_list_dict['Sell Wins']
df['Capital'] = stock_capital_list
df['Reserves(Lakhs)'] = stock_reserves_list

daily_transaction_dict = {}
for ticker_name, value in stock_transactions.items():
    for i in range(len(value['Buy Time'])):
        if (daily_transaction_dict.__contains__(util.get_date(value['Buy Time'][i])) == 0):
            daily_transaction_dict[util.get_date(value['Buy Time'][i])] = []
        daily_transaction_dict[util.get_date(value['Buy Time'][i])].append(ticker_name)
        
monthly_wins_dict = {}
for ticker_name, value in stock_transactions.items():
    if (monthly_wins_dict.__contains__(ticker_name) == 0):
        monthly_wins_dict[ticker_name] = {}
    for i in range(len(value['Buy Time'])):
        month_year = util.get_month_year(value['Buy Time'][i])
        if util.is_first_before_than_second(value['Buy Time'][i], value['Sell Time'][i]):
            month_year = util.get_month_year(value['Sell Time'][i])
        if (monthly_wins_dict[ticker_name].__contains__(month_year) == 0):
            monthly_wins_dict[ticker_name][month_year] = [0, 0, 0, value['Current Capital(k)'][i]]
        
        if (value['Pnl'][i] > 0):
            monthly_wins_dict[ticker_name][month_year][0] += 1
        else:
            monthly_wins_dict[ticker_name][month_year][1] += 1
            
        #TODO: Fix the stat around monthly pnl
        monthly_wins_dict[ticker_name][month_year][2] += value['Pnl'][i]/1000
        monthly_wins_dict[ticker_name][month_year][3] = value['Current Capital(k)'][i]

# Reconcile monthly_wins_dict with monthly_pos_exit_stats_dict_sell because
# we can have more entries in monthly_pos_exit_stats_dict_sell or 
# monthly_pos_exit_stats_dict_buy compared to monthly_wins_dict,
# if no transaction was done in that month.
for month_year, value in monthly_pos_exit_stats_dict_sell.items():
    if monthly_wins_dict[ticker_name].__contains__(month_year) == 0:
        last_month_end_capital = 0
        if monthly_wins_dict[ticker_name].__contains__(util.get_last_month(month_year)) == 1:
            last_month_end_capital =\
                monthly_wins_dict[ticker_name][util.get_last_month(month_year)][3]
        monthly_wins_dict[ticker_name][month_year] = [0, 0, 0,\
                                                      last_month_end_capital]
    
month_list = []
start_capital_list = []
end_capital_list = []
wins_pct_list = []
roi_list = []

for ticker_name, value in monthly_wins_dict.items():
    prev_month_end_capital = start_capital
    for month_year, stat in value.items():
        month_list.append(month_year)
        current_start_capital = prev_month_end_capital
        current_end_capital = stat[3] * 1000
        if (stock_monthly_cash_out_stats.__contains__(ticker_name)):
            if (stock_monthly_cash_out_stats[ticker_name].__contains__(month_year)):
                current_end_capital += stock_monthly_cash_out_stats[ticker_name][month_year]
        current_roi = 100 * ((current_end_capital - current_start_capital) / current_start_capital)
        start_capital_list.append(current_start_capital / 1000)
        end_capital_list.append(current_end_capital / 1000)
        roi_list.append(current_roi)
        win_pct = 0
        if (stat[0] + stat[1] != 0):
            win_pct = 100 * stat[0]/(stat[0] + stat[1])
        wins_pct_list.append(win_pct)
        prev_month_end_capital = stat[3] * 1000

num_buy_target_list = []
num_buy_sl_list = []
num_buy_cutoff_list = []

for month_year, stat in monthly_pos_exit_stats_dict_buy.items():
    num_buy_target_list.append(stat[0])
    num_buy_sl_list.append(stat[1])
    num_buy_cutoff_list.append(stat[2])
    

num_sell_target_list = []
num_sell_sl_list = []
num_sell_cutoff_list = []

for month_year, stat in monthly_pos_exit_stats_dict_sell.items():
    num_sell_target_list.append(stat[0])
    num_sell_sl_list.append(stat[1])
    num_sell_cutoff_list.append(stat[2])
    
monthly_stats = pd.DataFrame(columns = ['Month', 'Start Capital', 'End Capital',\
                                        'Wins(%)', 'ROI',\
                                        'TARGET BUY', 'SL BUY', 'CUTOFF BUY',\
                                        'TARGET_SELL', 'SL SELL', 'CUTOFF SELL'])
monthly_stats['Month'] = month_list
monthly_stats['Start Capital'] = start_capital_list
monthly_stats['End Capital'] = end_capital_list
monthly_stats['Wins(%)'] = wins_pct_list
monthly_stats['ROI'] = roi_list
monthly_stats['TARGET BUY'] = num_sell_target_list
monthly_stats['SL BUY'] = num_sell_sl_list
monthly_stats['CUTOFF BUY'] = num_sell_cutoff_list
monthly_stats['TARGET SELL'] = num_buy_target_list
monthly_stats['SL SELL'] = num_buy_sl_list
monthly_stats['CUTOFF SELL'] = num_buy_cutoff_list
