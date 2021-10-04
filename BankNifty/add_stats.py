#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 17:30:10 2021

@author: nishant.gupta
"""


# This class add the stats for the passed DF 'Close Price' column based
# request params if any.

import pandas as pd
import numpy as np
import statsmodels.api as sm

date = "Date"
open_price = "Open"
high_price = "High"
low_price = "Low"
close_price = "Close"
rsi = "RSI"

class candle:
    def __init__(self, open_price, high_price, low_price, close_price):
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        
        
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
    
    def is_candidate_for_parent_candle(self, test_candle, threshold):
        if (self.is_red_candle(test_candle)):
            return test_candle.open_price - test_candle.close_price >= threshold
        else:
            return test_candle.close_price - test_candle.open_price >= threshold
    
    def is_red_candle(self, test_candle):
        return test_candle.close_price < test_candle.open_price
    
    def is_candidate_for_child_candle(self, child_candle, parent_candle):
        if (child_candle.low_price > parent_candle.low_price and \
            child_candle.high_price < parent_candle.high_price):
            return True
        else:
            return False

class add_stats:
    def ema(DF, period):
        df = DF.copy()
        col_name = 'EMA' + str(period)
        df[col_name] = df[close_price].ewm(span = period, min_periods = period).mean()
        return DF.merge(df.loc[:, [date, col_name]], how = "outer", on = date)
    
    def simple_ma(DF, period):
        df = DF.copy()
        col_name = 'SMA' + str(period)
        df[col_name] = df[close_price].rolling(window = period).mean()
        return DF.merge(df.loc[:, [date, col_name]], how = "outer", on = date)
    
    def slope(ser, period):
        "function to calculate the slope of n consecutive points on a plot"
        n = len(ser)
        slopes = [0 for i in range(0, n)]
        for i in range(period-1, n):
            slopes[i] = 100 * (ser[i] - ser[i-period+1]) / ser[i-period+1]
        # for i in range(period - 1, n - 1):
        #     y = ser[i - period + 1: i]
        #     y_scaled = (y - y[i - period + 1]) / y[i - period + 1]
        #     print("Diff: ", y_scaled)
        #     slopes.append(y_scaled / n)
            
        return np.array(slopes)
        # slope_angle = (np.rad2deg(np.arctan(np.array(slopes))))
        # return np.array(slope_angle)
    
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
    
    def MACD(DF, a, b, c):
        # a: fast moving average
        # b: slow moving average
        # c: period of moving average for the signal line (Fast - Slow)
        """function to calculate MACD
           typical values a = 12; b = 26, c = 9"""
        df = DF.copy()
        df["MA_Fast"]=df["Close"].ewm(span = a, min_periods = a).mean()
        df["MA_Slow"]=df["Close"].ewm(span = b, min_periods = b).mean()
        df["MACD"]=df["MA_Fast"] - df["MA_Slow"]
        df["MACD_Signal"]=df["MACD"].ewm(span = c, min_periods = c).mean()
        df.dropna(inplace = True)
        return DF.merge(df.loc[:, [date, 'MACD', 'MACD_Signal']], how = "outer", on = date)
    
    @staticmethod
    def ATR(DF, n):
        "function to calculate True Range and Average True Range"
        df = DF.copy()
        df['H-L'] = abs(df['High']-df['Low'])
        df['H-PC'] = abs(df['High']-df['Close'].shift(1))
        df['L-PC'] = abs(df['Low']-df['Close'].shift(1))
        df['TR'] = df[['H-L','H-PC','L-PC']].max(axis=1, skipna=False)
        df['ATR'] = df['TR'].rolling(n).mean()
        #df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()
        df2 = df.drop(['H-L','H-PC','L-PC'], axis=1)
        return df2
    
    def beyond_ATR(DF):
        df = DF.copy()
        df['CanBuy'] = df['High'] > (df['ATR'].shift(1) + df['Close'].shift(1))
        df['CanSell'] = df['Low'] < (df['Close'].shift(1) - df['ATR'].shift(1))
        return df

    def ADX(DF,n):
        "function to calculate ADX"
        df2 = DF.copy()
        df2['TR'] = add_stats.ATR(df2,n)['TR'] #the period parameter of ATR function does not matter because period does not influence TR calculation
        df2['DMplus'] = np.where((df2['High']-df2['High'].shift(1)) > (df2['Low'].shift(1) - df2['Low']), df2['High'] - df2['High'].shift(1), 0)
        df2['DMplus'] = np.where(df2['DMplus']<0,0,df2['DMplus'])
        df2['DMminus'] = np.where((df2['Low'].shift(1) - df2['Low']) > (df2['High'] - df2['High'].shift(1)), df2['Low'].shift(1) - df2['Low'], 0)
        df2['DMminus'] = np.where(df2['DMminus'] < 0, 0, df2['DMminus'])
        TRn = []
        DMplusN = []
        DMminusN = []
        TR = df2['TR'].tolist()
        DMplus = df2['DMplus'].tolist()
        DMminus = df2['DMminus'].tolist()
        for i in range(len(df2)):
            if i < n:
                TRn.append(np.NaN)
                DMplusN.append(np.NaN)
                DMminusN.append(np.NaN)
            elif i == n:
                TRn.append(df2['TR'].rolling(n).sum().tolist()[n])
                DMplusN.append(df2['DMplus'].rolling(n).sum().tolist()[n])
                DMminusN.append(df2['DMminus'].rolling(n).sum().tolist()[n])
            elif i > n:
                TRn.append(TRn[i-1] - (TRn[i-1]/n) + TR[i])
                DMplusN.append(DMplusN[i-1] - (DMplusN[i-1]/n) + DMplus[i])
                DMminusN.append(DMminusN[i-1] - (DMminusN[i-1]/n) + DMminus[i])
        df2['TRn'] = np.array(TRn)
        df2['DMplusN'] = np.array(DMplusN)
        df2['DMminusN'] = np.array(DMminusN)
        df2['DIplusN'] = 100*(df2['DMplusN']/df2['TRn'])
        df2['DIminusN'] = 100*(df2['DMminusN']/df2['TRn'])
        df2['DIdiff'] = abs(df2['DIplusN']-df2['DIminusN'])
        df2['DIsum'] = df2['DIplusN']+df2['DIminusN']
        df2['DX'] = 100*(df2['DIdiff']/df2['DIsum'])
        ADX = []
        DX = df2['DX'].tolist()
        for j in range(len(df2)):
            if j < 2*n-1:
                ADX.append(np.NaN)
            elif j == 2*n-1:
                ADX.append(df2['DX'][j-n+1:j+1].mean())
            elif j > 2*n-1:
                ADX.append(((n-1)*ADX[j-1] + DX[j])/n)
        df2['ADX']=np.array(ADX)
        return DF.merge(df2.loc[:, [date, 'ADX']], how = "outer", on = date)
    
    def inside_candle_info(DF, parent_candle_length):
        helper = add_stats_helper()
        df = DF.copy()
        df.reset_index(inplace = True)
        close_price_series = df[close_price]
        open_price_series = df[open_price]
        high_price_series = df[high_price]
        low_price_series = df[low_price]
        
        parent_candle_candidates = []
        child_candle_candidates = []
        candle_color = []
        child_candle_trigger_price = []
        child_candle_direction = []
        child_candle_sl = []
        child_candle_target = []
        for i in range(0, len(close_price_series)):
            current_candle = candle(open_price = open_price_series[i],\
                                    high_price = high_price_series[i],\
                                    low_price = low_price_series[i],\
                                    close_price = close_price_series[i])
            parent_candle_candidates.append(helper.is_candidate_for_parent_candle(current_candle,\
                                                                                  parent_candle_length))
            if (helper.is_red_candle(current_candle) == True):
                candle_color.append('Red')
            else:
                candle_color.append('Green')
            
            child_candle_candidates.append(False)
            child_candle_trigger_price.append(-1)
            child_candle_direction.append('NA')
            child_candle_sl.append(-1)
            child_candle_target.append(-1)

        for i in range(0, len(parent_candle_candidates)):
            if (parent_candle_candidates[i] == True):
                # If next candle is also a candidate for being a parent we ignore this candle.
                if (i+1 < len(parent_candle_candidates)):
                    if (parent_candle_candidates[i+1] == True):
                        continue
                parent_candle = candle(open_price = open_price_series[i],\
                                    high_price = high_price_series[i],\
                                    low_price = low_price_series[i],\
                                    close_price = close_price_series[i])
                for j in range(i+1, len(close_price_series)):
                    current_candle = candle(open_price = open_price_series[j],\
                                    high_price = high_price_series[j],\
                                    low_price = low_price_series[j],\
                                    close_price = close_price_series[j])
                    child_candle_candidates[j] = helper.is_candidate_for_child_candle(current_candle, parent_candle)
                    if (child_candle_candidates[j] == False):
                        break
                    else:
                        if (helper.is_red_candle(parent_candle)):
                            child_candle_trigger_price[j] = parent_candle.low_price
                            child_candle_direction[j] = 'Short'
                            child_candle_sl[j] = current_candle.high_price + 10
                            child_candle_target[j] = parent_candle.high_price - parent_candle.low_price
                        else:
                            child_candle_trigger_price[j] = parent_candle.high_price
                            child_candle_direction[j] = 'Long'
                            child_candle_sl[j] = current_candle.low_price - 10
                            child_candle_target[j] = parent_candle.high_price - parent_candle.low_price

        for i in range(0, len(child_candle_candidates)):
            if (child_candle_candidates[i] == True and 0):
                print("Found inside candle.")
        
        df['IsParent'] = np.array(parent_candle_candidates)
        df['IsChild'] = np.array(child_candle_candidates)
        df['Color'] = np.array(candle_color)
        df['TP'] = np.array(child_candle_trigger_price)
        df['Signal'] = np.array(child_candle_direction)
        df['SL'] = np.array(child_candle_sl)
        df['Target'] = np.array(child_candle_target)
        return DF.merge(df.loc[:, [date, 'IsParent', 'IsChild', 'Color',\
                                   'TP', 'Signal', 'SL', 'Target']], how = "outer", on = date)
        
    def buy(DF, fast_ema_col_name, slow_ema_col_name, diff_price_fast_ema, diff_fast_slow_ema):
        helper = add_stats_helper()
        df = DF.copy()
        df.reset_index(inplace = True)
        close_price_series = df[close_price]
        fast_ema_series = df[fast_ema_col_name]
        slow_ema_series = df[slow_ema_col_name]
        rsi_series = df[rsi]
        open_price_series = df[open_price]
        
        # First check based on close price and populate 'BuyCP' column
        buy_cp = []
        for i in range(0, len(close_price_series)):
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
        df.reset_index(inplace = True)
        close_price_series = df[close_price]
        fast_ema_series = df[fast_ema_col_name]
        slow_ema_series = df[slow_ema_col_name]
        rsi_series = df[rsi]
        open_price_series = df[open_price]
        
        # First check based on close price and populate 'BuyCP' column
        sell_cp = []
        for i in range(0, len(close_price_series)):
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
    
    