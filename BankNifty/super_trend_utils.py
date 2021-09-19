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
    def get_pnl(buy_price, sell_price):
        if (buy_price > sell_price):
            print("Loss of: ", buy_price - sell_price)
        else:
            print("Profit of: ", sell_price - buy_price)
        
        return sell_price - buy_price
    
    # SUPERTREND STRATEGY
    @staticmethod
    def implement_st_strategy(data, have_cut_off_time_check):
        prices = data['Close']
        st = data['st']
        date = data['Date']
        ema = data['EMA50']
        
        cut_off_time_to_start = '14:30:00'
        cut_off_time_to_close = '15:00:00'
        is_open_pos = 0
        open_pos_type = 'NA'
        buy_time = ""
        sell_time = ""
        pos_buy_price = 0
        pos_sell_price = 0
        total_pnl = 0
        
        status_list = ['NA' for i in range(len(st))]
        signal_list = ['NA' for i in range(len(st))]
        
        for i in range(len(st)):
            if i <= 1:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                # st_signal.append(np.nan)
                continue
            
            current_time = util.get_time(date[i])
            if (have_cut_off_time_check == 1):
                if (current_time >= cut_off_time_to_close):
                    if (is_open_pos == 1):
                        if (open_pos_type == "BUY"):
                            pos_buy_price = prices[i]
                            print("Autosquare off initiated. Buy price: ", pos_buy_price)
                            open_pos_type = ""
                            is_open_pos = 0
                            status_list[i] = "BUY"
                        else:
                            pos_sell_price = prices[i]
                            print("Autosquare off initiated. Sell price: ", pos_sell_price)
                            open_pos_type = ""
                            is_open_pos = 0
                            status_list[i] = "SELL"
                        
                        total_pnl += super_trend_utils.get_pnl(pos_buy_price, pos_sell_price)
                    continue
    
                if (current_time > cut_off_time_to_start):
                    print("Not trying to initate a new trade after cutoff time.")
                    continue
            
            if (super_trend_utils.can_buy(st[i-1], prices[i-1], st[i], prices[i],\
                                          ema[i])) :
                signal_list[i] = "BUY"
                
                # Ideally sell price should be opening price of the next candle.
                if (is_open_pos == 0):
                    buy_time = util.get_time(date[i])
                    pos_buy_price = prices[i]
                    print("Buy trade initiated at: ", buy_time, " Price: ",\
                          pos_buy_price)
                    is_open_pos = 1
                    open_pos_type = "BUY"
                    status_list[i] = "BUY"
                else:
                    if (open_pos_type == "BUY"):
                        print("Already an open BUY position for the same day.")
                    elif (open_pos_type == "SELL"):
                        buy_time = util.get_time(date[i])
                        pos_buy_price = prices[i]
                        print("Closing position. Time: ", buy_time, "Buy price: ",\
                              pos_buy_price, " Sell price: ", pos_sell_price)
                        is_open_pos = 0
                        open_pos_type = "NA"
                        status_list[i] = "BUY"
                        total_pnl += super_trend_utils.get_pnl(pos_buy_price,\
                                                               pos_sell_price)
                        
            elif (super_trend_utils.can_sell(st[i-1], prices[i-1], st[i], prices[i],\
                                             ema[i])):
                signal_list[i] = "SELL"
                
                # Ideally sell price should be opening price of the next candle.
                if (is_open_pos == 0):
                    sell_time = util.get_time(date[i])
                    pos_sell_price = prices[i]
                    print("Sell trade initiated at: ", sell_time, " Price: ",\
                          pos_sell_price)
                    is_open_pos = 1
                    open_pos_type = "SELL"
                    status_list[i] = "SELL"
                else:
                    if (open_pos_type == "SELL"):
                        print("Already an open SELL position for the same day.")
                    elif (open_pos_type == "BUY"):
                        sell_time = util.get_time(date[i])
                        pos_sell_price = prices[i]
                        print("Closing position. Time: ", sell_time, "Sell price: ",\
                              pos_sell_price, " Buy price: ", pos_buy_price)
                        is_open_pos = 0
                        open_pos_type = "NA"
                        status_list[i] = "SELL"
                        total_pnl += super_trend_utils.get_pnl(pos_buy_price,\
                                                               pos_sell_price)
                            
        return total_pnl, status_list, signal_list

                
    # Plot super trend signals. 
    def plot_super_trend_band(data):
        plt.plot(data['Close'], linewidth = 2, label = 'CLOSING PRICE')
        plt.plot(data['st'], color = 'green', linewidth = 2,\
             label = 'ST UPTREND 10,3')
        plt.plot(data['st_dt'], color = 'r', linewidth = 2,\
             label = 'ST DOWNTREND 10,3')
        plt.legend(loc = 'upper left')
        plt.show()