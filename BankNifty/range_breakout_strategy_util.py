#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 13:34:25 2021

@author: nishant.gupta
"""

import math
import numpy as np

from util import util

class range_breakout_strategy_util:
    @staticmethod
    def is_bullish_candle(open_price, close_price):
        return close_price > open_price
    
    @staticmethod
    def is_bearish_candle(open_price, close_price):
        return open_price > close_price
    
    @staticmethod
    def get_pnl(buy_price, sell_price, num_units):
        message = "Profit of: " + str(sell_price - buy_price)
        if (buy_price > sell_price):
            message = "Loss of: " + str(buy_price - sell_price)
        
        range_breakout_strategy_util.print_debug_log(message, 0)
        return range_breakout_strategy_util.get_pnl_including_taxes(buy_price, sell_price, 1, num_units)
    
    @staticmethod
    def print_debug_log(message, level):
        if (level > 0):
            print("[DEBUG] ", message)
        
    @staticmethod
    def get_pnl_including_taxes(buy_price, sell_price, num_lots, lot_size):
        brokerage = 40
        transaction_charges = (.00345/100) * (buy_price + sell_price) * num_lots * lot_size
        stt = (.025/100) * sell_price * num_lots * lot_size
        stamp_duty = (.003/100) * buy_price * num_lots * lot_size
        sebi_charges = (10/100) * stamp_duty
        gst = (18/100) * (brokerage + transaction_charges)
        total_charges = brokerage + transaction_charges + stt + stamp_duty + sebi_charges + gst
        pnl = (sell_price - buy_price) * num_lots * lot_size - total_charges
        return pnl
    
    @staticmethod
    def update_transaction_record(pos_buy_price, buy_time, pos_sell_price, sell_time,\
                                  buy_price_list, buy_time_list, sell_price_list, sell_time_list,\
                                  pos_type, pos_type_list, current_pnl, pnl_list,\
                                  exit_method, exit_method_list, num_units, num_units_list,\
                                  current_capital, current_capital_list):
        buy_price_list.append(pos_buy_price)
        sell_price_list.append(pos_sell_price)
        buy_time_list.append(buy_time)
        sell_time_list.append(sell_time)
        pos_type_list.append(pos_type)
        pnl_list.append(current_pnl)
        exit_method_list.append(exit_method)
        num_units_list.append(num_units)
        current_capital_list.append(current_capital)
        
    def implement_strategy(data, target_pct, sl_pct, buy_dates, sell_dates):
        prices = data['Close']
        date = data['Date']
        high_prices = data['High']
        low_prices = data['Low']
        open_prices = data['Open']
        
        cut_off_time_to_start = '14:30:00'
        cut_off_time_to_close = '15:15:00'
        is_open_pos = 0
        open_pos_type = 'NA'
        buy_time = ""
        sell_time = ""
        pos_buy_price = 0
        pos_sell_price = 0
        total_pnl = 0
        sl_price = 0
        target_price = 0

        buy_time_list = []
        sell_time_list = []
        buy_price_list = []
        sell_price_list = []
        position_type_list = []
        pnl_list = []
        exit_method_list = []
        num_units_list = []
        current_capital_list = []
        
        status_list = ['NA' for i in range(len(data))]
        signal_list = ['NA' for i in range(len(data))]
        
        initial_capital = 100000
        num_units = 0
        last_trade_ctr = -1
        last_trade_date = ""
        dynamic_sl = 1
        
        for i in range(len(data)):
            #print("**********Date: ", util.get_date(data['Date'][i]), " *************")
            
            if (i <= last_trade_ctr):
                continue
            
            current_time = util.get_time(date[i])
            
            # Check if autosqaure off needed.
            if (current_time >= cut_off_time_to_close):
                if (is_open_pos == 1):
                    pos_type = "BUY"
                    exit_method = "Cutoff BUY"
                    if (open_pos_type == "BUY"):
                        pos_sell_price = prices[i]
                        message = "Autosquare off initiated. Sell price: " + str(pos_sell_price)
                        range_breakout_strategy_util.print_debug_log(message, 0)
                        open_pos_type = ""
                        is_open_pos = 0
                        status_list[i] = "[Cutoff] SELL"
                        sell_time = date[i]
                        exit_method = "Cutoff SELL"
                    else:
                        pos_buy_price = prices[i]
                        message = "Autosquare off initiated. Buy price: " + str(pos_buy_price)
                        range_breakout_strategy_util.print_debug_log(message, 0)
                        open_pos_type = ""
                        is_open_pos = 0
                        status_list[i] = "[Cutoff] BUY"
                        buy_time = date[i]
                        pos_type = "SELL"
                    
                    current_pnl = range_breakout_strategy_util.get_pnl(pos_buy_price, pos_sell_price, num_units)
                    total_pnl += current_pnl
                    initial_capital += current_pnl
                    range_breakout_strategy_util.update_transaction_record(pos_buy_price, buy_time,\
                                        pos_sell_price, sell_time,\
                                        buy_price_list, buy_time_list,\
                                        sell_price_list, sell_time_list,\
                                        pos_type, position_type_list, current_pnl, pnl_list,\
                                        exit_method, exit_method_list, num_units, num_units_list,\
                                        initial_capital/1000, current_capital_list)
                continue
            
            if (is_open_pos == 1):
                if (open_pos_type == "BUY"):
                    can_close_pos = 0
                    exit_method = ""
                    # Check if SL hit.
                    if (low_prices[i] <= sl_price):
                        pos_sell_price = sl_price
                        message = "[SL] Closing position. Time: " + str(date[i]) + " Buy Price: " +\
                            str(pos_buy_price) + " Sell Price: " + str(pos_sell_price)
                        range_breakout_strategy_util.print_debug_log(message, 0)
                        can_close_pos = 1
                        status_list[i] = "[SL] SELL"
                        exit_method = "SL SELL"
                    # Check if target achieved.
                    elif (high_prices[i] >= target_price):
                        pos_sell_price = target_price
                        message = "[Target] Closing position. Time: " + str(date[i]) + " Buy Price: " +\
                            str(pos_buy_price) + " Sell Price: " + str(pos_sell_price)
                        range_breakout_strategy_util.print_debug_log(message, 0)
                        can_close_pos = 1
                        status_list[i] = "[Target] SELL"
                        exit_method = "Target SELL"

                    if (can_close_pos == 1):
                        sell_time = date[i]
                        is_open_pos = 0
                        open_pos_type = "NA"
                        current_pnl = range_breakout_strategy_util.get_pnl(pos_buy_price,\
                                                               pos_sell_price, num_units)
                        total_pnl += current_pnl
                        initial_capital += current_pnl
                        range_breakout_strategy_util.update_transaction_record(pos_buy_price, buy_time,\
                                            pos_sell_price, sell_time,\
                                            buy_price_list, buy_time_list,\
                                            sell_price_list, sell_time_list,\
                                            "BUY", position_type_list, current_pnl, pnl_list,\
                                            exit_method, exit_method_list, num_units, num_units_list,\
                                            initial_capital /1000, current_capital_list)
                elif (open_pos_type == "SELL"):
                    can_close_pos = 0
                    exit_method = ""
                    # Check if SL hit.
                    if (high_prices[i] >= sl_price):
                        pos_buy_price = sl_price
                        message = "[SL] Closing position. Time: " + str(date[i]) + " Buy Price: " +\
                            str(pos_buy_price) + " Sell Price: " + str(pos_sell_price)
                        range_breakout_strategy_util.print_debug_log(message, 0)
                        can_close_pos = 1
                        status_list[i] = "[SL] BUY"
                        exit_method = "SL BUY"
                    elif (low_prices[i] <= target_price):
                        pos_buy_price = target_price
                        message = "[Target] Closing position. Time: " + str(date[i]) + " Buy Price: " +\
                            str(pos_buy_price) + " Sell Price: " + str(pos_sell_price)
                        range_breakout_strategy_util.print_debug_log(message, 0)
                        can_close_pos = 1
                        status_list[i] = "[Target] BUY"
                        exit_method = "Target BUY"
                        
                    if (can_close_pos == 1):
                        buy_time = date[i]
                        is_open_pos = 0
                        open_pos_type = "NA"
                        current_pnl = range_breakout_strategy_util.get_pnl(pos_buy_price,\
                                                               pos_sell_price, num_units)
                        total_pnl += current_pnl
                        initial_capital += current_pnl
                        range_breakout_strategy_util.update_transaction_record(pos_buy_price, buy_time,\
                                            pos_sell_price, sell_time,\
                                            buy_price_list, buy_time_list,\
                                            sell_price_list, sell_time_list,\
                                            "SELL", position_type_list, current_pnl, pnl_list,\
                                            exit_method, exit_method_list, num_units, num_units_list,\
                                            initial_capital/1000, current_capital_list)
                continue
            
            # Check if we can open a new position.                                     
            if (current_time > cut_off_time_to_start):
                message = "Not trying to initate a new trade after cutoff time."
                range_breakout_strategy_util.print_debug_log(message, -1)
                continue
            
            current_date = util.get_date(date[i])
            if (last_trade_date != "" and current_date <= last_trade_date):
                continue
            
            if (buy_dates.__contains__(util.get_date(data['Date'][i]))):
                trigger_price = buy_dates[util.get_date(data['Date'][i])]
                if (i+3 >= len(data) or util.get_time(date[i+3]) > cut_off_time_to_start):
                    continue
                
                if (prices[i] >= trigger_price):
                    if (low_prices[i+1] > low_prices[i] and\
                        low_prices[i+2] > low_prices[i]):
                        i += 3
                        # sl_price = open_prices[i] * (1 - sl_pct / 100)
                        # if (sl_price > low_prices[i-3]):
                        #     last_trade_ctr = i
                        #     continue
                        
                        last_trade_ctr = i
                        num_units = math.floor((5 * initial_capital) / open_prices[i])
                        if (dynamic_sl):
                            sl_pct_actual = sl_pct * 5
                            max_loss = initial_capital * sl_pct_actual / 100
                            potential_loss_per_unit = open_prices[i] - low_prices[i-3]
                            if (potential_loss_per_unit == 0):
                                num_units_throttled = num_units
                            else:
                                num_units_throttled = math.floor(max_loss / potential_loss_per_unit)
                                
                            num_units = min(num_units, num_units_throttled)
                        
                        if (num_units <= 0):
                            continue
                        pos_buy_price = open_prices[i]
                        buy_time = date[i]
                        message = "Buy trade initiated at: " + str(date[i]) + " Price: " +\
                            str(pos_buy_price)
                        range_breakout_strategy_util.print_debug_log(message, 0)
                        is_open_pos = 1
                        open_pos_type = "BUY"
                        status_list[i] = "BUY"
                        sl_price = low_prices[i-3]
                        target_price = 2 * (prices[i] - sl_price) + prices[i]
                        message = "Target: " + str(target_price) + " SL: " + str(sl_price)
                        range_breakout_strategy_util.print_debug_log(message, 0)
            elif (sell_dates.__contains__(util.get_date(data['Date'][i]))):
                trigger_price = sell_dates[util.get_date(data['Date'][i])]
                if (i+2 >= len(data) or util.get_time(date[i+2]) > cut_off_time_to_start):
                    continue
                
                if (prices[i] <= trigger_price):
                    if (high_prices[i+1] < high_prices[i] and low_prices[i+1] < low_prices[i]):
                        i += 2
                        # sl_price = open_prices[i] * (1 - sl_pct / 100)
                        # if (sl_price > low_prices[i-3]):
                        #     last_trade_ctr = i
                        #     continue
                        
                        last_trade_ctr = i
                        num_units = math.floor((5 * initial_capital) / open_prices[i])
                        if (dynamic_sl):
                            sl_pct_actual = sl_pct * 5
                            max_loss = initial_capital * sl_pct_actual / 100
                            potential_loss_per_unit = high_prices[i-2] - open_prices[i]
                            if (potential_loss_per_unit == 0):
                                num_units_throttled = num_units
                            else:
                                num_units_throttled = math.floor(max_loss / potential_loss_per_unit)
                                
                            num_units = min(num_units, num_units_throttled)
                        
                        if (num_units <= 0):
                            continue
                        last_trade_date = util.get_date(date[i])
                        pos_sell_price = open_prices[i]
                        sell_time = date[i]
                        message = "Sell trade initiated at: " + str(date[i]) + " Price: " +\
                            str(pos_sell_price)
                        range_breakout_strategy_util.print_debug_log(message, 0)
                        is_open_pos = 1
                        open_pos_type = "SELL"
                        status_list[i] = "SELL"
                        sl_price = high_prices[i-2]
                        target_price =  prices[i] - 1.5 * (sl_price - prices[i])
                        message = "Target: " + str(target_price) + " SL: " + str(sl_price)
                        range_breakout_strategy_util.print_debug_log(message, 0)
                
        print("[Initial Capital: 100000 -> Final capital: ", math.floor(initial_capital), "]")
        return total_pnl, initial_capital, status_list, signal_list, position_type_list, buy_time_list,\
            buy_price_list, sell_time_list, sell_price_list, pnl_list, exit_method_list, num_units_list,\
            current_capital_list