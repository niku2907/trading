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

target = -15
sl = 100
#max_profit_loss_per_day = 150
lot_size = 25
num_lots = 1
max_loss_per_lot = 150
max_gain_per_lot = 150
#max_profit_loss_per_day = max_pnl_per_lot * num_lots * lot_size

cut_off_time_to_start = '14:30:00'
cut_off_time_to_close = '15:00:00'


one_minute_data = data_reader.read("NIFTYBANK_SIXTEEN_YEAR_DATA.xlsx")
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
total_pnl_excluding_taxes = 0
open_trade = False
pl_dict = {}
pl_dict_yearly = {}
num_trades_yearly = {}
num_trades = 0
transactions = []
for transaction_date, value in five_minute_open_signal_dict.items():
    if (value['BuySignal'] == True):
        if (transaction_date > last_transaction_date and open_trade == False and \
            util.get_time(transaction_date) < cut_off_time_to_start):
            if (util.check_if_val_within_limit(pl_dict, util.get_date(transaction_date),\
                                               max_gain_per_lot, max_loss_per_lot)):
                num_trades += 1
                open_trade = True
                buy_date = transaction_date
                buy_price = value['Open']
                print("Buy trade initiated at: ", buy_date, " Price: ", buy_price)
                buy_time = util.get_time(buy_date)
                for sell_date, value in one_min_high_low_dict.items():
                   current_pnl = 0
                   current_pnl_excluding_taxes = 0
                   if (sell_date > buy_date):
                       sell_price = 0
                       if (value['High'] >= buy_price + target):
                           print("Trade ended. Sold at: ", sell_date, " Price: ", value['High'])
                           current_pnl = (util.get_pnl(buy_price, value['High'], num_lots, lot_size) /\
                                          (lot_size * num_lots))
                           current_pnl_excluding_taxes = value['High'] - buy_price
                           sell_price = value['High']
                           open_trade = False
                   
                       if (buy_price - value['Low'] >= sl):
                           print("SL hit. Sold at: ", sell_date, " Price: ", value['Low'])
                           current_pnl = (util.get_pnl(buy_price, buy_price - sl, num_lots, lot_size) /\
                                          (lot_size * num_lots))
                           current_pnl_excluding_taxes = -sl
                           sell_price = buy_price - sl
                           open_trade = False
                    
                       # Auto square off if we are past cutoff time.
                       if (util.get_time(sell_date) > cut_off_time_to_close):
                           print("Auto squareoff. Sell date: ", sell_date, " Price: ", value['High'])
                           current_pnl = (util.get_pnl(buy_price, value['High'], num_lots, lot_size) /\
                                          (lot_size * num_lots))
                           current_pnl_excluding_taxes = value['High'] - buy_price
                           sell_price = value['High']
                           open_trade = False
    
                       if open_trade == False:
                           last_transaction_date = sell_date
                           print("Logging pnl: ", current_pnl, " for day: ", util.get_date(buy_date))
                           util.add_or_update_val_to_key(pl_dict, util.get_date(buy_date),\
                                                         current_pnl_excluding_taxes)
                           dict_key = buy_date.split('-')[0] + '-' + buy_date.split('-')[1]
                           util.add_or_update_val_to_key(pl_dict_yearly, dict_key, current_pnl)
                           total_pl += current_pnl
                           total_pnl_excluding_taxes += current_pnl_excluding_taxes
                           row = {'Transaction':"Buy", 'StartTS':buy_date, 'Start Price': buy_price,\
                                  'EndTS':sell_date, 'End Price': sell_price, 'Pnl_taxed':current_pnl,\
                                  'Pnl_untaxed':current_pnl_excluding_taxes}
                           transactions.append(row)
                           break
            else:
                print("Daily limit reached for: ", util.get_date(transaction_date), " Pnl: ",\
                      pl_dict[util.get_date(transaction_date)])
                
    elif (value['SellSignal'] == True):
        if (transaction_date > last_transaction_date and open_trade == False and \
            util.get_time(transaction_date) < cut_off_time_to_start):
            if (util.check_if_val_within_limit(pl_dict, util.get_date(transaction_date),\
                                               max_gain_per_lot, max_loss_per_lot)):
                num_trades += 1
                open_trade = True
                sell_date = transaction_date
                sell_price = value['Open']
                print("Sell trade initiated at: ", sell_date, " Price: ", sell_price)
                sell_time = util.get_time(sell_date)
                for buy_date, value in one_min_high_low_dict.items():
                   current_pnl = 0
                   if (buy_date > sell_date):
                       if (value['Low'] <= sell_price - target):
                           buy_price = value['Low']
                           print("Trade ended. Buy at: ", buy_date, " Price: ", value['Low'])
                           current_pnl = (util.get_pnl(value['Low'], sell_price, num_lots, lot_size) /\
                                          (lot_size * num_lots))
                           current_pnl_excluding_taxes = sell_price - value['Low']
                           open_trade = False
                   
                       if (value['High'] - sell_price >= sl):
                           buy_price = value['High']
                           print("SL hit. Buy at: ", buy_date, " Price: ", value['High'])
                           current_pnl = (util.get_pnl(sell_price + sl, sell_price, num_lots, lot_size) /\
                                          (lot_size * num_lots))
                           current_pnl_excluding_taxes = -sl
                           open_trade = False
                    
                       # Auto square off if we are past cutoff time.
                       if (util.get_time(buy_date) > cut_off_time_to_close):
                           print("Auto squareoff. Buy date: ", buy_date, " Price: ", value['Low'])
                           current_pnl = (util.get_pnl(value['Low'], sell_price, num_lots, lot_size) /\
                                          (lot_size * num_lots))
                           current_pnl_excluding_taxes = sell_price - value['Low']
                           buy_price = value['Low']
                           open_trade = False
    
                       if open_trade == False:
                           last_transaction_date = buy_date
                           print("Logging pnl: ", current_pnl, " for day: ", util.get_date(sell_date))
                           util.add_or_update_val_to_key(pl_dict, util.get_date(sell_date),\
                                                         current_pnl_excluding_taxes)
                           dict_key = sell_date.split('-')[0] + '-' + sell_date.split('-')[1]
                           util.add_or_update_val_to_key(pl_dict_yearly, dict_key, current_pnl)
                           total_pl += current_pnl
                           total_pnl_excluding_taxes += current_pnl_excluding_taxes
                           row = {'Transaction':"Sell", 'StartTS':sell_date, 'Start Price': sell_price,\
                                  'EndTS':buy_date, 'End Price': buy_price, 'Pnl_taxed':current_pnl,\
                                  'Pnl_untaxed':current_pnl_excluding_taxes}
                           transactions.append(row)
                           total_pl += current_pnl
                           total_pnl_excluding_taxes += current_pnl_excluding_taxes
                           break
            else:
                print("Daily limit reached for: ", util.get_date(transaction_date), " Pnl: ",\
                      pl_dict[util.get_date(transaction_date)])
                    
transaction_df = pd.DataFrame(transactions)
transaction_df.set_index('Transaction', inplace=True)
transaction_df.to_excel("TRANSACTIONS_SIXTEEN_YEAR.xlsx")
