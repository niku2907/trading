#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 10:27:41 2021

@author: nishant.gupta
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 21:07:39 2021

@author: nishant.gupta
"""

import math
import pandas as pd
import numpy as np

from util import util

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
    
    # Get BUY signal
    @staticmethod
    def can_buy(prev_st, prev_price, current_st, current_price, ema):
        if (prev_st > prev_price and current_st < current_price):
            return current_price > ema
        
        return False
    
    # Get SELL signal
    @staticmethod
    def can_sell(prev_st, prev_price, current_st, current_price, ema):
        if (prev_st < prev_price and current_st > current_price):
            return current_price < ema
        
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
        for i in range(len(macd_list)):
            test_date = util.get_date_time(date_list[i])
            current_date = util.get_date_time(current_date)
            if (test_date <= current_date):
                continue
            
            if (i == 0):
                continue
            look_back = 2
            if (util.get_date_time(date_list[i-1]) == util.get_date_time(current_date) or\
                i-look_back < 0):
                look_back = 1
            
            message = "Using MACD of Date: " + str(date_list[i-look_back])
            custom_strategy_util.print_debug_log(message, 0)
            if (macd_list[i-look_back] > macd_signal_list[i-look_back]):
                return "BUY"
            else:
                return "SELL"
        return "NA"
    
    @staticmethod
    def update_wins_data(pos_type, pnl, num_buy_wins, num_sell_wins):
        if (pnl > 0):
            if (pos_type == "BUY"):
                num_buy_wins += 1
            elif (pos_type == "SELL"):
                num_sell_wins += 1
        
        return num_buy_wins, num_sell_wins
            
    def implement_strategy(data, buy_sl_pct, buy_dates, ema_period, sell_sl_pct, longer_tf,\
                           buy_allowed, sell_allowed):
        prices = data['Close']
        date = data['Date']
        st = data['st']
        ema = data['EMA' + str(ema_period)]
        high_prices = data['High']
        low_prices = data['Low']
        open_prices = data['Open']
        macd = longer_tf['MACD']
        macd_signal = longer_tf['MACD_Signal']
        
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
        pct_pnl_list = []
        target_price_list = []
        total_pct_pnl_list = []
        
        status_list = ['NA' for i in range(len(data))]
        signal_list = ['NA' for i in range(len(data))]
        
        initial_capital = 10000
        num_units = 0
        last_trade_ctr = -1
        last_trade_date = ""
        dynamic_sl = 1
        
        num_sells = 0
        num_sell_wins = 0
        num_buys = 0
        num_buy_wins = 0
        
        debug_date = ""
        for i in range(len(data)):
            if (initial_capital <= 0):
                break
            
            if (i <= last_trade_ctr or i <= 1):
                continue
            
            current_time = util.get_time(date[i])
            
                        
            if (debug_date != "" and util.get_date(date[i]) < debug_date):
                continue
            
            # Check if autosqaure off needed.
            if (current_time >= cut_off_time_to_close):
                if (is_open_pos == 1):
                    pos_type = "BUY"
                    exit_method = "Cutoff BUY"
                    if (open_pos_type == "BUY"):
                        pos_sell_price = prices[i]
                        message = "Autosquare off initiated. Sell price: " + str(pos_sell_price)
                        custom_strategy_util.print_debug_log(message, 0)
                        open_pos_type = ""
                        is_open_pos = 0
                        status_list[i] = "[Cutoff] SELL"
                        sell_time = date[i]
                        exit_method = "Cutoff SELL"
                        
                    else:
                        pos_buy_price = prices[i]
                        message = "Autosquare off initiated. Buy price: " + str(pos_buy_price)
                        custom_strategy_util.print_debug_log(message, 0)
                        open_pos_type = ""
                        is_open_pos = 0
                        status_list[i] = "[Cutoff] BUY"
                        buy_time = date[i]
                        pos_type = "SELL"
                    
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
                        custom_strategy_util.print_debug_log(message, 0)
                        can_close_pos = 1
                        status_list[i] = "[SL] SELL"
                        exit_method = "SL SELL"
                        
                    # Check if target achieved.
                    elif (high_prices[i] >= target_price):
                        pos_sell_price = target_price
                        message = "[Target] Closing position. Time: " + str(date[i]) + " Buy Price: " +\
                            str(pos_buy_price) + " Sell Price: " + str(pos_sell_price)
                        custom_strategy_util.print_debug_log(message, 0)
                        can_close_pos = 1
                        status_list[i] = "[Target] SELL"
                        exit_method = "Target SELL"

                    if (can_close_pos == 1):
                        sell_time = date[i]
                        is_open_pos = 0
                        open_pos_type = "NA"
                        current_pnl = custom_strategy_util.get_pnl(pos_buy_price,\
                                                               pos_sell_price, num_units)
                        num_buy_wins, num_sell_wins = custom_strategy_util.update_wins_data("BUY",\
                                                                                        current_pnl,\
                                                                                        num_buy_wins,\
                                                                                        num_sell_wins)
                        total_pnl += current_pnl
                        initial_capital += current_pnl
                        custom_strategy_util.update_transaction_record(pos_buy_price, buy_time,\
                                            pos_sell_price, sell_time,\
                                            buy_price_list, buy_time_list,\
                                            sell_price_list, sell_time_list,\
                                            "BUY", position_type_list, current_pnl, pnl_list,\
                                            exit_method, exit_method_list, num_units, num_units_list,\
                                            initial_capital /1000, current_capital_list, pct_pnl_list,\
                                            total_pct_pnl_list,\
                                            target_price, target_price_list)
                elif (open_pos_type == "SELL"):
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
                    elif (low_prices[i] <= target_price):
                        pos_buy_price = target_price
                        message = "[Target] Closing position. Time: " + str(date[i]) + " Buy Price: " +\
                            str(pos_buy_price) + " Sell Price: " + str(pos_sell_price)
                        custom_strategy_util.print_debug_log(message, 0)
                        can_close_pos = 1
                        status_list[i] = "[Target] BUY"
                        exit_method = "Target BUY"
                        
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
                continue
            
            # Check if we can open a new position.                                     
            if (current_time > cut_off_time_to_start):
                message = "Not trying to initate a new trade after cutoff time."
                custom_strategy_util.print_debug_log(message, -1)
                continue
            
            current_date = util.get_date(date[i])
            if (last_trade_date != "" and current_date <= last_trade_date):
                continue
            
            if (buy_dates.__contains__(util.get_date(data['Date'][i])) and\
                buy_allowed):
                trigger_price = buy_dates[util.get_date(data['Date'][i])]
                if (i+3 >= len(data) or util.get_time(date[i+3]) > cut_off_time_to_start):
                    continue
                
                if (prices[i] >= trigger_price):
                    if (low_prices[i+1] > low_prices[i] and\
                        low_prices[i+2] > low_prices[i] and\
                        prices[i+1] >= trigger_price and\
                        prices[i+2] >= trigger_price):
                        i += 3
                        
                        last_trade_ctr = i
                        num_units = math.floor((5 * initial_capital) / open_prices[i])
                        if (dynamic_sl):
                            sl_pct_actual = buy_sl_pct * 5
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
                        custom_strategy_util.print_debug_log(message, 0)
                        is_open_pos = 1
                        open_pos_type = "BUY"
                        status_list[i] = "BUY"
                        sl_price = low_prices[i-3]
                        target_price = 2 * (open_prices[i] - sl_price) + open_prices[i]
                        message = "Target: " + str(target_price) + " SL: " + str(sl_price)
                        custom_strategy_util.print_debug_log(message, 0)
                        num_buys += 1
                        #last_trade_date = util.get_date(date[i])
                        
            elif (custom_strategy_util.can_sell(st[i-1], prices[i-1], st[i], prices[i],\
                                             ema[i]) and\
                  custom_strategy_util.get_signal_based_on_macd(macd, macd_signal,\
                                                          longer_tf['Date'], date[i]) == "SELL" and\
                  sell_allowed):
                if (i+1 >= len(data) or util.get_time(date[i+1]) > cut_off_time_to_start):
                    continue
                
                i += 1
                signal_list[i] = "SELL"
                potential_sl =  st[i-1] - open_prices[i]
                sell_time = date[i]
                last_trade_ctr = i

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
                message = "Sell trade initiated at: " + str(date[i]) + " Price: " + str(pos_sell_price)
                custom_strategy_util.print_debug_log(message, 0)
                is_open_pos = 1
                open_pos_type = "SELL"
                status_list[i] = "SELL"
                sl_price = st[i-1]
                target_price = open_prices[i] - 2 * (sl_price - open_prices[i])
                num_sells += 1
                #last_trade_date = util.get_date(date[i])
                
        print("[Initial Capital: 10000 -> Final capital: ", math.floor(initial_capital), "]")
        return total_pnl, num_buys, num_buy_wins, num_sells, num_sell_wins, \
            initial_capital, status_list, signal_list, position_type_list, buy_time_list,\
            buy_price_list, sell_time_list, sell_price_list, pnl_list, exit_method_list, num_units_list,\
            current_capital_list, pct_pnl_list, total_pct_pnl_list, target_price_list