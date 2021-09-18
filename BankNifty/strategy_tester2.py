#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 13:59:12 2021

@author: nishant.gupta
"""

import pandas as pd

from add_stats import add_stats
from data_reader import data_reader 
from util import util

fast_ema = 80
slow_ema = 240
diff_price_fast_ema = 600
diff_fast_slow_ema = 500

#target = 10
sl_orig = 80
sl = sl_orig
lot_size = 25
num_lots = 1
time_to_start_trade = '09:14:00'
cut_off_time_to_start = '14:30:00'
cut_off_time_to_close = '15:00:00'

# Dynamic parameters
max_loss_per_lot = 110
max_gain_per_lot = 2000
max_trades_per_day = 10
max_hold_period_in_minutes = 2


one_minute_data = data_reader.read("NIFTYBANK_SIX_YEAR_1_MINUTE_DATA.xlsx")
five_minute_data = data_reader.read("NIFTYBANK_SIX_YEAR_5_MINUTE_DATA.xlsx")
#five_minute_data = one_minute_data.iloc[::5]

five_minute_data = add_stats.ema(five_minute_data, fast_ema)
five_minute_data.drop_duplicates(keep = 'first', inplace = True)

five_minute_data = add_stats.ema(five_minute_data, slow_ema)
five_minute_data.drop_duplicates(keep = 'first', inplace = True)

five_minute_data = add_stats.rsi(five_minute_data, 14)
five_minute_data.drop_duplicates(keep = 'first', inplace = True)

five_minute_data = add_stats.buy(five_minute_data, "EMA" + str(fast_ema), "EMA" + str(slow_ema),\
                                 diff_price_fast_ema, diff_fast_slow_ema)
five_minute_data.drop_duplicates(keep = 'first', inplace = True)
    
five_minute_data = add_stats.sell(five_minute_data, "EMA" + str(fast_ema), "EMA" + str(slow_ema),\
                                  diff_price_fast_ema, diff_fast_slow_ema)
five_minute_data.drop_duplicates(keep = 'first', inplace = True)

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
    
for date, open_price in one_minute_dict['Open'].items():
    one_min_high_low_dict[date]['Open'] = open_price
    
five_minute_dict = five_minute_data.to_dict()
five_minute_open_signal_dict = {}
for date, open_price in five_minute_dict['Open'].items():
    five_minute_open_signal_dict[date] = {}
    five_minute_open_signal_dict[date]['Open'] = open_price
    
for date, low in five_minute_dict['Low'].items():
    five_minute_open_signal_dict[date]['Low'] = low
    
for date, high in five_minute_dict['High'].items():
    five_minute_open_signal_dict[date]['High'] = high
    
for date, buy_signal in five_minute_dict['BuySignal'].items():
    five_minute_open_signal_dict[date]['BuySignal'] = buy_signal

for date, sell_signal in five_minute_dict['SellSignal'].items():
    five_minute_open_signal_dict[date]['SellSignal'] = sell_signal
    
for date, rsi in five_minute_dict['RSI'].items():
    five_minute_open_signal_dict[date]['RSI'] = rsi

last_transaction_date = ''
total_pl = 0
total_pnl_excluding_taxes = 0
open_trade = False
pl_dict = {}
pl_dict_yearly = {}
num_trades_yearly = {}
num_trades_per_day_dict = {}
num_trades = 0
transactions = []

prev_high = 0
prev_low = 0
exit_signal_buy = 'Open'
exit_signal_sell = 'Open'

prev_date = ''
for transaction_date, value_five_min in five_minute_open_signal_dict.items():
    if (value_five_min['BuySignal'] == True and prev_low != 0):
        if (util.get_time(transaction_date) > time_to_start_trade and \
            transaction_date > last_transaction_date and open_trade == False and \
            util.get_time(transaction_date) < cut_off_time_to_start):
            if (util.check_if_val_within_limit(pl_dict, util.get_date(transaction_date),\
                                               max_gain_per_lot, max_loss_per_lot) and\
                util.check_if_trades_limit_not_reached(num_trades_per_day_dict,\
                                                       util.get_date(transaction_date),\
                                                       max_trades_per_day)):
                util.add_or_update_val_to_key(num_trades_per_day_dict,\
                                              util.get_date(transaction_date), 1)

                current_hold_period = 0
                num_trades += 1
                open_trade = True
                buy_date = transaction_date
                buy_price = value_five_min['Open']
                
                if buy_price >= prev_low:
                    sl = buy_price - prev_low
                else:
                    sl = 0
                
                sl = min(sl, sl_orig)
                print("Buy trade initiated at: ", buy_date, " Price: ", buy_price)
                buy_time = util.get_time(buy_date)
                target = -10000
                for sell_date, value in one_min_high_low_dict.items():
                   current_pnl = 0
                   current_pnl_excluding_taxes = 0
                   if (sell_date > buy_date):
                       # # Setting the target to be high of the next candle on 1 min chart.
                       # if (current_hold_period <= max_hold_period_in_minutes):
                       #     # We set the target to be min of low of all the candles in the holding period.
                       #     target = max(target, value['High'])
                       target = 30000
                       current_hold_period += 1
                       # print("Target is: ", target)
                       sell_price = 0
                       # Take care of SL first.
                       if (buy_price - value['Low'] >= sl):
                           print("SL hit. Sold at: ", sell_date, " Price: ", value['Low'])
                           current_pnl = (util.get_pnl(buy_price, buy_price - sl, num_lots, lot_size) /\
                                          (lot_size * num_lots))
                           current_pnl_excluding_taxes = -sl
                           sell_price = buy_price - sl
                           open_trade = False
                    
                       # Auto square off if we are past cutoff time.
                       if (open_trade == True and util.get_time(sell_date) > cut_off_time_to_close):
                           print("Auto squareoff. Sell date: ", sell_date, " Price: ",\
                                 value[exit_signal_buy])
                           current_pnl = (util.get_pnl(buy_price, value[exit_signal_buy], num_lots,\
                                                       lot_size) /\
                                          (lot_size * num_lots))
                           current_pnl_excluding_taxes = value[exit_signal_buy] - buy_price
                           sell_price = value[exit_signal_buy]
                           open_trade = False
                       
                       if (open_trade == True and current_hold_period > max_hold_period_in_minutes and \
                           value[exit_signal_buy] - buy_price >= target):
                           #or current_hold_period >= max_hold_period_in_minutes):
                           print("Trade ended. Sold at: ", sell_date, " Price: ", value[exit_signal_buy])
                           current_pnl = (util.get_pnl(buy_price, value[exit_signal_buy], num_lots,\
                                                       lot_size) /\
                                          (lot_size * num_lots))
                           current_pnl_excluding_taxes = value[exit_signal_buy] - buy_price
                           sell_price = value[exit_signal_buy]
                           open_trade = False
                   
    
                       if open_trade == False:
                           last_transaction_date = sell_date
                           print("Logging pnl: ", current_pnl, " for day: ", util.get_date(buy_date))
                           util.add_or_update_val_to_key(pl_dict, util.get_date(buy_date),\
                                                         current_pnl)
                           dict_key = buy_date.split('-')[0] + '-' + buy_date.split('-')[1]
                           util.add_or_update_val_to_key(pl_dict_yearly, dict_key, current_pnl)
                           total_pl += current_pnl
                           total_pnl_excluding_taxes += current_pnl_excluding_taxes
                           row = {'Transaction':"Buy", 'StartTS':buy_date, 'Start Price': buy_price,\
                                  'EndTS':sell_date, 'End Price': sell_price, 'Pnl_taxed':current_pnl,\
                                  'Pnl_untaxed':current_pnl_excluding_taxes, 'RSI':value_five_min['RSI']}
                           transactions.append(row)
                           break
            else:
                print("Daily limit reached for: ", util.get_date(transaction_date), " Pnl: ",\
                      pl_dict[util.get_date(transaction_date)])
                
    elif (value_five_min['SellSignal'] == True and prev_high != 0):
        if (util.get_time(transaction_date) > time_to_start_trade and\
            transaction_date > last_transaction_date and open_trade == False and \
            util.get_time(transaction_date) < cut_off_time_to_start):
            if (util.check_if_val_within_limit(pl_dict, util.get_date(transaction_date),\
                                               max_gain_per_lot, max_loss_per_lot) and\
                util.check_if_trades_limit_not_reached(num_trades_per_day_dict,\
                                                       util.get_date(transaction_date),\
                                                       max_trades_per_day)):
                util.add_or_update_val_to_key(num_trades_per_day_dict,\
                                              util.get_date(transaction_date), 1)
                current_hold_period = 0
                num_trades += 1
                open_trade = True
                sell_date = transaction_date
                sell_price = value_five_min['Open']
                if prev_high >= sell_price:
                    sl = prev_high - sell_price
                else:
                    sl = 0
                
                target = 100000

                sl = min(sl, sl_orig)
                print("Sell trade initiated at: ", sell_date, " Price: ", sell_price)
                sell_time = util.get_time(sell_date)
                for buy_date, value in one_min_high_low_dict.items():
                   current_pnl = 0
                   if (buy_date > sell_date):
                       # # Setting the target to be high of the next candle on 1 min chart.
                       # if (current_hold_period <= max_hold_period_in_minutes):
                       #     # We set the target to be min of low of all the candles in the holding period.
                       #     target = min(target, value['Low'])
                       target = 30000
                       current_hold_period += 1
                       # print("Target is: ", target)
                       
                       # Take care of SL first.
                       if (value['High'] - sell_price >= sl):
                           buy_price = value['High']
                           print("SL hit. Buy at: ", buy_date, " Price: ", value['High'])
                           current_pnl = (util.get_pnl(sell_price + sl, sell_price, num_lots, lot_size) /\
                                          (lot_size * num_lots))
                           current_pnl_excluding_taxes = -sl
                           open_trade = False
                    
                       # Auto square off if we are past cutoff time.
                       if (open_trade == True and util.get_time(buy_date) > cut_off_time_to_close):
                           print("Auto squareoff. Buy date: ", buy_date, " Price: ",\
                                 value[exit_signal_sell])
                           current_pnl = (util.get_pnl(value[exit_signal_sell], sell_price, num_lots,\
                                                       lot_size) /\
                                          (lot_size * num_lots))
                           current_pnl_excluding_taxes = sell_price - value[exit_signal_sell]
                           buy_price = value[exit_signal_sell]
                           open_trade = False
                           
                       if (open_trade == True and current_hold_period > max_hold_period_in_minutes and\
                           sell_price - value[exit_signal_sell] >= target):
                           #or current_hold_period >= max_hold_period_in_minutes):
                           buy_price = value[exit_signal_sell]
                           print("Trade ended. Buy at: ", buy_date, " Price: ", value[exit_signal_sell])
                           current_pnl = (util.get_pnl(value[exit_signal_sell], sell_price, num_lots,\
                                                       lot_size) /\
                                          (lot_size * num_lots))
                           current_pnl_excluding_taxes = sell_price - value[exit_signal_sell]
                           open_trade = False

                       if open_trade == False:
                           last_transaction_date = buy_date
                           print("Logging pnl: ", current_pnl, " for day: ", util.get_date(sell_date))
                           util.add_or_update_val_to_key(pl_dict, util.get_date(sell_date),\
                                                         current_pnl)
                           dict_key = sell_date.split('-')[0] + '-' + sell_date.split('-')[1]
                           util.add_or_update_val_to_key(pl_dict_yearly, dict_key, current_pnl)
                           total_pl += current_pnl
                           total_pnl_excluding_taxes += current_pnl_excluding_taxes
                           row = {'Transaction':"Sell", 'StartTS':sell_date, 'Start Price': sell_price,\
                                  'EndTS':buy_date, 'End Price': buy_price, 'Pnl_taxed':current_pnl,\
                                  'Pnl_untaxed':current_pnl_excluding_taxes, 'RSI':value_five_min['RSI']}
                           transactions.append(row)
                           total_pl += current_pnl
                           total_pnl_excluding_taxes += current_pnl_excluding_taxes
                           break
            else:
                print("Daily limit reached for: ", util.get_date(transaction_date), " Pnl: ",\
                      pl_dict[util.get_date(transaction_date)])
                    
    prev_high = value_five_min['High']
    prev_low = value_five_min['Low']
                    
transaction_df = pd.DataFrame(transactions)
transaction_df.set_index('Transaction', inplace=True)
#transaction_df.to_excel("TRANSACTIONS_ONE_YEAR.xlsx")
