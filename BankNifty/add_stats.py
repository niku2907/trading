#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 17:30:10 2021

@author: nishant.gupta
"""


# This class add the stats for the passed DF 'Close Price' column based
# request params if any.

import numpy as np

date = "Date"
open_price = "Open"
high_price = "High"
low_price = "Low"
close_price = "Close"
rsi = "RSI"

class add_stats_helper:        
    def compare(self, price, fast_ema, diff):
        return abs(price - fast_ema) < diff
    
    def compare_ema(self, fast_ema, slow_ema, diff):
        return abs(fast_ema - slow_ema) < diff
    
    def can_buy(self, price, fast_ema, slow_ema, rsi, diff_price_fast_ema, diff_fast_slow_ema):
        cond1 = price > fast_ema
        cond2 = self.compare(price, fast_ema, diff_price_fast_ema)
        cond3 = fast_ema > slow_ema
        cond4 = self.compare_ema(fast_ema, slow_ema, diff_fast_slow_ema)
        cond5 = rsi > 50
        signal = cond1 and cond2 and cond3 and cond4 and cond5
        return signal
    
    def can_sell(self, price, fast_ema, slow_ema, rsi, diff_price_fast_ema, diff_fast_slow_ema):
        cond1 = price < fast_ema
        cond2 = self.compare(price, fast_ema,  diff_price_fast_ema)
        cond3 = fast_ema < slow_ema
        cond4 = self.compare_ema(fast_ema, slow_ema, diff_fast_slow_ema)
        cond5 = rsi < 50
        signal = cond1 and cond2 and cond3 and cond4 and cond5
        return signal
    
class add_stats:
    def ema(DF, period):
        df = DF.copy()
        col_name = 'EMA' + str(period)
        df[col_name] = df[close_price].ewm(span = period, min_periods = period).mean()
        return DF.merge(df.loc[:, [date, col_name]], how = "outer", on = date)
    
    def rsi(DF, n):
        df = DF.copy()
        df['delta'] = df[close_price] - df[close_price].shift(1)
        df['gain'] = np.where(df['delta'] >= 0, df['delta'], 0)
        df['loss']= np.where(df['delta'] < 0, abs(df['delta']), 0)
        avg_gain = []
        avg_loss = []
        gain = df['gain'].tolist()
        loss = df['loss'].tolist()
        for i in range(len(df)):
            if i < n:
                avg_gain.append(np.NaN)
                avg_loss.append(np.NaN)
            elif i == n:
                avg_gain.append(df['gain'].rolling(n).mean().tolist()[n])
                avg_loss.append(df['loss'].rolling(n).mean().tolist()[n])
            elif i > n:
                avg_gain.append(((n-1)*avg_gain[i-1] + gain[i])/n)
                avg_loss.append(((n-1)*avg_loss[i-1] + loss[i])/n)
        df['avg_gain'] = np.array(avg_gain)
        df['avg_loss'] = np.array(avg_loss)
        df['RS'] = df['avg_gain']/df['avg_loss']
        df['RSI'] = 100 - (100/(1+df['RS']))
        return DF.merge(df.loc[:, [date, 'RSI']], how = "outer", on = date)

    
    def buy(DF, fast_ema_col_name, slow_ema_col_name, diff_price_fast_ema, diff_fast_slow_ema):
        helper = add_stats_helper()
        df = DF.copy()
        close_price_series = df[close_price]
        fast_ema_series = df[fast_ema_col_name]
        slow_ema_series = df[slow_ema_col_name]
        rsi_series = df[rsi]
        open_price_series = df[open_price]
        
        # First check based on close price and populate 'BuyCP' column
        buy_cp = []
        for i in range(len(close_price_series)):
            buy_cp.append(helper.can_buy(close_price_series[i], fast_ema_series[i],\
                                                  slow_ema_series[i], rsi_series[i],\
                                                  diff_price_fast_ema, diff_fast_slow_ema))
        df['BuyCP'] = np.array(buy_cp)
        
        buy_op = []
        buy_op.append(False)
        for i in range(1, len(open_price_series)):
            buy_op.append(buy_cp[i-1] and helper.can_buy(open_price_series[i], fast_ema_series[i],\
                                                  slow_ema_series[i], rsi_series[i],\
                                                  diff_price_fast_ema, diff_fast_slow_ema))
        df['BuySignal'] = np.array(buy_op)
        
        #return DF.merge(df.loc[:, [date, 'BuySignal', 'BuyCP']], how = "outer", on = date)
        return DF.merge(df.loc[:, [date, 'BuySignal']], how = "outer", on = date)
    
    def sell(DF, fast_ema_col_name, slow_ema_col_name, diff_price_fast_ema, diff_fast_slow_ema):
        helper = add_stats_helper()
        df = DF.copy()
        close_price_series = df[close_price]
        fast_ema_series = df[fast_ema_col_name]
        slow_ema_series = df[slow_ema_col_name]
        rsi_series = df[rsi]
        open_price_series = df[open_price]
        
        # First check based on close price and populate 'BuyCP' column
        sell_cp = []
        for i in range(len(close_price_series)):
            sell_cp.append(helper.can_sell(close_price_series[i], fast_ema_series[i],\
                                                  slow_ema_series[i], rsi_series[i],\
                                                  diff_price_fast_ema, diff_fast_slow_ema))
        df['SellCP'] = np.array(sell_cp)
        
        sell_op = []
        sell_op.append(False)
        for i in range(1, len(open_price_series)):
            sell_op.append(sell_cp[i-1] and helper.can_sell(open_price_series[i], fast_ema_series[i],\
                                                  slow_ema_series[i], rsi_series[i],\
                                                  diff_price_fast_ema, diff_fast_slow_ema))
        df['SellSignal'] = np.array(sell_op)
        
        #return DF.merge(df.loc[:, [date, 'SellSignal', 'SellCP']], how = "outer", on = date)
        return DF.merge(df.loc[:, [date, 'SellSignal']], how = "outer", on = date)
    
    