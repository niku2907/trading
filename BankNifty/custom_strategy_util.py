#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 21:07:39 2021

@author: nishant.gupta
"""

import math
import pandas as pd
import numpy as np

from enum import Enum
from util import util

class ExitMethod(Enum):
    TARGET_BUY = 0
    SL_BUY = 1
    CUTOFF_BUY = 2
    
class custom_strategy_util:
    # SUPERTREND CALCULATION
    def get_supertrend(high, low, close, lookback, multiplier):       
        # ATR
        tr1 = pd.DataFrame(high - low)
        tr2 = pd.DataFrame(abs(high - close.shift(1)))
        tr3 = pd.DataFrame(abs(low - close.shift(1)))
        frames = [tr1, tr2, tr3]
        tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
        atr = tr.ewm(lookback).mean()
        #print("ATR: ", len(atr))
        # H/L AVG AND BASIC UPPER & LOWER BAND
        
        hl_avg = (high + low) / 2
        upper_band = (hl_avg + multiplier * atr).dropna()
        lower_band = (hl_avg - multiplier * atr).dropna()
        #print("HL_avg: ", hl_avg)
        #print("Upper band: ", upper_band)
        #print("Lower band: ", lower_band)
        # FINAL UPPER BAND
        
        final_bands = pd.DataFrame(columns = ['upper', 'lower'])
        #print("Final band: ", len(final_bands))
        final_bands.iloc[:,0] = [x for x in upper_band - upper_band]
        #print("Final band2: ", len(final_bands))
        final_bands.iloc[:,1] = final_bands.iloc[:,0]
        #print("Final band3: ", len(final_bands))
        
        for i in range(len(final_bands)):
            if i == 0:
                final_bands.iloc[i,0] = 0
            else:
                if (upper_band[i] < final_bands.iloc[i-1,0]) | (close[i-1] > final_bands.iloc[i-1,0]):
                    final_bands.iloc[i,0] = upper_band[i]
                else:
                    final_bands.iloc[i,0] = final_bands.iloc[i-1,0]
        
        #print("Final band3: ", final_bands)
        # FINAL LOWER BAND
        
        for i in range(len(final_bands)):
            if i == 0:
                final_bands.iloc[i, 1] = 0
            else:
                if (lower_band[i] > final_bands.iloc[i-1,1]) | (close[i-1] < final_bands.iloc[i-1,1]):
                    final_bands.iloc[i,1] = lower_band[i]
                else:
                    final_bands.iloc[i,1] = final_bands.iloc[i-1,1]
        
        # SUPERTREND
        #print("Final band4: ", final_bands)
        supertrend = pd.DataFrame(columns = [f'supertrend_{lookback}'])
        #print("Supertrend: ", len(supertrend))
        supertrend.iloc[:,0] = [x for x in final_bands['upper'] - final_bands['upper']]
        for i in range(len(supertrend)):
            if i == 0:
                supertrend.iloc[i, 0] = 0
            elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 0] and close[i] <= final_bands.iloc[i, 0]:
                #print("Place A.")
                supertrend.iloc[i, 0] = final_bands.iloc[i, 0]
            elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 0] and close[i] > final_bands.iloc[i, 0]:
                #print("Place B.")
                supertrend.iloc[i, 0] = final_bands.iloc[i, 1]
            elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 1] and close[i] > final_bands.iloc[i, 1]:
                #print("Place C.")
                supertrend.iloc[i, 0] = final_bands.iloc[i, 1]
            elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 1] and close[i] <= final_bands.iloc[i, 1]:
                #print("Place D.")
                supertrend.iloc[i, 0] = final_bands.iloc[i, 0]
        
        #print("Supertrend3: ", supertrend)
        supertrend = supertrend.set_index(upper_band.index)
        #print("Supertrend4: ", len(supertrend))
        # TODO(Nishant): Debug as to why do we need following line.
        #supertrend = supertrend.dropna()[1:]
        
        # ST UPTREND/DOWNTREND
        
        upt = []
        dt = []
        close = close.iloc[len(close) - len(supertrend):]
        for i in range(len(supertrend)):
            #print("Close: ", close[i], " ST: ", supertrend.iloc[i, 0])
            if close[i] > supertrend.iloc[i, 0]:
                upt.append(supertrend.iloc[i, 0])
                dt.append(np.nan)
            elif close[i] < supertrend.iloc[i, 0]:
                #print("Place2.")
                upt.append(np.nan)
                dt.append(supertrend.iloc[i, 0])
            else:
                upt.append(np.nan)
                dt.append(np.nan)
          
        st, upt, dt = pd.Series(supertrend.iloc[:, 0]), pd.Series(upt), pd.Series(dt)
        #print("ST: ", len(st))
        #print("upt: ", len(upt))
        #print("dt: ", len(dt))
        upt.index, dt.index = supertrend.index, supertrend.index
        
        return st, upt, dt
    
    # Get SELL signal
    @staticmethod
    def can_sell(prev_st, prev_price, current_st, current_price, date_time):
        time = util.get_time(date_time)
        if (time == "09:15:00" and 0):
            if (prev_st > prev_price and current_st > current_price):
                return True
            
        if (prev_st < prev_price and current_st > current_price):
            return True
        
        return False
    
    @staticmethod
    def get_pnl(buy_price, sell_price, num_units):
        message = "Profit of: " + str(sell_price - buy_price)
        if (buy_price > sell_price):
            message = "Loss of: " + str(buy_price - sell_price)
        
        custom_strategy_util.print_debug_log(message, 0)
        return custom_strategy_util.get_pnl_including_taxes(buy_price, sell_price, 1, num_units)
    
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
                                  current_capital, current_capital_list, pct_pnl_list, total_pct_pnl_list,\
                                  target_price, target_price_list):
        buy_price_list.append(pos_buy_price)
        sell_price_list.append(pos_sell_price)
        buy_time_list.append(buy_time)
        sell_time_list.append(sell_time)
        pos_type_list.append(pos_type)
        pnl_list.append(current_pnl)
        if (pos_type == "SELL"):
            pct_pnl_list.append(100 * (current_pnl / (pos_sell_price * num_units / 5)))
        else:
            pct_pnl_list.append(100 * (current_pnl / (pos_buy_price * num_units / 5)))
            
        total_pct_pnl_list.append(100 * (current_pnl / (current_capital*1000 - current_pnl)))
        exit_method_list.append(exit_method)
        num_units_list.append(num_units)
        current_capital_list.append(current_capital)
        target_price_list.append(target_price)
    
    @staticmethod
    def get_signal_based_on_macd(macd_list, macd_signal_list, date_list, current_date):
        return "SELL"
    
    @staticmethod
    def update_wins_data(pos_type, pnl, num_buy_wins, num_sell_wins):
        if (pnl > 0):
            if (pos_type == "BUY"):
                num_buy_wins += 1
            elif (pos_type == "SELL"):
                num_sell_wins += 1
        
        return num_buy_wins, num_sell_wins
            
    @staticmethod
    def update_daily_pos_exit_stats(daily_pos_exit_stats_dict, current_date, prev_date,\
                                    update_field, update_value):
        # prev_daily_val_old = ' '.join([str(elem) for i,elem in\
        #                       enumerate(daily_pos_exit_stats_dict[prev_date])])
        #print("Prev date old: " + str(prev_date) + " val: " + prev_daily_val_old)
        daily_pos_exit_stats_dict[current_date][update_field] = update_value
        daily_val = ' '.join([str(elem) for i,elem in\
                              enumerate(daily_pos_exit_stats_dict[current_date])])
        #print("Updating field: " + str(update_field) + " for date: " + str(current_date) +\
        #      " val" + daily_val)
        # prev_daily_val = ' '.join([str(elem) for i,elem in\
        #                       enumerate(daily_pos_exit_stats_dict[prev_date])])
        #print("Prev date: " + str(prev_date) + " val: " + prev_daily_val)
        
    def implement_strategy(data, buy_sl_pct, buy_dates, ema_period, sell_sl_pct, longer_tf,\
                           buy_allowed, sell_allowed, start_capital, cash_out_limit):
        prices = data['Close']
        date = data['Date']
        st = data['st']
        ema = data['EMA' + str(ema_period)]
        high_prices = data['High']
        low_prices = data['Low']
        open_prices = data['Open']
        macd = longer_tf['MACD']
        macd_signal = longer_tf['MACD_Signal']
        
        start_time = '09:15:00'
        
        # Open price of the cutoff time.
        cut_off_time_to_start = '13:50:00'
        
        # Close price of the cutoff time.
        cut_off_time_to_close = '14:45:00'
        is_open_pos = 0
        open_pos_type = 'NA'
        buy_time = ""
        sell_time = ""
        pos_buy_price = 0
        pos_sell_price = 0
        total_pnl = 0
        sl_price = 0
        target_price = 0
        decrease_sl_trigger_price = 0

        buy_time_list = []
        sell_time_list = []
        buy_price_list = []
        sell_price_list = []
        position_type_list = []
        pnl_list = []
        exit_method_list = []
        num_units_list = []
        current_capital_list = []
        pct_pnl_list = []
        target_price_list = []
        total_pct_pnl_list = []
        
        status_list = ['NA' for i in range(len(data))]
        signal_list = ['NA' for i in range(len(data))]
        
        initial_capital = start_capital
        num_units = 0
        last_trade_ctr = -1
        last_trade_date = ""
        dynamic_sl = 1
        
        num_sells = 0
        num_sell_wins = 0
        num_buys = 0
        num_buy_wins = 0
        max_sl_pct = 3.2
        reserves = 0
        
        start_date = "2023-05-01"
        start_date = ""
        #end_date = "2019-01-10"
        end_date = ""
        
        max_trades_per_day = 2
        num_trades_per_day_dict = {}
        pnl_per_day_dict = {}
        pnl_per_day_of_month_dict = {}
        num_target_buy_per_month = {}
        monthly_cash_out_stats_dict = {}
        
        high_price_daily_dict = {}
        high_price_daily_ts_dict = {}
        monthly_pnl_dict = {}
        monthly_start_capital_dict = {}
        cash_out_factor = 0.02
        monthly_target = 0.5
        
        # Each entry is a tuple of three integers.
        # 0 -> Target BUY
        # 1 -> SL BUY
        # 2 -> Cutoff BUY
        monthly_pos_exit_stats_dict = {}
        
        # This is a snapshot of monthly_pos_exit_stats_dict on a particular day
        # 0 -> Target BUY
        # 1 -> SL BUY
        # 2 -> Cutoff BUY
        # 3 -> Running ROI of the current month
        daily_pos_exit_stats_dict = {}
        date_encountered_dict = {}
        
        prev_date = ""
        prev_month = ""
        current_date = ""
        for i in range(len(data)):
            rr_ratio = 3
            
            if (initial_capital <= 0):
                break
            
            if (i < last_trade_ctr or i <= 1):
                continue
            
            current_time = util.get_time(date[i])
            current_date = util.get_date(date[i])
            current_month = util.get_month_year(date[i])
            current_time = util.get_time(date[i])
            month_year = util.get_month_year(date[i])
            last_date = util.get_date(date[i-1])
            if (last_date != current_date):
                prev_date = last_date
                
            if (prev_date != ""):
                prev_month = util.get_month_year(prev_date)
                
            if (initial_capital > cash_out_limit):
                if (monthly_cash_out_stats_dict.__contains__(month_year) == 0):
                    monthly_cash_out_stats_dict[month_year] = 0
                    
                monthly_cash_out_stats_dict[month_year] += cash_out_factor * cash_out_limit
                reserves += cash_out_factor * cash_out_limit
                initial_capital -= cash_out_factor * cash_out_limit
                #print("Cashing out: ", cash_out_factor * cash_out_limit, " on : ", util.get_date(date[i]))
            
            if (high_price_daily_dict.__contains__(util.get_date(date[i])) == 0):
                high_price_daily_dict[util.get_date(date[i])] = high_prices[i]
                high_price_daily_ts_dict[util.get_date(date[i])] = date[i]
            else:
                if (high_price_daily_dict[util.get_date(date[i])] < high_prices[i]):
                    high_price_daily_ts_dict[util.get_date(date[i])] = date[i]
                high_price_daily_dict[util.get_date(date[i])] = max(high_price_daily_dict[util.get_date(date[i])],
                                                                    high_prices[i])

            high_price_current_date = high_price_daily_dict[util.get_date(date[i])]
            high_price_current_date_ts = high_price_daily_ts_dict[util.get_date(date[i])]
            
            if ((start_date != "" and util.get_date(date[i]) < start_date) or\
                (end_date != "" and util.get_date(date[i]) > end_date)):
                continue

            if (monthly_pnl_dict.__contains__(month_year) == 0):
                monthly_pnl_dict[month_year] = 0
                
            if (monthly_start_capital_dict.__contains__(month_year) == 0):
                monthly_start_capital_dict[month_year] = initial_capital
                
            if (monthly_cash_out_stats_dict.__contains__(month_year) == 0):
                monthly_cash_out_stats_dict[month_year] = 0
                
            if ((monthly_pnl_dict[month_year] + monthly_cash_out_stats_dict[month_year]) /
                monthly_start_capital_dict[month_year] > monthly_target):
                target_achieved_for_month = 1
            else:
                target_achieved_for_month = 0
                
            if (monthly_pos_exit_stats_dict.__contains__(month_year) == 0):
                monthly_pos_exit_stats_dict[month_year] = [0, 0, 0]

            if (daily_pos_exit_stats_dict.__contains__(current_date) == 0):
                if (current_month == prev_month and\
                        daily_pos_exit_stats_dict.__contains__(prev_date) == 1):
                    daily_pos_exit_stats_dict[current_date] = \
                        daily_pos_exit_stats_dict[prev_date].copy()
                else:
                    daily_pos_exit_stats_dict[current_date] = [-1, -1, -1, -100.0]           
                    
            # Check if autosquare off needed.
            if (current_time > cut_off_time_to_close):
                if (is_open_pos == 1):
                    pos_type = "BUY"
                    exit_method = "Cutoff BUY"
                    if (open_pos_type == "BUY"):
                        pos_sell_price = open_prices[i]
                        message = "Autosquare off initiated. Sell price: " + str(pos_sell_price)
                        custom_strategy_util.print_debug_log(message, 0)
                        open_pos_type = ""
                        is_open_pos = 0
                        status_list[i] = "[Cutoff] SELL"
                        sell_time = date[i]
                        exit_method = "Cutoff SELL"
                        
                    else:
                        pos_buy_price = open_prices[i]
                        message = "Autosquare off initiated. Buy price: " + str(pos_buy_price)
                        custom_strategy_util.print_debug_log(message, 0)
                        open_pos_type = ""
                        is_open_pos = 0
                        status_list[i] = "[Cutoff] BUY"
                        buy_time = date[i]
                        pos_type = "SELL"
                        monthly_pos_exit_stats_dict[month_year][ExitMethod['CUTOFF_BUY'].value] += 1
                        custom_strategy_util.update_daily_pos_exit_stats(daily_pos_exit_stats_dict,\
                                                                         current_date,\
                                                                         prev_date,\
                                                                         ExitMethod['CUTOFF_BUY'].value,\
                                                                         monthly_pos_exit_stats_dict[month_year][ExitMethod['CUTOFF_BUY'].value])
                    
                    current_pnl = custom_strategy_util.get_pnl(pos_buy_price, pos_sell_price, num_units)
                    num_buy_wins, num_sell_wins = custom_strategy_util.update_wins_data(pos_type,\
                                                                                        current_pnl,\
                                                                                        num_buy_wins,\
                                                                                        num_sell_wins)
                    total_pnl += current_pnl
                    initial_capital += current_pnl
                    custom_strategy_util.update_transaction_record(pos_buy_price, buy_time,\
                                        pos_sell_price, sell_time,\
                                        buy_price_list, buy_time_list,\
                                        sell_price_list, sell_time_list,\
                                        pos_type, position_type_list, current_pnl, pnl_list,\
                                        exit_method, exit_method_list, num_units, num_units_list,\
                                        initial_capital/1000, current_capital_list, pct_pnl_list,\
                                        total_pct_pnl_list,\
                                        target_price, target_price_list)
                    ctr = 1
                    if (current_pnl < 0):
                        ctr = -1
                    day = util.get_day_of_month(util.get_date(sell_time))
                    if (pnl_per_day_of_month_dict.__contains__(day) == False):
                        pnl_per_day_of_month_dict[day] = [0, 0, 0, 0]
                    
                    pnl_per_day_of_month_dict[day][0] += ctr
                    if (ctr > 0):
                        pnl_per_day_of_month_dict[day][1] += ctr
                    else:
                        pnl_per_day_of_month_dict[day][2] += ctr
                    
                    pnl_per_day_of_month_dict[day][3] += current_pnl
                    
                    monthly_pnl_dict[month_year] += current_pnl
                    if ((monthly_pnl_dict[month_year] + monthly_cash_out_stats_dict[month_year]) /
                        monthly_start_capital_dict[month_year] > monthly_target):
                        target_achieved_for_month = 1
                    else:
                        target_achieved_for_month = 0
                        
                    daily_roi = 100 * (initial_capital + monthly_cash_out_stats_dict[month_year] - \
                        monthly_start_capital_dict[month_year]) / monthly_start_capital_dict[month_year]
                    custom_strategy_util.update_daily_pos_exit_stats(daily_pos_exit_stats_dict,\
                                                                     current_date,\
                                                                     prev_date, 3,\
                                                                     daily_roi)
                continue
            
            if (is_open_pos == 1):
                if (1):
                    can_close_pos = 0
                    exit_method = ""
                    
                    # Check if SL hit.
                    if (high_prices[i] >= sl_price):
                        pos_buy_price = sl_price
                        message = "[SL] Closing position. Time: " + str(date[i]) + " Buy Price: " +\
                            str(pos_buy_price) + " Sell Price: " + str(pos_sell_price)
                        custom_strategy_util.print_debug_log(message, 0)
                        can_close_pos = 1
                        status_list[i] = "[SL] BUY"
                        exit_method = "SL BUY"
                        monthly_pos_exit_stats_dict[month_year][ExitMethod['SL_BUY'].value] += 1
                        custom_strategy_util.update_daily_pos_exit_stats(daily_pos_exit_stats_dict,\
                                                                         current_date,\
                                                                         prev_date,\
                                                                         ExitMethod['SL_BUY'].value,\
                                                                         monthly_pos_exit_stats_dict[month_year][ExitMethod['SL_BUY'].value])
                    elif (low_prices[i] < target_price):
                        pos_buy_price = target_price
                        message = "[Target] Closing position. Time: " + str(date[i]) + " Buy Price: " +\
                            str(pos_buy_price) + " Sell Price: " + str(pos_sell_price)
                        custom_strategy_util.print_debug_log(message, 0)
                        can_close_pos = 1
                        status_list[i] = "[Target] BUY"
                        exit_method = "Target BUY"
                        monthly_pos_exit_stats_dict[month_year][ExitMethod['TARGET_BUY'].value] += 1
                        custom_strategy_util.update_daily_pos_exit_stats(daily_pos_exit_stats_dict,\
                                                                         current_date,\
                                                                         prev_date,\
                                                                         ExitMethod['TARGET_BUY'].value,\
                                                                         monthly_pos_exit_stats_dict[month_year][ExitMethod['TARGET_BUY'].value])
                        
                        if (num_target_buy_per_month.__contains__(month_year) == False):
                            num_target_buy_per_month[month_year] = 0
                        
                        num_target_buy_per_month[month_year] += 1
                            
                        #print("Target achieved !!: ", message)
                    elif (low_prices[i] <= decrease_sl_trigger_price and\
                          util.get_time_diff_minutes(sell_time, date[i]) > 60 and\
                          0):
                        # Decresing SL to the cost price does not give any better results and hence disabling
                        # this feature.
                        sl_price = pos_sell_price
                    if (can_close_pos == 1):
                        buy_time = date[i]
                        is_open_pos = 0
                        open_pos_type = "NA"
                        current_pnl = custom_strategy_util.get_pnl(pos_buy_price,\
                                                               pos_sell_price, num_units)
                        num_buy_wins, num_sell_wins = custom_strategy_util.update_wins_data("SELL",\
                                                                                        current_pnl,\
                                                                                        num_buy_wins,\
                                                                                        num_sell_wins)
                        total_pnl += current_pnl
                        initial_capital += current_pnl
                        custom_strategy_util.update_transaction_record(pos_buy_price, buy_time,\
                                            pos_sell_price, sell_time,\
                                            buy_price_list, buy_time_list,\
                                            sell_price_list, sell_time_list,\
                                            "SELL", position_type_list, current_pnl, pnl_list,\
                                            exit_method, exit_method_list, num_units, num_units_list,\
                                            initial_capital/1000, current_capital_list, pct_pnl_list,\
                                            total_pct_pnl_list,\
                                            target_price, target_price_list)
                        util.add_or_update_val_to_key(pnl_per_day_dict, util.get_date(date[i]),\
                                                      current_pnl)
                        ctr = 1
                        if (current_pnl < 0):
                            ctr = -1
                        day = util.get_day_of_month(util.get_date(sell_time))
                        if (pnl_per_day_of_month_dict.__contains__(day) == False):
                            pnl_per_day_of_month_dict[day] = [0, 0, 0, 0]
                        
                        pnl_per_day_of_month_dict[day][0] += ctr
                        if (ctr > 0):
                            pnl_per_day_of_month_dict[day][1] += ctr
                        else:
                            pnl_per_day_of_month_dict[day][2] += ctr
                        
                        pnl_per_day_of_month_dict[day][3] += current_pnl
                        
                        monthly_pnl_dict[month_year] += current_pnl
                        if ((monthly_pnl_dict[month_year] + monthly_cash_out_stats_dict[month_year]) /
                            monthly_start_capital_dict[month_year] > monthly_target):
                            target_achieved_for_month = 1
                        else:
                            target_achieved_for_month = 0
                            
                        daily_roi = 100 * (initial_capital + monthly_cash_out_stats_dict[month_year] - \
                            monthly_start_capital_dict[month_year]) / monthly_start_capital_dict[month_year]
                        custom_strategy_util.update_daily_pos_exit_stats(daily_pos_exit_stats_dict,\
                                                                         current_date,\
                                                                         prev_date, 3,\
                                                                         daily_roi)
                        
                continue
            
            # Check if we can open a new position.                                     
            if (current_time > cut_off_time_to_start):
                message = "Not trying to initate a new trade after cutoff time."
                custom_strategy_util.print_debug_log(message, -1)
                continue
            
            if (current_time < start_time):
                message = "Not trying to initate a new trade before start time."
                custom_strategy_util.print_debug_log(message, -1)
                continue
            
            if ((last_trade_date != "" and current_date <= last_trade_date) or\
                (num_trades_per_day_dict.__contains__(current_date) and\
                 num_trades_per_day_dict[current_date] >= max_trades_per_day)):
                continue
            
            if (custom_strategy_util.can_sell(st[i-1], prices[i-1], st[i], prices[i], date[i]) and\
                  sell_allowed):
                
                if (util.get_day_of_month(util.get_date(date[i+1])) > "31" and 0):
                    #print("Date: ", date[i+1])
                    continue
                
                if (util.get_time(date[i+1]) == "09:20:00" or 1):
                    # If diffference in opening price and the closing price of the last candle is > 1.5%
                    # skip the trade (only for gap down scenario). This is valid for all the cases and not
                    # just for the 9:20am candle.
                    prev_price = prices[i-1]
                    current_price = open_prices[i]
                    is_gap_down = False
                    if (current_price < prev_price):
                        is_gap_down = True
                        
                    if (is_gap_down == True):
                        diff_pct = ((prev_price - current_price) / prev_price) * 100
                        if (diff_pct > 1):
                            #print("Date: " + str(date[i+1]))
                            continue
                
# =============================================================================
#                 # If ST trigger candle is very big, probably avoid the trade
#                 prev_open = open_prices[i-1]
#                 prev_close = prices[i-1]
#                 prev_high = high_prices[i-1]
#                 prev_low = low_prices[i-1]
#                 if (prev_open > prev_close):
#                     diff = prev_open - prev_close
#                     diff2 = prev_high - prev_low
#                     if (((diff2 / prev_high) * 100) > 1.5):
#                         continue
# =============================================================================
                if (i+1 >= len(data) or util.get_time(date[i+1]) > cut_off_time_to_start):
                    continue
                
                if (pnl_per_day_dict.__contains__(current_date) and pnl_per_day_dict[current_date] > 0 and 0):
                    #print("Skipping the 2nd trade.")
                    continue
                
                i += 1
                sl_price_to_consider = 0
                sl_price_to_consider = max(sl_price_to_consider, high_price_current_date)
                # if (num_trades_per_day_dict.__contains__(current_date)):
                #     sl_price_to_consider = st[i-1]
                sl_price_to_consider = st[i-1]
                potential_sl =  ((math.ceil(sl_price_to_consider * 10)) / 10) - open_prices[i]
                potential_sl_pct = (potential_sl / open_prices[i]) * 100
                # if (sl_price_to_consider - open_prices[i] < 0.8 and \
                #     util.get_time_diff_minutes(high_price_current_date_ts, date[i]) > 90):
                #     print("SL: " + str(sl_price_to_consider) + " Sell Price: " + str(open_prices[i]))
                #     continue
                    
                if (potential_sl_pct > max_sl_pct):
                    continue
                    # Following does not help
                    sl_price_to_consider = st[i-1]
                    potential_sl =  ((math.ceil(sl_price_to_consider * 10)) / 10) - open_prices[i]
                    potential_sl_pct = (potential_sl / open_prices[i]) * 100
                    if (potential_sl_pct > max_sl_pct):
                        continue
                
                if (num_target_buy_per_month.__contains__(month_year) and\
                    num_target_buy_per_month[month_year] > 200 and\
                    0):
                    # Don't num target buy for the month 
                    continue

                pos_sell_price = open_prices[i]
                num_units = math.floor((5 * initial_capital) / pos_sell_price)
                if (dynamic_sl):
                    sl_pct_actual = sell_sl_pct * 5
                    max_loss = initial_capital * sl_pct_actual / 100
                    if (potential_sl == 0):
                        num_units_throttled = num_units
                    else:
                        num_units_throttled = math.floor(max_loss / potential_sl)
                    
                    num_units = min(num_units, num_units_throttled)
                    
                signal_list[i] = "SELL"
                sell_time = date[i]
                last_trade_ctr = i


                message = "Sell trade initiated at: " + str(date[i]) + " Price: " + str(pos_sell_price)
                custom_strategy_util.print_debug_log(message, 0)
                is_open_pos = 1
                open_pos_type = "SELL"
                status_list[i] = "SELL"
                sl_price = (math.ceil(sl_price_to_consider * 10)) / 10 + 0.05
                target_price = (open_prices[i] - rr_ratio * potential_sl)
                decrease_sl_trigger_price = open_prices[i] - 1.5 * (sl_price - open_prices[i])
                num_sells += 1
                util.add_or_update_val_to_key(num_trades_per_day_dict, util.get_date(date[i]), 1)
                i -= 1
                #last_trade_date = util.get_date(date[i])
        
        #reserves += initial_capital
        if (initial_capital > 100000):
            print("[Initial Capital: 100000 -> Final capital: ", math.floor(initial_capital), "]")
            print("Wealth: ", reserves)
            
        return total_pnl, num_buys, num_buy_wins, num_sells, num_sell_wins, \
            initial_capital, reserves, status_list, signal_list, position_type_list, buy_time_list,\
            buy_price_list, sell_time_list, sell_price_list, pnl_list, exit_method_list, num_units_list,\
            current_capital_list, pct_pnl_list, total_pct_pnl_list, target_price_list,\
            pnl_per_day_of_month_dict, monthly_cash_out_stats_dict, monthly_pos_exit_stats_dict,\
            daily_pos_exit_stats_dict