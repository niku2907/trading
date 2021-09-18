#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 20:01:13 2021

@author: nishant.gupta
"""

# Strategy:
#   Whenever an inside candle is seen and if the parent candle is:
#   1. Green: We trigger a buy as soon as high of the parent candle is taken out on the 1min chart. SL is low of the 
#             child candle.
#   2. Red: We trigger a sell order as soon as low of the parent candle is taken out on the 1min chart. SL is high of
#           the child candle.

import pandas as pd

from add_stats import add_stats
from data_reader import data_reader 
from util import util

# Config parameters
lot_size = 25
num_lots = 1
time_to_start_trade = '09:14:00'
cut_off_time_to_start = '14:30:00'
cut_off_time_to_close = '15:00:00'
parent_candle_length = 40
rr_ratio = 2

# Fetch 15 min data from xls and add metadata for inside candle
fifteen_minute_data = data_reader.read("NIFTYBANK_ONE_YEAR_15_MINUTE_DATA.xlsx")
fifteen_minute_data = add_stats.inside_candle_info(fifteen_minute_data, parent_candle_length)
fifteen_minute_data.set_index('Date', inplace=True)
fifteen_minute_dict = fifteen_minute_data.to_dict()
fifteen_minute_metadata_dict = {}
for date, high_price in fifteen_minute_dict['High'].items():
    fifteen_minute_metadata_dict[date] = {}
    fifteen_minute_metadata_dict[date]['High'] = high_price

for date, low_price in fifteen_minute_dict['Low'].items():
    fifteen_minute_metadata_dict[date]['Low'] = low_price
    
for date, is_child_candle in fifteen_minute_dict['IsChild'].items():
    fifteen_minute_metadata_dict[date]['IsChild'] = is_child_candle
    
for date, TP in fifteen_minute_dict['TP'].items():
    fifteen_minute_metadata_dict[date]['TP'] = TP
    
for date, signal in fifteen_minute_dict['Signal'].items():
    fifteen_minute_metadata_dict[date]['Signal'] = signal

for date, sl in fifteen_minute_dict['SL'].items():
    fifteen_minute_metadata_dict[date]['SL'] = sl
    
for date, target in fifteen_minute_dict['Target'].items():
    fifteen_minute_metadata_dict[date]['Target'] = target

# Fetch 1 min data from xls
one_minute_data = data_reader.read("NIFTYBANK_ONE_YEAR_1_MINUTE_DATA.xlsx")
one_minute_data.set_index('Date', inplace=True)
one_minute_dict = one_minute_data.to_dict()
one_minute_ohlc_dict = {}
for date, open_price in one_minute_dict['Open'].items():
    one_minute_ohlc_dict[date] = {}
    one_minute_ohlc_dict[date]['Open'] = open_price

for date, high_price in one_minute_dict['High'].items():
    one_minute_ohlc_dict[date]['High'] = high_price
    
for date, low_price in one_minute_dict['Low'].items():
    one_minute_ohlc_dict[date]['Low'] = low_price
    
for date, close_price in one_minute_dict['Close'].items():
    one_minute_ohlc_dict[date]['Close'] = close_price

# Actual simulation of the strategy starts here
open_trade = False
pl_dict = {}
pl_dict_yearly = {}
num_trades_yearly = {}
num_trades_per_day_dict = {}
num_trades = 0
transactions = []
last_transaction_date = ''
total_pl = 0
total_pnl_excluding_taxes = 0
transactions = []

class transaction_request_params:
    def __init__(self, signal, trigger_price, target, sl, start_date, cut_off_time_to_close_date,\
                 cut_off_time_to_start_date, current_date):
        self.signal = signal
        self.trigger_price = trigger_price
        self.target = target
        self.sl = sl
        self.start_date = start_date
        self.cut_off_time_to_close_date = cut_off_time_to_close_date
        self.cut_off_time_to_start_date = cut_off_time_to_start_date
        self.current_date = current_date

class transaction_result_params:
    def __init__(self, transaction_start_date = '-', start_price = -1,\
                 transaction_end_date = '-', end_price = -1, is_long_trade = False,\
                 pnl = -1, pnl_untaxed = -1):
        self.transaction_start_date = transaction_start_date
        self.start_price = start_price
        self.transaction_end_date = transaction_end_date
        self.end_price = end_price
        self.is_long_trade = is_long_trade
        self.pnl = pnl
        self.pnl_untaxed = pnl_untaxed

def get_buy_sell_price(start_price, end_price, is_long_trade):
    if (is_long_trade):
        return start_price, end_price
    else:
        return end_price, start_price

def trade_on_one_min_chart(one_minute_ohlc_dict, transaction_req_params):
    #print("Request params: ", transaction_req_params)
    is_triggered = False
    trade_type = ''
    transaction_result = transaction_result_params()
    done = False
    for date_one_min, value in one_minute_ohlc_dict.items():
            if (util.get_date(date_one_min) > transaction_req_params.current_date):
                break
            
            if (date_one_min < transaction_req_params.start_date or \
                util.get_time(date_one_min) >= transaction_req_params.cut_off_time_to_start_date):
                continue
            
            if (transaction_req_params.signal == 'Long'):
                if (value['Close'] > transaction_req_params.trigger_price):
                    if (is_triggered == False):
                        is_triggered = True
                        trade_type = 'Buy'
                        continue
            
            elif (transaction_req_params.signal == 'Short'):
                if (value['Close'] < transaction_req_params.trigger_price):
                    if (is_triggered == False):
                        trade_type = 'Sell'
                        is_triggered = True
                        continue
            
            
            if (is_triggered == False):
                continue
            
            print("One min start date: ", date_one_min, " 15min date: ",\
                  transaction_req_params.start_date, ' current date: ',\
                  transaction_req_params.current_date)
            start_price = value['Open']
            start_date = date_one_min
            print(trade_type, " trade initiated at: ", start_date, " Price: ", start_price)
            open_trade = True
            current_pnl = 0
            current_pnl_excluding_taxes = 0
            for end_date, value_end in one_minute_ohlc_dict.items():
                if (end_date <= start_date):
                    continue
                
                # print("End Date: ", end_date)
                sl_price = value_end['Low']
                current_potential_pnl = value_end['High'] - start_price
                target_end_price = start_price + transaction_req_params.target
                is_long_trade = True
                if (transaction_req_params.signal == 'Short'):
                    # for short position target and sl are opposite to that of a long trade.
                    sl_price = value_end['High']
                    current_potential_pnl = start_price - value_end['Low']
                    target_end_price = start_price - transaction_req_params.target
                    is_long_trade = False
                
                
                # Check if SL hit
                is_sl_hit = False
                sl_end_price = -1
                if (is_long_trade == True):
                    is_sl_hit = (start_price - sl_price >= sl)
                    sl_end_price = start_price - sl
                else:
                    is_sl_hit = (sl_price - start_price >= sl)
                    sl_end_price = start_price + sl
                    
                if (is_sl_hit == True) :
                    end_price = sl_end_price
                    print("SL hit. Exit at: ", end_date, " Price: ", end_price)
                    buy_price, sell_price = get_buy_sell_price(start_price, end_price, is_long_trade)
                    current_pnl = (util.get_pnl(buy_price, sell_price, num_lots, lot_size) /\
                                          (lot_size * num_lots))
                    current_pnl_excluding_taxes = sell_price - buy_price
                    open_trade = False
                
                if (open_trade == True and \
                    util.get_time(end_date) > transaction_req_params.cut_off_time_to_close_date):
                    end_price = value_end['Open']
                    print("Auto squareoff. End date: ", end_date, " Price: ", end_price)
                    buy_price, sell_price = get_buy_sell_price(start_price, end_price, is_long_trade)
                    current_pnl = (util.get_pnl(buy_price, sell_price, num_lots, lot_size) /\
                                          (lot_size * num_lots))
                    current_pnl_excluding_taxes = sell_price - buy_price
                    open_trade = False
                
                if (open_trade == True and current_potential_pnl >= transaction_req_params.target):
                    print("Trade ended at: ", end_date, " Price: ", target_end_price)
                    end_price = target_end_price
                    buy_price, sell_price = get_buy_sell_price(start_price, end_price, is_long_trade)
                    current_pnl = (util.get_pnl(buy_price, sell_price, num_lots, lot_size) /\
                                          (lot_size * num_lots))
                    current_pnl_excluding_taxes = target
                    open_trade = False
                
                
                if (open_trade == False):
                    transaction_result.transaction_start_date = start_date
                    transaction_result.start_price = start_price
                    transaction_result.transaction_end_date = end_date
                    transaction_result.end_price = end_price
                    transaction_result.is_long_trade = is_long_trade
                    transaction_result.pnl = current_pnl
                    transaction_result.pnl_untaxed = current_pnl_excluding_taxes
                    done = True
                    break
        
            if (done == True):
                break
    return transaction_result
            
good_to_go_for_15_min_candle = False
# debug_date = '2021-07-09'
for date_15_min, value_fifteen_min in fifteen_minute_metadata_dict.items():
    if (value_fifteen_min['IsChild'] == True and date_15_min > last_transaction_date and \
        good_to_go_for_15_min_candle == False):
        # Enable following to debug a particular date.
        # if (util.get_date(date_15_min) != debug_date):
        #     continue;
        # We are first looking for the inside candle
        print("Test date: ", date_15_min)
        signal = value_fifteen_min['Signal']
        trigger_price = value_fifteen_min['TP']
        sl = abs(value_fifteen_min['SL'] - trigger_price)
        if (sl > 150):
            continue
        
        # sl = min(50, sl)

        # target = sl * rr_ratio
        target = 2 * value_fifteen_min['Target']

        good_to_go_for_15_min_candle = True
        continue
        
    if (good_to_go_for_15_min_candle == True):
        good_to_go_for_15_min_candle = False
        # print("Last date: ", last_transaction_date, " Current: ", date_15_min)
        transaction_req_params = transaction_request_params(signal = signal,\
                                                            trigger_price = trigger_price,\
                                                            target = target,\
                                                            sl = sl,\
                                                            start_date = date_15_min,\
                                                            cut_off_time_to_close_date = cut_off_time_to_close,\
                                                            cut_off_time_to_start_date = cut_off_time_to_start,\
                                                            current_date = util.get_date(date_15_min))
        trade_result = trade_on_one_min_chart(one_minute_ohlc_dict, transaction_req_params)
        if (trade_result.transaction_end_date == '-'):
            #print("Did not find any good trade environment for the inside candle.")
            continue
        
        
        last_transaction_date = trade_result.transaction_end_date
        print("Logging pnl: ", trade_result.pnl, " for day: ", util.get_date(last_transaction_date))
        util.add_or_update_val_to_key(pl_dict, util.get_date(last_transaction_date),\
                                      trade_result.pnl)
        dict_key = last_transaction_date.split('-')[0] + '-' + last_transaction_date.split('-')[1]
        util.add_or_update_val_to_key(pl_dict_yearly, dict_key, trade_result.pnl)
        total_pl += trade_result.pnl
        total_pnl_excluding_taxes += trade_result.pnl_untaxed
        trade_type = 'Buy'
        if (trade_result.is_long_trade == False):
            trade_type = 'Sell'
        
        row = {'Transaction':trade_type, 'StartTS':trade_result.transaction_start_date,\
               'Start Price': trade_result.start_price,\
               'EndTS':trade_result.transaction_end_date, 'End Price': trade_result.end_price,\
               'Pnl_taxed':trade_result.pnl, 'Pnl_untaxed':trade_result.pnl_untaxed}

        transactions.append(row)
    else:
        if (0):
            print("Transaction conditions not met.")
        
transaction_df = pd.DataFrame(transactions)
transaction_df.set_index('Transaction', inplace=True)

