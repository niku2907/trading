# -*- coding: utf-8 -*-
"""
Created on Fri May 26 15:44:53 2023

@author: NishantGupta
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

class ExitMethodForBuy(Enum):
    TARGET_SELL = 0
    SL_SELL = 1
    CUTOFF_SELL = 2
    
class CandleMetadata:
    def __init__(self, time, open_price, high_price, low_price, close_price):
        self.time = time
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
    
class traffic_light_strategy_util:
    @staticmethod
    def get_pnl(buy_price, sell_price, num_units):
        message = "Profit of: " + str(sell_price - buy_price) + " per unit"
        if (buy_price > sell_price):
            message = "Loss of: " + str(buy_price - sell_price) + " per unit"
        
        traffic_light_strategy_util.print_debug_log(message, 1)
        return traffic_light_strategy_util.get_pnl_including_taxes(buy_price, sell_price, 1, num_units)
    
    @staticmethod
    def print_debug_log(message, level):
        if (level > 1):
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
                                  target_price, target_price_list,\
                                  price_per_lot, lot_size):
        buy_price_list.append(pos_buy_price)
        sell_price_list.append(pos_sell_price)
        buy_time_list.append(buy_time)
        sell_time_list.append(sell_time)
        pos_type_list.append(pos_type)
        pnl_list.append(current_pnl)
        num_lots = num_units / lot_size
        if num_lots == 0:
            print("Num units: " + str(num_units) + " lot size: " + str(lot_size))
        if price_per_lot != -1:
            pct_pnl_list.append(100 * (current_pnl / (price_per_lot * num_lots)))
        else:
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

    def implement_strategy(data, buy_sl_pct, ema_period, sell_sl_pct, \
                               buy_allowed, sell_allowed, start_capital, cash_out_limit,\
                               start_execution_error_pct,\
                               sl_buffer_pct,\
                               price_per_lot, lot_size):
        prices = data['Close']
        date = data['Date']
        ema = data['EMA' + str(ema_period)]
        high_prices = data['High']
        low_prices = data['Low']
        open_prices = data['Open']
        
        start_time = '09:15:00'
        
        # Open price of the cutoff time.
        cut_off_time_to_start = '14:30:00'
        
        # Close price of the cutoff time.
        cut_off_time_to_close = '16:00:00'
        is_open_pos_buy = 0
        is_open_pos_sell = 0
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
        alert_candle_encountered = 0
        start_limit_price_based_on_alert_candle = -1
        sl_price_based_on_alert_candle = -1
        
        num_sells = 0
        num_sell_wins = 0
        num_buys = 0
        num_buy_wins = 0
        max_sl_pct = 3.2
        reserves = 0
        sl_points = 0
        target_points = 0
        distance_from_ema = 0
        
        start_date = "2022-06-03"
        start_date = ""
        end_date = "2022-06-04"
        end_date = ""
        
        max_trades_per_day = 3
        num_trades_per_day_dict = {}
        pnl_per_day_dict = {}
        pnl_per_day_of_month_dict = {}
        num_target_sell_per_month = {}
        monthly_cash_out_stats_dict = {}
        
        high_price_daily_dict = {}
        high_price_daily_ts_dict = {}
        monthly_pnl_dict = {}
        monthly_start_capital_dict = {}
        cash_out_factor = 0.02
        monthly_target = 0.5
        
        max_buy_sl = 100
        max_sell_sl = 100
        
        # Each entry is a tuple of three integers.
        # 0 -> Target BUY
        # 1 -> SL BUY
        # 2 -> Cutoff BUY
        monthly_pos_exit_stats_dict_sell = {}
        
        # Each entry is a tuple of three integers.
        # 0 -> Target SELL
        # 1 -> SL SELL
        # 2 -> Cutoff SELL
        monthly_pos_exit_stats_dict_buy = {}
        
        # This is a snapshot of monthly_pos_exit_stats_dict on a particular day
        # 0 -> Target SELL
        # 1 -> SL SELL
        # 2 -> Cutoff SELL
        # 3 -> Running ROI of the current month
        daily_pos_exit_stats_dict_buy = {}
        
        # This is a snapshot of monthly_pos_exit_stats_dict on a particular day
        # 0 -> Target 
        # 1 -> SL BUY
        # 2 -> Cutoff BUY
        # 3 -> Running ROI of the current month
        daily_pos_exit_stats_dict_sell = {}
        
        date_encountered_dict = {}
        
        prev_date = ""
        prev_month = ""
        current_date = ""
        
        red_candle = CandleMetadata("-", -1, -1, -1, -1)
        green_candle = CandleMetadata("-", -1, -1, -1, -1)
        red_candle_encountered = 0
        green_candle_encountered = 0
        for i in range(len(data)):
            rr_ratio = 4
            
            current_time = util.get_time(date[i])
            current_date = util.get_date(date[i])
            current_month = util.get_month_year(date[i])
            current_time = util.get_time(date[i])
            month_year = util.get_month_year(date[i])
            
            # Initialize
            if (monthly_pnl_dict.__contains__(month_year) == 0):
                monthly_pnl_dict[month_year] = 0
                
            if (monthly_start_capital_dict.__contains__(month_year) == 0):
                monthly_start_capital_dict[month_year] = initial_capital
                
            if (monthly_cash_out_stats_dict.__contains__(month_year) == 0):
                monthly_cash_out_stats_dict[month_year] = 0

            
            if (monthly_pos_exit_stats_dict_buy.__contains__(month_year) == 0):
                monthly_pos_exit_stats_dict_buy[month_year] = [0, 0, 0]
                
            if (monthly_pos_exit_stats_dict_sell.__contains__(month_year) == 0):
                monthly_pos_exit_stats_dict_sell[month_year] = [0, 0, 0]

            if (daily_pos_exit_stats_dict_buy.__contains__(current_date) == 0):
                if (current_month == prev_month and\
                        daily_pos_exit_stats_dict_buy.__contains__(prev_date) == 1):
                    daily_pos_exit_stats_dict_buy[current_date] = \
                        daily_pos_exit_stats_dict_buy[prev_date].copy()
                else:
                    daily_pos_exit_stats_dict_buy[current_date] = [-1, -1, -1, -100.0]  
                    
            if (daily_pos_exit_stats_dict_sell.__contains__(current_date) == 0):
                if (current_month == prev_month and\
                        daily_pos_exit_stats_dict_sell.__contains__(prev_date) == 1):
                    daily_pos_exit_stats_dict_sell[current_date] = \
                        daily_pos_exit_stats_dict_sell[prev_date].copy()
                else:
                    daily_pos_exit_stats_dict_sell[current_date] = [-1, -1, -1, -100.0]
                    
            # Early return
            if (initial_capital <= 0):
                break
            
            if (i < last_trade_ctr or i <= 1):
                continue
            
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
            
            # if ((monthly_pnl_dict[month_year] + monthly_cash_out_stats_dict[month_year]) /
            #     monthly_start_capital_dict[month_year] > monthly_target):
            #     target_achieved_for_month = 1
            # else:
            #     target_achieved_for_month = 0
                
                    
            # Check if autosquare off needed.
            if (current_time > cut_off_time_to_close):
                alert_candle_encountered = 0
                red_candle_encountered = 0
                green_candle_encountered = 0
                high_limit_price_based_on_alert_candle = -1
                low_limit_price_based_on_alert_candle = -1
                sl_price_based_on_alert_candle_for_long = -1
                sl_price_based_on_alert_candle_for_short = -1
                red_candle = CandleMetadata("-", -1, -1, -1, -1)
                green_candle = CandleMetadata("-", -1, -1, -1, -1)
                if (is_open_pos_buy == 1):
                    pos_type = "BUY"
                    pos_sell_price = open_prices[i]
                    message = "Autosquare off initiated. Sell price: " + str(pos_sell_price)
                    traffic_light_strategy_util.print_debug_log(message, 0)
                    open_pos_type = ""
                    is_open_pos_buy = 0
                    status_list[i] = "[Cutoff] SELL"
                    sell_time = date[i]
                    exit_method = "Cutoff SELL"
                    monthly_pos_exit_stats_dict_buy[month_year][ExitMethodForBuy['CUTOFF_SELL'].value] += 1
                    traffic_light_strategy_util.update_daily_pos_exit_stats(daily_pos_exit_stats_dict_buy,\
                                                                     current_date,\
                                                                     prev_date,\
                                                                     ExitMethodForBuy['CUTOFF_SELL'].value,\
                                                                     monthly_pos_exit_stats_dict_buy[month_year][ExitMethodForBuy['CUTOFF_SELL'].value])                    
                    
                    current_pnl = traffic_light_strategy_util.get_pnl(pos_buy_price, pos_sell_price, num_units)
                    num_buy_wins, num_sell_wins = traffic_light_strategy_util.update_wins_data(pos_type,\
                                                                                        current_pnl,\
                                                                                        num_buy_wins,\
                                                                                        num_sell_wins)
                    total_pnl += current_pnl
                    initial_capital += current_pnl
                    traffic_light_strategy_util.update_transaction_record(pos_buy_price, buy_time,\
                                        pos_sell_price, sell_time,\
                                        buy_price_list, buy_time_list,\
                                        sell_price_list, sell_time_list,\
                                        pos_type, position_type_list, current_pnl, pnl_list,\
                                        exit_method, exit_method_list, num_units, num_units_list,\
                                        initial_capital/1000, current_capital_list, pct_pnl_list,\
                                        total_pct_pnl_list,\
                                        target_price, target_price_list,\
                                        price_per_lot, lot_size)
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
                    traffic_light_strategy_util.update_daily_pos_exit_stats(daily_pos_exit_stats_dict_buy,\
                                                                  current_date,\
                                                                  prev_date, 3,\
                                                                  daily_roi)
                elif is_open_pos_sell == 1 :
                    pos_type = "SELL"
                    pos_buy_price = open_prices[i]
                    message = "Autosquare off initiated. Buy price: " + str(pos_buy_price)
                    traffic_light_strategy_util.print_debug_log(message, 0)
                    open_pos_type = ""
                    is_open_pos_sell = 0
                    status_list[i] = "[Cutoff] BUY"
                    sell_time = date[i]
                    exit_method = "Cutoff BUY"
                    monthly_pos_exit_stats_dict_sell[month_year][ExitMethod['CUTOFF_BUY'].value] += 1
                    traffic_light_strategy_util.update_daily_pos_exit_stats(daily_pos_exit_stats_dict_sell,\
                                                                     current_date,\
                                                                     prev_date,\
                                                                     ExitMethod['CUTOFF_BUY'].value,\
                                                                     monthly_pos_exit_stats_dict_sell[month_year][ExitMethod['CUTOFF_BUY'].value])                    
                    
                    current_pnl = traffic_light_strategy_util.get_pnl(pos_buy_price, pos_sell_price, num_units)
                    num_buy_wins, num_sell_wins = traffic_light_strategy_util.update_wins_data(pos_type,\
                                                                                        current_pnl,\
                                                                                        num_buy_wins,\
                                                                                        num_sell_wins)
                    total_pnl += current_pnl
                    initial_capital += current_pnl
                    traffic_light_strategy_util.update_transaction_record(pos_buy_price, buy_time,\
                                        pos_sell_price, sell_time,\
                                        buy_price_list, buy_time_list,\
                                        sell_price_list, sell_time_list,\
                                        pos_type, position_type_list, current_pnl, pnl_list,\
                                        exit_method, exit_method_list, num_units, num_units_list,\
                                        initial_capital/1000, current_capital_list, pct_pnl_list,\
                                        total_pct_pnl_list,\
                                        target_price, target_price_list,\
                                        price_per_lot, lot_size)
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
                    traffic_light_strategy_util.update_daily_pos_exit_stats(daily_pos_exit_stats_dict_sell,\
                                                                  current_date,\
                                                                  prev_date, 3,\
                                                                  daily_roi) 
                continue
            
            if (is_open_pos_buy == 1):
                can_close_pos = 0
                exit_method = ""
                
                # Check if SL hit.
                if (low_prices[i] <= sl_price):
                    pos_sell_price = sl_price
                    pos_sell_price = min(open_prices[i], sl_price)
                    message = "[SL] Closing position. Time: " + str(date[i]) + " Sell Price: " +\
                        str(pos_sell_price) + " Buy Price: " + str(pos_buy_price)
                    traffic_light_strategy_util.print_debug_log(message, 1)
                    can_close_pos = 1
                    status_list[i] = "[SL] SELL"
                    exit_method = "SL SELL"
                    monthly_pos_exit_stats_dict_buy[month_year][ExitMethodForBuy['SL_SELL'].value] += 1
                    traffic_light_strategy_util.update_daily_pos_exit_stats(daily_pos_exit_stats_dict_buy,\
                                                                  current_date,\
                                                                  prev_date,\
                                                                  ExitMethodForBuy['SL_SELL'].value,\
                                                                  monthly_pos_exit_stats_dict_buy[month_year][ExitMethodForBuy['SL_SELL'].value])
                elif (high_prices[i] > target_price):
                    pos_sell_price = target_price
                    message = "[Target] Closing position. Time: " + str(date[i]) + " Sell Price: " +\
                        str(pos_sell_price) + " Buy Price: " + str(pos_buy_price)
                    traffic_light_strategy_util.print_debug_log(message, 1)
                    can_close_pos = 1
                    status_list[i] = "[Target] SELL"
                    exit_method = "Target SELL"
                    monthly_pos_exit_stats_dict_buy[month_year][ExitMethodForBuy['TARGET_SELL'].value] += 1
                    traffic_light_strategy_util.update_daily_pos_exit_stats(daily_pos_exit_stats_dict_buy,\
                                                                  current_date,\
                                                                  prev_date,\
                                                                  ExitMethodForBuy['TARGET_SELL'].value,\
                                                                  monthly_pos_exit_stats_dict_buy[month_year][ExitMethodForBuy['TARGET_SELL'].value])
                    
                    if (num_target_sell_per_month.__contains__(month_year) == False):
                        num_target_sell_per_month[month_year] = 0
                    
                    num_target_sell_per_month[month_year] += 1
                        
                    #print("Target achieved !!: ", message)
                elif (high_prices[i] >= decrease_sl_trigger_price and\
                      util.get_time_diff_minutes(date[i], buy_time) > 60 and\
                      0):
                    # Decresing SL to the cost price does not give any better results and hence disabling
                    # this feature.
                    sl_price = pos_buy_price
                if (can_close_pos == 1):
                    sell_time = date[i]
                    is_open_pos_buy = 0
                    is_open_pos_sell = 0
                    open_pos_type = "NA"
                    alert_candle_encountered = 0
                    red_candle_encountered = 0
                    green_candle_encountered = 0
                    high_limit_price_based_on_alert_candle = -1
                    low_limit_price_based_on_alert_candle = -1
                    sl_price_based_on_alert_candle_for_long = -1
                    sl_price_based_on_alert_candle_for_short = -1
                    red_candle = CandleMetadata("-", -1, -1, -1, -1)
                    green_candle = CandleMetadata("-", -1, -1, -1, -1)
                    current_pnl = traffic_light_strategy_util.get_pnl(pos_buy_price,\
                                                           pos_sell_price, num_units)
                    num_buy_wins, num_sell_wins = traffic_light_strategy_util.update_wins_data("BUY",\
                                                                                    current_pnl,\
                                                                                    num_buy_wins,\
                                                                                    num_sell_wins)
                    total_pnl += current_pnl
                    initial_capital += current_pnl
                    traffic_light_strategy_util.update_transaction_record(pos_buy_price, buy_time,\
                                        pos_sell_price, sell_time,\
                                        buy_price_list, buy_time_list,\
                                        sell_price_list, sell_time_list,\
                                        "BUY", position_type_list, current_pnl, pnl_list,\
                                        exit_method, exit_method_list, num_units, num_units_list,\
                                        initial_capital/1000, current_capital_list, pct_pnl_list,\
                                        total_pct_pnl_list,\
                                        target_price, target_price_list,\
                                        price_per_lot, lot_size)
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
                    traffic_light_strategy_util.update_daily_pos_exit_stats(daily_pos_exit_stats_dict_buy,\
                                                                  current_date,\
                                                                  prev_date, 3,\
                                                                  daily_roi)
                        
                continue
            elif is_open_pos_sell == 1:
                can_close_pos = 0
                exit_method = ""
                
                # Check if SL hit.
                if (high_prices[i] >= sl_price):
                    pos_buy_price = sl_price
                    pos_buy_price = max(open_prices[i], sl_price)
                    message = "[SL] Closing position. Time: " + str(date[i]) + " Sell Price: " +\
                        str(pos_sell_price) + " Buy Price: " + str(pos_buy_price)
                    traffic_light_strategy_util.print_debug_log(message, 1)
                    can_close_pos = 1
                    status_list[i] = "[SL] BUY"
                    exit_method = "SL BUY"
                    monthly_pos_exit_stats_dict_sell[month_year][ExitMethod['SL_BUY'].value] += 1
                    traffic_light_strategy_util.update_daily_pos_exit_stats(daily_pos_exit_stats_dict_sell,\
                                                                  current_date,\
                                                                  prev_date,\
                                                                  ExitMethod['SL_BUY'].value,\
                                                                  monthly_pos_exit_stats_dict_sell[month_year][ExitMethod['SL_BUY'].value])
                elif (low_prices[i] < target_price):
                    pos_buy_price = target_price
                    message = "[Target] Closing position. Time: " + str(date[i]) + " Sell Price: " +\
                        str(pos_sell_price) + " Buy Price: " + str(pos_buy_price)
                    traffic_light_strategy_util.print_debug_log(message, 1)
                    can_close_pos = 1
                    status_list[i] = "[Target] BUY"
                    exit_method = "Target BUY"
                    monthly_pos_exit_stats_dict_sell[month_year][ExitMethod['TARGET_BUY'].value] += 1
                    traffic_light_strategy_util.update_daily_pos_exit_stats(daily_pos_exit_stats_dict_sell,\
                                                                  current_date,\
                                                                  prev_date,\
                                                                  ExitMethod['TARGET_BUY'].value,\
                                                                  monthly_pos_exit_stats_dict_sell[month_year][ExitMethod['TARGET_BUY'].value])
                    
                    if (num_target_sell_per_month.__contains__(month_year) == False):
                        num_target_sell_per_month[month_year] = 0
                    
                    num_target_sell_per_month[month_year] += 1
                        
                    #print("Target achieved !!: ", message)
                elif (high_prices[i] >= decrease_sl_trigger_price and\
                      util.get_time_diff_minutes(date[i], buy_time) > 60 and\
                      0):
                    # Decresing SL to the cost price does not give any better results and hence disabling
                    # this feature.
                    sl_price = pos_buy_price
                    
                if (can_close_pos == 1):
                    buy_time = date[i]
                    is_open_pos_buy = 0
                    is_open_pos_sell = 0
                    open_pos_type = "NA"
                    alert_candle_encountered = 0
                    red_candle_encountered = 0
                    green_candle_encountered = 0
                    high_limit_price_based_on_alert_candle = -1
                    low_limit_price_based_on_alert_candle = -1
                    sl_price_based_on_alert_candle_for_long = -1
                    sl_price_based_on_alert_candle_for_short = -1
                    red_candle = CandleMetadata("-", -1, -1, -1, -1)
                    green_candle = CandleMetadata("-", -1, -1, -1, -1)
                    current_pnl = traffic_light_strategy_util.get_pnl(pos_buy_price,\
                                                           pos_sell_price, num_units)
                    num_buy_wins, num_sell_wins = traffic_light_strategy_util.update_wins_data("SELL",\
                                                                                    current_pnl,\
                                                                                    num_buy_wins,\
                                                                                    num_sell_wins)
                    total_pnl += current_pnl
                    initial_capital += current_pnl
                    traffic_light_strategy_util.update_transaction_record(pos_buy_price, buy_time,\
                                        pos_sell_price, sell_time,\
                                        buy_price_list, buy_time_list,\
                                        sell_price_list, sell_time_list,\
                                        "SELL", position_type_list, current_pnl, pnl_list,\
                                        exit_method, exit_method_list, num_units, num_units_list,\
                                        initial_capital/1000, current_capital_list, pct_pnl_list,\
                                        total_pct_pnl_list,\
                                        target_price, target_price_list,\
                                        price_per_lot, lot_size)
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
                    traffic_light_strategy_util.update_daily_pos_exit_stats(daily_pos_exit_stats_dict_sell,\
                                                                  current_date,\
                                                                  prev_date, 3,\
                                                                  daily_roi)
                        
                continue
                
            # Check if we can open a new position.                                     
            if (current_time > cut_off_time_to_start):
                message = "Not trying to initate a new trade after cutoff time."
                traffic_light_strategy_util.print_debug_log(message, 0)
                alert_candle_encountered = 0
                red_candle_encountered = 0
                green_candle_encountered = 0
                high_limit_price_based_on_alert_candle = -1
                low_limit_price_based_on_alert_candle = -1
                sl_price_based_on_alert_candle_for_long = -1
                sl_price_based_on_alert_candle_for_short = -1
                red_candle = CandleMetadata("-", -1, -1, -1, -1)
                green_candle = CandleMetadata("-", -1, -1, -1, -1)
                continue
            
            if (current_time < start_time):
                message = "Not trying to initate a new trade before start time."
                traffic_light_strategy_util.print_debug_log(message, 0)
                continue
            
            if ((last_trade_date != "" and current_date <= last_trade_date) or\
                (num_trades_per_day_dict.__contains__(current_date) and\
                 num_trades_per_day_dict[current_date] >= max_trades_per_day)):
                continue 
            
            if alert_candle_encountered == 1 :
                if (high_prices[i] > high_limit_price_based_on_alert_candle and\
                  buy_allowed == 1):
                    signal_list[i] = "BUY"
                    pos_buy_price = max(high_limit_price_based_on_alert_candle + 10,\
                                        open_prices[i])
                        
                    sl_price_to_consider = sl_price_based_on_alert_candle_for_long

                    sl_price = math.ceil(sl_price_to_consider) - 5
                    
                    # Setting maximum SL as 100 for every trade.  
                    sl_price = max(math.ceil(pos_buy_price - max_buy_sl),\
                                   sl_price)
                    message = "Changing SL to: " + str(sl_price) + " from: " +\
                        str(sl_price_to_consider)
                    traffic_light_strategy_util.print_debug_log(message, 0)
                    potential_sl = pos_buy_price - sl_price
                    
                    # Risk management
                    num_lots = math.floor(initial_capital / price_per_lot)
                    max_loss = initial_capital * buy_sl_pct / 100
                    potential_loss_per_lot = potential_sl * lot_size
                    # print("Potential loss per lot: " +\
                    #       str(potential_loss_per_lot) + " Max loss: " +\
                    #       str(max_loss))
                    if potential_loss_per_lot == 0:
                        num_lots_throttled = num_lots
                    else:
                        num_lots_throttled = math.floor(max_loss /\
                                                        potential_loss_per_lot)
                            
                    num_lots = min(num_lots, num_lots_throttled)
                    num_units = num_lots * lot_size
                    
                    if num_units == 0:
                        continue

                    is_open_pos_buy = 1
                    buy_time = date[i]
                    last_trade_ctr = i

                    open_pos_type = "BUY"
                    status_list[i] = "BUY"
                    #print("Potential SL: " + str(potential_sl) + " SP: " + str(pos_sell_price))
                    target_price = (pos_buy_price + rr_ratio * potential_sl)
                    message = "BUY trade initiated at: " + str(date[i]) +\
                        " Price: " + str(pos_buy_price) + " Target: " +\
                        str(target_price) + " SL: " + str(sl_price)
                    buy_time = date[i]
                    traffic_light_strategy_util.print_debug_log(message, 1)
                    
                    num_buys += 1
                    util.add_or_update_val_to_key(num_trades_per_day_dict,\
                                                  util.get_date(date[i]), 1)
                elif (low_prices[i] < low_limit_price_based_on_alert_candle and\
                      sell_allowed == 1):
                    signal_list[i] = "SELL"
                    pos_sell_price = min(low_limit_price_based_on_alert_candle - 10,\
                                         open_prices[i])
                        
                    sl_price_to_consider = sl_price_based_on_alert_candle_for_short

                    sl_price = math.ceil(sl_price_to_consider) + 5
                    
                    # Setting maximum SL as 100 for every trade.  
                    sl_price = min(math.ceil(pos_sell_price + max_sell_sl),\
                                   sl_price)
                    message = "Changing SL to: " + str(sl_price) + " from: " +\
                        str(sl_price_to_consider)
                    traffic_light_strategy_util.print_debug_log(message, -1)
                    potential_sl = sl_price - pos_sell_price
                    
                    # Risk management
                    num_lots = math.floor(initial_capital / price_per_lot)
                    max_loss = initial_capital * sell_sl_pct / 100
                    potential_loss_per_lot = potential_sl * lot_size
                    # print("Potential loss per lot: " +\
                    #       str(potential_loss_per_lot) + " Max loss: " +\
                    #       str(max_loss))
                    if potential_loss_per_lot == 0:
                        num_lots_throttled = num_lots
                    else:
                        num_lots_throttled = math.floor(max_loss /\
                                                        potential_loss_per_lot)
                            
                    num_lots = min(num_lots, num_lots_throttled)
                    num_units = num_lots * lot_size
                    
                    if num_units == 0:
                        continue

                    is_open_pos_sell = 1
                    buy_time = date[i]
                    last_trade_ctr = i

                    open_pos_type = "SELL"
                    status_list[i] = "SELL"
                    #print("Potential SL: " + str(potential_sl) + " SP: " + str(pos_sell_price))
                    target_price = (pos_sell_price - rr_ratio * potential_sl)
                    message = "SELL trade initiated at: " + str(date[i]) +\
                        " Price: " + str(pos_sell_price) + " Target: " +\
                        str(target_price) + " SL: " + str(sl_price)
                    sell_time = date[i]
                    traffic_light_strategy_util.print_debug_log(message, 1)
                    
                    num_sells += 1
                    util.add_or_update_val_to_key(num_trades_per_day_dict,\
                                                  util.get_date(date[i]), 1)
                        
            else:
                # Alert candle not encountered till now.
                if green_candle_encountered == 1:
                    if open_prices[i] > prices[i]:
                        alert_candle_encountered = 1
                        red_candle = CandleMetadata(date[i],\
                                                    open_prices[i],\
                                                    high_prices[i],\
                                                    low_prices[i],\
                                                    prices[i])
                    elif open_prices[i] < prices[i] :
                        green_candle = CandleMetadata(date[i],\
                                                      open_prices[i],\
                                                      high_prices[i],\
                                                      low_prices[i],\
                                                      prices[i])
                elif red_candle_encountered == 1:
                    if open_prices[i] < prices[i]:
                       alert_candle_encountered = 1
                       green_candle = CandleMetadata(date[i],\
                                                     open_prices[i],\
                                                     high_prices[i],\
                                                     low_prices[i],\
                                                     prices[i])
                    elif open_prices[i] > prices[i]:
                       red_candle = CandleMetadata(date[i],\
                                                   open_prices[i],\
                                                   high_prices[i],\
                                                   low_prices[i],\
                                                   prices[i]) 
                
                if alert_candle_encountered == 1:
                    message = "Alert candle encountered at: " + str(date[i])
                    traffic_light_strategy_util.print_debug_log(message, 0)
                    high_limit_price_based_on_alert_candle =\
                        max(green_candle.high_price,\
                            red_candle.high_price)
                    low_limit_price_based_on_alert_candle =\
                        min(green_candle.low_price,\
                            red_candle.low_price)
                    
                    # Setting the SLs appropriately.
                    sl_price_based_on_alert_candle_for_long =\
                        low_limit_price_based_on_alert_candle
                    sl_price_based_on_alert_candle_for_short =\
                        high_limit_price_based_on_alert_candle
                    continue        
                            
                if open_prices[i] < prices[i]:
                    message = "Green candle encountered at: " + str(date[i])
                    traffic_light_strategy_util.print_debug_log(message, 0)
                    green_candle_encountered = 1
                    green_candle = CandleMetadata(date[i],\
                                                  open_prices[i],\
                                                  high_prices[i],\
                                                  low_prices[i],\
                                                  prices[i])
                elif open_prices[i] > prices[i] :
                    message = "Red candle encountered at: " + str(date[i])
                    traffic_light_strategy_util.print_debug_log(message, 0)
                    red_candle_encountered = 1
                    red_candle = CandleMetadata(date[i],\
                                                open_prices[i],\
                                                high_prices[i],\
                                                low_prices[i],\
                                                prices[i])
                        
        print("[Initial Capital: 200000 -> Final capital: ", math.floor(initial_capital), "]")
        print("Wealth: ", reserves)
        
        return total_pnl, num_buys, num_buy_wins, num_sells, num_sell_wins, \
            initial_capital, reserves, status_list, signal_list, position_type_list, buy_time_list,\
            buy_price_list, sell_time_list, sell_price_list, pnl_list, exit_method_list, num_units_list,\
            current_capital_list, pct_pnl_list, total_pct_pnl_list, target_price_list,\
            pnl_per_day_of_month_dict, monthly_cash_out_stats_dict, monthly_pos_exit_stats_dict_buy,\
            daily_pos_exit_stats_dict_buy, monthly_pos_exit_stats_dict_sell,\
            daily_pos_exit_stats_dict_sell