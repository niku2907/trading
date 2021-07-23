#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 13:59:12 2021

@author: nishant.gupta
"""

from add_stats import add_stats

from data_reader import data_reader 

from util import util

fast_ema = 5
slow_ema = 25
diff_price_fast_ema = 600
diff_fast_slow_ema = 500

target = 15
sl = 15
max_profit_loss_per_day = 150

cut_off_time_to_start = '14:30:00'
cut_off_time_to_close = '15:00:00'


one_minute_data = data_reader.read("NIFTY_TWO_YEAR_DATA.xlsx")
five_minute_data = one_minute_data.iloc[::5]

five_minute_data = add_stats.ema(five_minute_data, fast_ema)
five_minute_data = add_stats.ema(five_minute_data, slow_ema)
five_minute_data = add_stats.rsi(five_minute_data, 14)
five_minute_data = add_stats.buy(five_minute_data, "EMA" + str(fast_ema), "EMA" + str(slow_ema),\
                                 diff_price_fast_ema, diff_fast_slow_ema)
five_minute_data = add_stats.sell(five_minute_data, "EMA" + str(fast_ema), "EMA" + str(slow_ema),\
                                  diff_price_fast_ema, diff_fast_slow_ema)

one_minute_data.set_index('Date', inplace=True)
one_minute_data.dropna(inplace = True)

five_minute_data.set_index('Date', inplace=True)
five_minute_data.dropna(inplace = True)



#fifteen_minute_data = one_minute_data.iloc[::15]

#one_minute_list = one_minute_data.values.tolist()
#five_minute_list = five_minute_data.values.tolist()

one_min_high_low_dict = {}
one_minute_dict = one_minute_data.to_dict()
for date, high_price in one_minute_dict['High'].items():
    one_min_high_low_dict[date] = {}
    one_min_high_low_dict[date]['High'] = high_price
    
for date, low_price in one_minute_dict['Low'].items():
    one_min_high_low_dict[date]['Low'] = low_price
    
five_minute_dict = five_minute_data.to_dict()
five_minute_open_signal_dict = {}
for date, open_price in five_minute_dict['Open'].items():
    five_minute_open_signal_dict[date] = {}
    five_minute_open_signal_dict[date]['Open'] = open_price
    
for date, buy_signal in five_minute_dict['BuySignal'].items():
    five_minute_open_signal_dict[date]['BuySignal'] = buy_signal

for date, sell_signal in five_minute_dict['SellSignal'].items():
    five_minute_open_signal_dict[date]['SellSignal'] = sell_signal


last_transaction_date = ''
total_pl = 0
open_trade = False
pl_dict = {}
for transaction_date, value in five_minute_open_signal_dict.items():
    if (value['BuySignal'] == True):
        if (transaction_date > last_transaction_date and open_trade == False and \
            util.get_time(transaction_date) < cut_off_time_to_start):
            if (util.check_if_val_within_limit(pl_dict, util.get_date(transaction_date),\
                                               max_profit_loss_per_day)):
                open_trade = True
                buy_date = transaction_date
                buy_price = value['Open']
                print("Buy trade initiated at: ", buy_date, " Price: ", buy_price)
                buy_time = util.get_time(buy_date)
                for sell_date, value in one_min_high_low_dict.items():
                   current_pnl = 0
                   if (sell_date > buy_date):
                       if (value['High'] >= buy_price + target):
                           print("Trade ended. Sold at: ", sell_date, " Price: ", value['High'])
                           current_pnl = value['High'] - buy_price
                           open_trade = False
                   
                       if (buy_price - value['Low'] >= sl):
                           print("SL hit. Sold at: ", sell_date, " Price: ", value['Low'])
                           current_pnl = -sl
                           open_trade = False
                    
                       # Auto square off if we are past cutoff time.
                       if (util.get_time(sell_date) > cut_off_time_to_close):
                           print("Auto squareoff. Sell date: ", sell_date, " Price: ", value['High'])
                           current_pnl = value['High'] - buy_price
                           open_trade = False
    
                       if open_trade == False:
                           last_transaction_date = sell_date
                           print("Logging pnl: ", current_pnl, " for day: ", util.get_date(buy_date))
                           util.add_or_update_val_to_key(pl_dict, util.get_date(buy_date), current_pnl)
                           total_pl += current_pnl
                           break
            else:
                print("Daily limit reached for: ", util.get_date(transaction_date), " Pnl: ",\
                      pl_dict[util.get_date(transaction_date)])
                
    elif (value['SellSignal'] == True):
        if (transaction_date > last_transaction_date and open_trade == False and \
            util.get_time(transaction_date) < cut_off_time_to_start):
            if (util.check_if_val_within_limit(pl_dict, util.get_date(transaction_date),\
                                               max_profit_loss_per_day)):
                open_trade = True
                sell_date = transaction_date
                sell_price = value['Open']
                print("Sell trade initiated at: ", sell_date, " Price: ", sell_price)
                sell_time = util.get_time(sell_date)
                for buy_date, value in one_min_high_low_dict.items():
                   current_pnl = 0
                   if (buy_date > sell_date):
                       if (value['Low'] <= sell_price - target):
                           print("Trade ended. Buy at: ", buy_date, " Price: ", value['Low'])
                           current_pnl = sell_price - value['Low']
                           open_trade = False
                   
                       if (value['High'] - sell_price >= sl):
                           print("SL hit. Buy at: ", buy_date, " Price: ", value['High'])
                           current_pnl = -sl
                           open_trade = False
                    
                       # Auto square off if we are past cutoff time.
                       if (util.get_time(buy_date) > cut_off_time_to_close):
                           print("Auto squareoff. Buy date: ", buy_date, " Price: ", value['Low'])
                           current_pnl = sell_price - value['Low']
                           open_trade = False
    
                       if open_trade == False:
                           last_transaction_date = buy_date
                           print("Logging pnl: ", current_pnl, " for day: ", util.get_date(sell_date))
                           util.add_or_update_val_to_key(pl_dict, util.get_date(sell_date), current_pnl)
                           total_pl += current_pnl
                           break
            else:
                print("Daily limit reached for: ", util.get_date(transaction_date), " Pnl: ",\
                      pl_dict[util.get_date(transaction_date)])