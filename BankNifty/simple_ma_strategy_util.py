#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 17:28:56 2021

@author: nishant.gupta
"""

import math
import numpy as np
import statsmodels.api as sm

from util import util

class simple_ma_strategy_util:
    @staticmethod
    def get_signal_based_on_ma(close_price, high_price, low_price, ma, ma_slope, allowed_diff_pct,\
                               buy_slope_threshold, sell_slope_threshold):
        close_price_ma_diff = abs(close_price - ma)
        high_price_ma_diff = abs(high_price - ma)
        low_price_ma_diff = abs(low_price - ma)
        # if (close_price_ma_diff <= allowed_diff_pct * close_price / 100 or\
        #     high_price_ma_diff <= allowed_diff_pct * high_price / 100 or\
        #     low_price_ma_diff <= allowed_diff_pct * low_price / 100):
        if (close_price_ma_diff <= allowed_diff_pct * close_price / 100):
            if (ma_slope >= buy_slope_threshold):
                return "BUY"
            elif (ma_slope <= sell_slope_threshold):
                return "CAN SELL"
                
        return "NO"
    
    @staticmethod
    def is_bullish_candle(open_price, close_price):
        return close_price > open_price
    
    @staticmethod
    def is_bearish_candle(open_price, close_price):
        return open_price > close_price
    
    def add_signal(data):
        date = data['Date']
        open_price = data['Open']
        close_price = data['Close']
        high_price = data['High']
        low_price = data['Low']
        ma = data['SMA44']
        slope = data['SMA Slope']
        
        buy_slope_threshold = 0.15
        sell_slope_threshold = -0.5
        allowed_diff_pct = 0.2
        signal_list = []
        
        for i in range(len(data)):
            if (util.get_time(date[i]) == '15:25:00'):
                signal_list.append(simple_ma_strategy_util.get_signal_based_on_ma(close_price[i],\
                                                                               high_price[i],
                                                                               low_price[i],
                                                                               ma[i],\
                                                                               slope[i],\
                                                                               allowed_diff_pct,\
                                                                               buy_slope_threshold,\
                                                                               sell_slope_threshold))  
            else:
                signal_list.append('-')
        data['Signal'] = signal_list
        
        action_list = ['NA' for i in range(len(data))]
        for i in range(len(data)):
            look_back_period = -1
            if (util.get_time(date[i]) == '09:15:00'):
                look_back_period = 1
            elif (util.get_time(date[i]) == '09:20:00'):
                look_back_period = 2

            if (i-look_back_period >= 0 and look_back_period != -1):
                if (data['Signal'][i-look_back_period] == "BUY"):
                   if (simple_ma_strategy_util.is_bullish_candle(open_price[i], close_price[i])):
                       action_list[i] = "BUY"
                elif (data['Signal'][i-look_back_period] == "SELL"):
                   if (simple_ma_strategy_util.is_bearish_candle(open_price[i], close_price[i])):
                       action_list[i] = "SELL"
                    
            
        data['Action'] = action_list
        return data
    
    @staticmethod
    def get_pnl(buy_price, sell_price, num_units):
        message = "Profit of: " + str(sell_price - buy_price)
        if (buy_price > sell_price):
            message = "Loss of: " + str(buy_price - sell_price)
        
        simple_ma_strategy_util.print_debug_log(message, 0)
        return simple_ma_strategy_util.get_pnl_including_taxes(buy_price, sell_price, 1, num_units)
    
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
        
    def implement_strategy(data, target_pct, sl_pct):
        prices = data['Close']
        date = data['Date']
        high_prices = data['High']
        low_prices = data['Low']
        open_prices = data['Open']
        
        cut_off_time_to_start = '09:20:00'
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
        for i in range(len(data)):
            #print("**********Date: ", util.get_date(data['Date'][i]), " *************")
            
            current_time = util.get_time(date[i])
            
            # Check if autosqaure off needed.
            if (current_time >= cut_off_time_to_close):
                if (is_open_pos == 1):
                    pos_type = "BUY"
                    exit_method = "Cutoff BUY"
                    if (open_pos_type == "BUY"):
                        pos_sell_price = prices[i]
                        message = "Autosquare off initiated. Sell price: " + str(pos_sell_price)
                        simple_ma_strategy_util.print_debug_log(message, 0)
                        open_pos_type = ""
                        is_open_pos = 0
                        status_list[i] = "[Cutoff] SELL"
                        sell_time = date[i]
                        exit_method = "Cutoff SELL"
                    else:
                        pos_buy_price = prices[i]
                        message = "Autosquare off initiated. Buy price: " + str(pos_buy_price)
                        simple_ma_strategy_util.print_debug_log(message, 0)
                        open_pos_type = ""
                        is_open_pos = 0
                        status_list[i] = "[Cutoff] BUY"
                        buy_time = date[i]
                        pos_type = "SELL"
                    
                    current_pnl = simple_ma_strategy_util.get_pnl(pos_buy_price, pos_sell_price, num_units)
                    total_pnl += current_pnl
                    initial_capital += current_pnl
                    simple_ma_strategy_util.update_transaction_record(pos_buy_price, buy_time,\
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
                        simple_ma_strategy_util.print_debug_log(message, 0)
                        can_close_pos = 1
                        status_list[i] = "[SL] SELL"
                        exit_method = "SL SELL"
                    # Check if target achieved.
                    elif (high_prices[i] >= target_price):
                        pos_sell_price = target_price
                        message = "[Target] Closing position. Time: " + str(date[i]) + " Buy Price: " +\
                            str(pos_buy_price) + " Sell Price: " + str(pos_sell_price)
                        simple_ma_strategy_util.print_debug_log(message, 0)
                        can_close_pos = 1
                        status_list[i] = "[Target] SELL"
                        exit_method = "Target SELL"

                    if (can_close_pos == 1):
                        sell_time = date[i]
                        is_open_pos = 0
                        open_pos_type = "NA"
                        current_pnl = simple_ma_strategy_util.get_pnl(pos_buy_price,\
                                                               pos_sell_price, num_units)
                        total_pnl += current_pnl
                        initial_capital += current_pnl
                        simple_ma_strategy_util.update_transaction_record(pos_buy_price, buy_time,\
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
                        simple_ma_strategy_util.print_debug_log(message, 0)
                        can_close_pos = 1
                        status_list[i] = "[SL] BUY"
                        exit_method = "SL BUY"
                    elif (low_prices[i] <= target_price):
                        pos_buy_price = target_price
                        message = "[Target] Closing position. Time: " + str(date[i]) + " Buy Price: " +\
                            str(pos_buy_price) + " Sell Price: " + str(pos_sell_price)
                        simple_ma_strategy_util.print_debug_log(message, 0)
                        can_close_pos = 1
                        status_list[i] = "[Target] BUY"
                        exit_method = "Target BUY"
                        
                    if (can_close_pos == 1):
                        buy_time = date[i]
                        is_open_pos = 0
                        open_pos_type = "NA"
                        current_pnl = simple_ma_strategy_util.get_pnl(pos_buy_price,\
                                                               pos_sell_price, num_units)
                        total_pnl += current_pnl
                        initial_capital += current_pnl
                        simple_ma_strategy_util.update_transaction_record(pos_buy_price, buy_time,\
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
                simple_ma_strategy_util.print_debug_log(message, -1)
                continue
            
            if (data['Action'][i] == "BUY"):
                #target_price = prices[i] * (1 + target_pct / 100)
                buy_time = date[i]
                
                # Ideally sell price should be opening price of the next candle.
                pos_buy_price = prices[i]
                num_units = math.floor((5 * initial_capital) / pos_buy_price)
                message = "Buy trade initiated at: " + str(date[i]) + " Price: " + str(pos_buy_price)
                simple_ma_strategy_util.print_debug_log(message, 0)
                is_open_pos = 1
                open_pos_type = "BUY"
                status_list[i] = "BUY"
                #sl_price = prices[i] * (1 - sl_pct / 100)
                sl_price = low_prices[i]
                target_price = 1.5 * (prices[i] - sl_price) + prices[i]
                message = "Target: " + str(target_price) + " SL: " + str(sl_price)
                simple_ma_strategy_util.print_debug_log(message, 0)
            elif (data['Action'][i] == "SELL"):
                target_price = prices[i] * (1 - target_pct / 100)
                sell_time = date[i]
                
                # Ideally sell price should be opening price of the next candle.
                pos_sell_price = prices[i]
                num_units = math.floor((5 * initial_capital) / pos_sell_price)
                message = "Sell trade initiated at: " + str(date[i]) + " Price: " + str(pos_sell_price)
                simple_ma_strategy_util.print_debug_log(message, 0)
                is_open_pos = 1
                open_pos_type = "SELL"
                status_list[i] = "SELL"
                sl_price = prices[i] * (1 + sl_pct / 100)
                message = "Target: " + str(target_price) + " SL: " + str(sl_price)
                simple_ma_strategy_util.print_debug_log(message, 0)
                
        print("[Initial Capital: 100000 -> Final capital: ", math.floor(initial_capital), "]")
        return total_pnl, initial_capital, status_list, signal_list, position_type_list, buy_time_list,\
            buy_price_list, sell_time_list, sell_price_list, pnl_list, exit_method_list, num_units_list,\
            current_capital_list