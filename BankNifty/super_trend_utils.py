#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 20:33:34 2021

@author: nishant.gupta
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from util import util

class super_trend_utils:
    # SUPERTREND CALCULATION
    def get_supertrend(high, low, close, lookback, multiplier):
        
        # ATR
        tr1 = pd.DataFrame(high - low)
        tr2 = pd.DataFrame(abs(high - close.shift(1)))
        tr3 = pd.DataFrame(abs(low - close.shift(1)))
        frames = [tr1, tr2, tr3]
        tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
        atr = tr.ewm(lookback).mean()
        # H/L AVG AND BASIC UPPER & LOWER BAND
        
        hl_avg = (high + low) / 2
        upper_band = (hl_avg + multiplier * atr).dropna()
        lower_band = (hl_avg - multiplier * atr).dropna()
        
        # FINAL UPPER BAND
        
        final_bands = pd.DataFrame(columns = ['upper', 'lower'])
        final_bands.iloc[:,0] = [x for x in upper_band - upper_band]
        final_bands.iloc[:,1] = final_bands.iloc[:,0]
        
        for i in range(len(final_bands)):
            if i == 0:
                final_bands.iloc[i,0] = 0
            else:
                if (upper_band[i] < final_bands.iloc[i-1,0]) | (close[i-1] > final_bands.iloc[i-1,0]):
                    final_bands.iloc[i,0] = upper_band[i]
                else:
                    final_bands.iloc[i,0] = final_bands.iloc[i-1,0]
        
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
        
        supertrend = pd.DataFrame(columns = [f'supertrend_{lookback}'])
        supertrend.iloc[:,0] = [x for x in final_bands['upper'] - final_bands['upper']]
        for i in range(len(supertrend)):
            if i == 0:
                supertrend.iloc[i, 0] = 0
            elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 0] and close[i] < final_bands.iloc[i, 0]:
                supertrend.iloc[i, 0] = final_bands.iloc[i, 0]
            elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 0] and close[i] > final_bands.iloc[i, 0]:
                supertrend.iloc[i, 0] = final_bands.iloc[i, 1]
            elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 1] and close[i] > final_bands.iloc[i, 1]:
                supertrend.iloc[i, 0] = final_bands.iloc[i, 1]
            elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 1] and close[i] < final_bands.iloc[i, 1]:
                supertrend.iloc[i, 0] = final_bands.iloc[i, 0]
        
        supertrend = supertrend.set_index(upper_band.index)
        # TODO(Nishant): Debug as to why do we need following line.
        #supertrend = supertrend.dropna()[1:]
        
        # ST UPTREND/DOWNTREND
        
        upt = []
        dt = []
        close = close.iloc[len(close) - len(supertrend):]
        for i in range(len(supertrend)):
            if close[i] > supertrend.iloc[i, 0]:
                upt.append(supertrend.iloc[i, 0])
                dt.append(np.nan)
            elif close[i] < supertrend.iloc[i, 0]:
                upt.append(np.nan)
                dt.append(supertrend.iloc[i, 0])
            else:
                upt.append(np.nan)
                dt.append(np.nan)
          
        st, upt, dt = pd.Series(supertrend.iloc[:, 0]), pd.Series(upt), pd.Series(dt)
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
    def can_buy_based_on_st(prev_st, prev_price, current_st, current_price):
        if (prev_st > prev_price and current_st < current_price):
            return True
        return False
    
    @staticmethod
    def can_sell_based_on_st(prev_st, prev_price, current_st, current_price):
        if (prev_st < prev_price and current_st > current_price):
            return True
        return False
    
    @staticmethod
    def get_pnl(buy_price, sell_price):
        if (buy_price > sell_price):
            print("Loss of: ", buy_price - sell_price)
        else:
            print("Profit of: ", sell_price - buy_price)
        
        return super_trend_utils.get_pnl_including_taxes(buy_price, sell_price, 1, 100)
    
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
                                  exit_method, exit_method_list):
        buy_price_list.append(pos_buy_price)
        sell_price_list.append(pos_sell_price)
        buy_time_list.append(buy_time)
        sell_time_list.append(sell_time)
        pos_type_list.append(pos_type)
        pnl_list.append(current_pnl)
        exit_method_list.append(exit_method)
        
    # SUPERTREND STRATEGY
    @staticmethod
    def implement_st_strategy(data, have_cut_off_time_check, ema_period, target_pct,\
                              sl_pct):
        prices = data['Close']
        st = data['st']
        date = data['Date']
        ema = data['EMA' + str(ema_period)]
        high_prices = data['High']
        low_prices = data['Low']
        open_prices = data['Open']
        
        cut_off_time_to_start = '14:30:00'
        cut_off_time_to_close = '15:00:00'
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
        
        status_list = ['NA' for i in range(len(st))]
        signal_list = ['NA' for i in range(len(st))]
        
        for i in range(len(st)):
            if i <= 1:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                # st_signal.append(np.nan)
                continue
            
            current_time = util.get_time(date[i])
            
            # Check if autosqaure off needed.
            if (have_cut_off_time_check == 1):
                if (current_time >= cut_off_time_to_close):
                    if (is_open_pos == 1):
                        pos_type = "BUY"
                        exit_method = "Cutoff BUY"
                        if (open_pos_type == "BUY"):
                            pos_sell_price = prices[i]
                            print("Autosquare off initiated. Sell price: ", pos_sell_price)
                            open_pos_type = ""
                            is_open_pos = 0
                            status_list[i] = "[Cutoff] SELL"
                            sell_time = date[i]
                            exit_method = "Cutoff SELL"
                        else:
                            pos_buy_price = prices[i]
                            print("Autosquare off initiated. Buy price: ", pos_buy_price)
                            open_pos_type = ""
                            is_open_pos = 0
                            status_list[i] = "[Cutoff] BUY"
                            buy_time = date[i]
                            pos_type = "SELL"
                        
                        current_pnl = super_trend_utils.get_pnl(pos_buy_price, pos_sell_price)
                        super_trend_utils.update_transaction_record(pos_buy_price, buy_time,\
                                            pos_sell_price, sell_time,\
                                            buy_price_list, buy_time_list,\
                                            sell_price_list, sell_time_list,\
                                            pos_type, position_type_list, current_pnl, pnl_list,\
                                            exit_method, exit_method_list)
                        total_pnl += current_pnl
                    continue
    
                if (current_time > cut_off_time_to_start):
                    message = "Not trying to initate a new trade after cutoff time."
                    super_trend_utils.print_debug_log(message, 0)
                    continue
            
            if (is_open_pos == 1):
                if (open_pos_type == "BUY"):
                    can_close_pos = 0
                    exit_method = ""
                    # Check if SL hit.
                    if (low_prices[i] <= sl_price):
                        pos_sell_price = low_prices[i]
                        print("[SL] Closing position. Time: ", date[i],\
                              " Buy Price: ", pos_buy_price, " Sell Price: ",\
                                  pos_sell_price)
                        can_close_pos = 1
                        status_list[i] = "[SL] SELL"
                        exit_method = "SL SELL"
                    # Check if target achieved.
                    elif (high_prices[i] >= target_price):
                        pos_sell_price = target_price
                        print("[Target] Closing position. Time: ", date[i],\
                              " Buy Price: ", pos_buy_price, " Sell Price: ",\
                                  pos_sell_price)
                        can_close_pos = 1
                        status_list[i] = "[Target] SELL"
                        exit_method = "Target SELL"
                    # Check if ST signal changed.
                    elif (super_trend_utils.can_sell_based_on_st(st[i-1], prices[i-1], st[i], prices[i])):
                        pos_sell_price = prices[i]
                        print("[ST] Closing position. Time: ", date[i],\
                              " Buy Price: ", pos_buy_price, " Sell Price: ",\
                                  pos_sell_price)
                        can_close_pos = 1
                        status_list[i] = "[ST] SELL"
                        exit_method = "ST SELL"

                    if (can_close_pos == 1):
                        sell_time = date[i]
                        is_open_pos = 0
                        open_pos_type = "NA"
                        current_pnl = super_trend_utils.get_pnl(pos_buy_price,\
                                                               pos_sell_price)
                        total_pnl += current_pnl
                        super_trend_utils.update_transaction_record(pos_buy_price, buy_time,\
                                            pos_sell_price, sell_time,\
                                            buy_price_list, buy_time_list,\
                                            sell_price_list, sell_time_list,\
                                            "BUY", position_type_list, current_pnl, pnl_list,\
                                            exit_method, exit_method_list)
                elif (open_pos_type == "SELL"):
                    can_close_pos = 0
                    exit_method = ""
                    # Check if SL hit.
                    if (high_prices[i] >= sl_price):
                        pos_buy_price = high_prices[i]
                        print("[SL] Closing position. Time: ", date[i],\
                              " Buy Price: ", pos_buy_price, " Sell Price: ",\
                                  pos_sell_price)
                        can_close_pos = 1
                        status_list[i] = "[SL] BUY"
                        exit_method = "SL BUY"
                    elif (low_prices[i] <= target_price):
                        pos_buy_price = target_price
                        print("[Target] Closing position. Time: ", date[i],\
                              " Buy Price: ", pos_buy_price, " Sell Price: ",\
                                  pos_sell_price)
                        can_close_pos = 1
                        status_list[i] = "[Target] BUY"
                        exit_method = "Target BUY"
                    # Check if ST signal changed.
                    elif (super_trend_utils.can_buy_based_on_st(st[i-1], prices[i-1], st[i], prices[i])):
                        pos_buy_price = prices[i]
                        print("[ST] Closing position. Time: ", date[i],\
                              " Buy Price: ", pos_buy_price, " Sell Price: ",\
                                  pos_sell_price)
                        can_close_pos = 1
                        status_list[i] = "[ST] BUY"
                        exit_method = "ST BUY"
                        
                    if (can_close_pos == 1):
                        buy_time = date[i]
                        is_open_pos = 0
                        open_pos_type = "NA"
                        current_pnl = super_trend_utils.get_pnl(pos_buy_price,\
                                                               pos_sell_price)
                        total_pnl += current_pnl
                        super_trend_utils.update_transaction_record(pos_buy_price, buy_time,\
                                            pos_sell_price, sell_time,\
                                            buy_price_list, buy_time_list,\
                                            sell_price_list, sell_time_list,\
                                            "SELL", position_type_list, current_pnl, pnl_list,\
                                            exit_method, exit_method_list)
                continue
            
            # Check if we can open a new position.                                     
            if (super_trend_utils.can_buy(st[i-1], prices[i-1], st[i], prices[i],\
                                          ema[i])) :
                signal_list[i] = "BUY"
                potential_sl = prices[i] - st[i]
                allowed_sl = prices[i] * sl_pct / 100
                if (potential_sl > allowed_sl):
                    message = "SL needed is not in the limits."
                    super_trend_utils.print_debug_log(message, 0)
                    continue
                target_price = prices[i] * (1 + target_pct / 100)
                buy_time = date[i]
                
                # Ideally sell price should be opening price of the next candle.
                pos_buy_price = prices[i]
                print("Buy trade initiated at: ", date[i], " Price: ",\
                      pos_buy_price)
                is_open_pos = 1
                open_pos_type = "BUY"
                status_list[i] = "BUY"
                sl_price = st[i]
            elif (super_trend_utils.can_sell(st[i-1], prices[i-1], st[i], prices[i],\
                                             ema[i])):
                signal_list[i] = "SELL"
                potential_sl =  st[i] - prices[i]
                allowed_sl = prices[i] * sl_pct / 100
                if (potential_sl > allowed_sl):
                    message = "SL needed is not in the limits."
                    super_trend_utils.print_debug_log(message, 0)
                    continue
                target_price = prices[i] * (1 - target_pct / 100)
                sell_time = date[i]
                
                # Ideally sell price should be opening price of the next candle.
                pos_sell_price = prices[i]
                print("Sell trade initiated at: ", date[i], " Price: ",\
                      pos_sell_price)
                is_open_pos = 1
                open_pos_type = "SELL"
                status_list[i] = "SELL"
                sl_price = st[i]
            else:
                # dynamic SL.
                if (is_open_pos == 5):
                    if (open_pos_type == "BUY"):
                        if (sl_price < st[i] and st[i] < pos_buy_price):
                            print("Trailing the SL for BUY position.")
                            sl_price = st[i]
                    elif (open_pos_type == "SELL"):
                        if (sl_price > st[i] and st[i] > pos_sell_price):
                            print("Trailing the SL for SELL position.")
                            sl_price = st[i]
                
                            
        return total_pnl, status_list, signal_list, position_type_list, buy_time_list, buy_price_list,\
            sell_time_list, sell_price_list, pnl_list, exit_method_list

                
    # Plot super trend signals. 
    def plot_super_trend_band(data):
        plt.plot(data['Close'], linewidth = 2, label = 'CLOSING PRICE')
        plt.plot(data['st'], color = 'green', linewidth = 2,\
             label = 'ST UPTREND 10,3')
        plt.plot(data['st_dt'], color = 'r', linewidth = 2,\
             label = 'ST DOWNTREND 10,3')
        plt.legend(loc = 'upper left')
        plt.show()