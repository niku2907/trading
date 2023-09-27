# -*- coding: utf-8 -*-
"""
Created on Tue May 30 23:11:08 2023

@author: NishantGupta
"""

import math

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
    
class traffic_light_strategy_util_v2:
    # Start time of the day.
    start_time = '09:15:00'
    
    # Open price of the cutoff time.
    cut_off_time_to_start = '14:15:00'
    
    # Close price of the cutoff time.
    cut_off_time_to_close = '15:15:00'
    
    is_open_pos_buy = 0
    is_open_pos_sell = 0
    buy_time = ""
    sell_time = ""
    pos_buy_price = 0
    pos_sell_price = 0
    total_pnl = 0
    sl_price = 0
    target_price = 0
    decrease_sl_trigger_price = 0
    max_sl_pct = 3.2
    max_trades_per_day = 4
    cash_out_factor = 0.02
    monthly_target = 0.5
    cash_out_limit = 10000000
    
    max_buy_sl = 200
    max_sell_sl = 200
    
    rr_ratio = 4.5
    execution_error_margin_ticks = 10
    sl_buffer = 20
    buy_sl_pct = 5
    sell_sl_pct = 5
        
    def __init__(self, data, start_capital, price_per_lot, lot_size,\
                 buy_allowed, sell_allowed, cash_out_limit):
        self.buy_price_list = []
        self.sell_price_list = []
        self.buy_time_list = []
        self.sell_time_list = []
        self.pos_type_list = []
        self.pnl_list = []
        self.pct_pnl_list = []
        self.total_pct_pnl_list = []
        self.exit_method_list = []
        self.num_units_list = []
        self.current_capital_list = []
        self.target_price_list = []
        self.data = data
        self.status_list = ['NA' for i in range(len(data))]
        self.signal_list = ['NA' for i in range(len(data))]
        self.initial_capital = start_capital
        self.current_capital = start_capital
        self.last_trade_ctr = -1
        self.dynamic_sl = 1
        self.alert_candle_encountered = 0
        self.start_limit_price_based_on_alert_candle = -1
        self.sl_price_based_on_alert_candle = -1
        
        self.high_limit_price_based_on_alert_candle = -1
        self.low_limit_price_based_on_alert_candle = -1
        self.sl_price_based_on_alert_candle_for_long = -1
        self.sl_price_based_on_alert_candle_for_short = -1
        
        self.cash_out_limit = cash_out_limit
        self.buy_allowed = buy_allowed
        self.sell_allowed = sell_allowed
        self.num_sells = 0
        self.num_sell_wins = 0
        self.num_buys = 0
        self.num_buy_wins = 0
        self.reserves = 0
        self.sl_points = 0
        self.target_points = 0
        self.distance_from_ema = 0
        self.start_date = "2019-01-01"
        self.start_date = ""
        self.end_date = "2019-12-31"
        self.end_date = ""
        
        
        self.num_trades_per_day_dict = {}
        self.pnl_per_day_dict = {}
        self.pnl_per_day_of_month_dict = {}
        self.num_target_sell_per_month = {}
        self.monthly_cash_out_stats_dict = {}
        
        self.high_price_daily_dict = {}
        self.high_price_daily_ts_dict = {}
        self.monthly_pnl_dict = {}
        self.monthly_start_capital_dict = {}

        
        # Each entry is a tuple of three integers.
        # 0 -> Target BUY
        # 1 -> SL BUY
        # 2 -> Cutoff BUY
        self.monthly_pos_exit_stats_dict_sell = {}
        
        # Each entry is a tuple of three integers.
        # 0 -> Target SELL
        # 1 -> SL SELL
        # 2 -> Cutoff SELL
        self.monthly_pos_exit_stats_dict_buy = {}
        
        # This is a snapshot of monthly_pos_exit_stats_dict on a particular day
        # 0 -> Target SELL
        # 1 -> SL SELL
        # 2 -> Cutoff SELL
        # 3 -> Running ROI of the current month
        self.daily_pos_exit_stats_dict_buy = {}
        
        # This is a snapshot of monthly_pos_exit_stats_dict on a particular day
        # 0 -> Target 
        # 1 -> SL BUY
        # 2 -> Cutoff BUY
        # 3 -> Running ROI of the current month
        self.daily_pos_exit_stats_dict_sell = {}
        
        self.date_encountered_dict = {}
        
        self.red_candle = CandleMetadata("-", -1, -1, -1, -1)
        self.green_candle = CandleMetadata("-", -1, -1, -1, -1)
        self.red_candle_encountered = 0
        self.green_candle_encountered = 0
        
        self.price_per_lot = price_per_lot
        if self.price_per_lot == -1:
            print("Unsupported entity encountered.")
            return
            
        self.lot_size = lot_size
        
        self.pos_buy_price = -1
        self.buy_time = ""
        self.pos_sell_price = -1
        self.sell_time = ""
        self.num_units = -1
        self.target_price = -1
        self.sl_price = -1
        
    def initialize(self, current_date_time, prev_date):
        current_date = util.get_date(current_date_time)
        month_year = util.get_month_year(current_date)
        current_month = month_year
        prev_month = "" 
        if prev_date != "":
            prev_month = util.get_month_year(prev_date)
        
        # Initialize
        if (self.monthly_pnl_dict.__contains__(current_month) == 0):
            self.monthly_pnl_dict[month_year] = 0
            
        if (self.monthly_start_capital_dict.__contains__(month_year) == 0):
            self.monthly_start_capital_dict[month_year] = self.current_capital
            
        if (self.monthly_cash_out_stats_dict.__contains__(month_year) == 0):
            self.monthly_cash_out_stats_dict[month_year] = 0

        
        if (self.monthly_pos_exit_stats_dict_buy.__contains__(month_year) == 0):
            self.monthly_pos_exit_stats_dict_buy[month_year] = [0, 0, 0]
            
        if (self.monthly_pos_exit_stats_dict_sell.__contains__(month_year) == 0):
            self.monthly_pos_exit_stats_dict_sell[month_year] = [0, 0, 0]

        if (self.daily_pos_exit_stats_dict_buy.__contains__(current_date) == 0):
            if (current_month == prev_month and\
                    self.daily_pos_exit_stats_dict_buy.__contains__(prev_date) == 1):
                self.daily_pos_exit_stats_dict_buy[current_date] = \
                    self.daily_pos_exit_stats_dict_buy[prev_date].copy()
            else:
                self.daily_pos_exit_stats_dict_buy[current_date] = [-1, -1, -1, -100.0]  
                
        if (self.daily_pos_exit_stats_dict_sell.__contains__(current_date) == 0):
            if (current_month == prev_month and\
                    self.daily_pos_exit_stats_dict_sell.__contains__(prev_date) == 1):
                self.daily_pos_exit_stats_dict_sell[current_date] = \
                    self.daily_pos_exit_stats_dict_sell[prev_date].copy()
            else:
                self.daily_pos_exit_stats_dict_sell[current_date] = [-1, -1, -1, -100.0]
        
    
    def cash_out(self, current_date_time):
        month_year = util.get_month_year(current_date_time)
        if (self.current_capital > self.cash_out_limit):
            if (self.monthly_cash_out_stats_dict.__contains__(month_year) == 0):
                self.monthly_cash_out_stats_dict[month_year] = 0
                
            self.monthly_cash_out_stats_dict[month_year] +=\
                self.cash_out_factor * self.cash_out_limit
            self.reserves += self.cash_out_factor * self.cash_out_limit
            self.current_capital -= self.cash_out_factor * self.cash_out_limit
            
    def update_high_price(self, current_date_time, current_high_price):
        if (self.high_price_daily_dict.get(util.get_date(current_date_time) == None)):
            print("Inserting key: " + str(util.get_date(current_date_time)))
            self.high_price_daily_dict[util.get_date(current_date_time)] =\
                current_high_price
            self.high_price_daily_ts_dict[util.get_date(current_date_time)] = current_date_time
        else:
            print("Contains key: " + str(util.get_date(current_date_time)))
            if (self.high_price_daily_dict[util.get_date(current_date_time)] < current_high_price):
                self.high_price_daily_ts_dict[util.get_date(current_date_time)] = current_date_time
            self.high_price_daily_dict[util.get_date(current_date_time)] =\
                max(self.high_price_daily_dict[util.get_date(current_date_time)],
                    current_high_price)

        high_price_current_date = self.high_price_daily_dict[util.get_date(current_date_time)]
        high_price_current_date_ts = self.high_price_daily_ts_dict[util.get_date(current_date_time)]
        return high_price_current_date, high_price_current_date_ts
    
    def reset_all_state_data(self):
        self.alert_candle_encountered = 0
        self.red_candle_encountered = 0
        self.green_candle_encountered = 0
        self.high_limit_price_based_on_alert_candle = -1
        self.low_limit_price_based_on_alert_candle = -1
        self.sl_price_based_on_alert_candle_for_long = -1
        self.sl_price_based_on_alert_candle_for_short = -1
        self.red_candle = CandleMetadata("-", -1, -1, -1, -1)
        self.green_candle = CandleMetadata("-", -1, -1, -1, -1)
        self.is_open_pos_buy = 0
        self.is_open_pos_sell = 0
        self.pos_buy_price = -1
        self.pos_sell_price = -1
        self.buy_time = ""
        self.sell_time = ""
        self.target_price = ""
        self.sl_price = ""
        

    def get_pnl(self):
        message = "Profit of: " + str(self.pos_sell_price - self.pos_buy_price) + " per unit"
        if (self.pos_buy_price > self.pos_sell_price):
            message = "Loss of: " + str(self.pos_buy_price - self.pos_sell_price) + " per unit"
        
        traffic_light_strategy_util_v2.print_debug_log(message, 1)
        return traffic_light_strategy_util_v2.get_pnl_including_taxes(self.pos_buy_price,\
                                                                   self.pos_sell_price, 1,\
                                                                   self.num_units)
    
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
    
   
    def update_transaction_record(self, pos_type, exit_method):
        current_pnl = self.get_pnl()
        self.buy_price_list.append(self.pos_buy_price)
        self.sell_price_list.append(self.pos_sell_price)
        self.buy_time_list.append(self.buy_time)
        self.sell_time_list.append(self.sell_time)
        self.pos_type_list.append(pos_type)
        self.pnl_list.append(current_pnl)
        num_lots = self.num_units / self.lot_size
        if num_lots == 0:
            print("Num units: " + str(self.num_units) + " lot size: " + str(self.lot_size))
        
        self.pct_pnl_list.append(100 * (current_pnl / (self.price_per_lot * num_lots)))
            
        self.total_pct_pnl_list.append(100 * (current_pnl /\
                                              (self.current_capital - current_pnl)))
        self.exit_method_list.append(exit_method)
        self.num_units_list.append(self.num_units)
        self.current_capital_list.append(self.current_capital)
        self.target_price_list.append(self.target_price)
    
    def update_wins_data(self, pos_type, pnl):
        if (pnl > 0):
            if (pos_type == "BUY"):
                self.num_buy_wins += 1
            elif (pos_type == "SELL"):
                self.num_sell_wins += 1
            
    def update_daily_pos_exit_stats(self, pos_type, current_date,\
                                    update_field, update_value):
        if pos_type == "BUY":
            self.daily_pos_exit_stats_dict_buy[current_date][update_field] = update_value
        elif pos_type == "SELL":
            self.daily_pos_exit_stats_dict_sell[current_date][update_field] = update_value
        else:
            print("Unsupported posititon type encountered.")
        # daily_val = ' '.join([str(elem) for i,elem in\
        #                       enumerate(self.daily_pos_exit_stats_dict[current_date])])  
    
    def squareoff_and_update_stats(self, pos_type, exit_method, current_date_time,\
                                   day, monthly_pos_exit_stats_dict,\
                                   index_in_monthly_pos_exit_dict):
        current_date = util.get_date(current_date_time)
        month_year = util.get_month_year(current_date_time)
        monthly_pos_exit_stats_dict[month_year][index_in_monthly_pos_exit_dict] += 1
        self.update_daily_pos_exit_stats(pos_type, current_date,\
                                         index_in_monthly_pos_exit_dict,\
                                         monthly_pos_exit_stats_dict[month_year][index_in_monthly_pos_exit_dict])                    
        
        current_pnl = self.get_pnl()
        self.update_wins_data(pos_type, current_pnl)
        self.total_pnl += current_pnl
        self.current_capital += current_pnl
        self.update_transaction_record(pos_type, exit_method)
        ctr = 1
        if (current_pnl < 0):
            ctr = -1
            
        # TODO: Create enum for these indexes
        if (self.pnl_per_day_of_month_dict.__contains__(day) == False):
            self.pnl_per_day_of_month_dict[day] = [0, 0, 0, 0]
        
        self.pnl_per_day_of_month_dict[day][0] += ctr
        if (ctr > 0):
            self.pnl_per_day_of_month_dict[day][1] += ctr
        else:
            self.pnl_per_day_of_month_dict[day][2] += ctr
        
        self.pnl_per_day_of_month_dict[day][3] += current_pnl
        
        self.monthly_pnl_dict[month_year] += current_pnl
        if ((self.monthly_pnl_dict[month_year] +\
             self.monthly_cash_out_stats_dict[month_year]) /
            self.monthly_start_capital_dict[month_year] > self.monthly_target):
            target_achieved_for_month = 1
        else:
            target_achieved_for_month = 0
            
        daily_roi = 100 * (self.current_capital + self.monthly_cash_out_stats_dict[month_year] - \
            self.monthly_start_capital_dict[month_year]) / self.monthly_start_capital_dict[month_year]
        self.update_daily_pos_exit_stats(pos_type, current_date,\
                                         3,\
                                         # 3 is the index of the ROI field in the dict
                                         daily_roi)   
            
    def squareoff_sell_position_beyond_cutoff(self, buy_price, current_date_time, current_index):
        i = current_index
        pos_type = "SELL"
        exit_method = "CUTOFF_BUY"

        self.pos_buy_price = buy_price
        self.is_open_pos_sell = 0
        self.status_list[i] = exit_method
        self.buy_time = current_date_time
        
        day = util.get_day_of_month(util.get_date(self.buy_time))
        
        message = "Autosquare off initiated. Buy price: " + str(self.pos_buy_price)
        traffic_light_strategy_util_v2.print_debug_log(message, 0)
        self.squareoff_and_update_stats(pos_type, exit_method, current_date_time, day,\
                                        self.monthly_pos_exit_stats_dict_sell,\
                                        ExitMethod[exit_method].value)
        
        
    def squareoff_buy_position_beyond_cutoff(self, sell_price, current_date_time, current_index):
        i = current_index
        pos_type = "BUY"
        exit_method = "CUTOFF_SELL"
        
        self.sell_time = current_date_time
        self.pos_sell_price = sell_price
        self.is_open_pos_buy = 0
        self.status_list[i] = exit_method
        
        day = util.get_day_of_month(util.get_date(self.sell_time))
        
        message = "Autosquare off initiated. Sell price: " + str(self.pos_sell_price)
        traffic_light_strategy_util_v2.print_debug_log(message, 0)
        self.squareoff_and_update_stats(pos_type, exit_method, current_date_time, day,\
                                        self.monthly_pos_exit_stats_dict_buy,\
                                        ExitMethodForBuy[exit_method].value)
        
        
            
    def maybe_squareoff_if_beyond_cutoff_time(self, current_date_time, current_index):
        i = current_index
        current_time = util.get_time(current_date_time)
        if current_time < self.cut_off_time_to_close:
            return False
        if self.is_open_pos_buy == 0 and self.is_open_pos_sell == 0:
            return True
        
        open_prices = self.data['Open']
        if self.is_open_pos_buy == 1:
            self.squareoff_buy_position_beyond_cutoff(open_prices[i],\
                                                      current_date_time,\
                                                      current_index)
        else :
            self.squareoff_sell_position_beyond_cutoff(open_prices[i],\
                                                       current_date_time,\
                                                       current_index)

        self.reset_all_state_data()
        return True
    
    def maybe_squareoff_buy_position(self, current_date_time, current_index):
        current_date = util.get_date(current_date_time)
        i = current_index
        can_close_pos = 0
        exit_method = ""
        month_year = util.get_month_year(current_date_time)
        low_prices = self.data['Low']
        high_prices = self.data['High']
        open_prices = self.data['Open']
        pos_type = "BUY"
        
        # Check if SL hit.
        if (low_prices[i] <= self.sl_price):
            #self.pos_sell_price = self.sl_price
            self.pos_sell_price = min(open_prices[i], self.sl_price)
            message = "[SL] Closing position. Time: " + str(current_date_time) + " Sell Price: " +\
                str(self.pos_sell_price) + " Buy Price: " + str(self.pos_buy_price)
            traffic_light_strategy_util_v2.print_debug_log(message, 1)
            can_close_pos = 1
            exit_method = "SL_SELL"
            self.status_list[i] = exit_method
            
            self.monthly_pos_exit_stats_dict_buy[month_year][ExitMethodForBuy[exit_method].value] += 1
            self.update_daily_pos_exit_stats(pos_type, current_date,\
                                             ExitMethodForBuy[exit_method].value,\
                                             self.monthly_pos_exit_stats_dict_buy[month_year][ExitMethodForBuy[exit_method].value])
        elif (high_prices[i] > self.target_price):
            self.pos_sell_price = self.target_price
            message = "[Target] Closing position. Time: " + str(current_date_time) + " Sell Price: " +\
                str(self.pos_sell_price) + " Buy Price: " + str(self.pos_buy_price)
            traffic_light_strategy_util_v2.print_debug_log(message, 1)
            can_close_pos = 1
            exit_method = "TARGET_SELL"
            self.status_list[i] = exit_method
            
            self.monthly_pos_exit_stats_dict_buy[month_year][ExitMethodForBuy[exit_method].value] += 1
            self.update_daily_pos_exit_stats(pos_type, current_date,\
                                             ExitMethodForBuy[exit_method].value,\
                                             self.monthly_pos_exit_stats_dict_buy[month_year][ExitMethodForBuy[exit_method].value])

        if can_close_pos == 0:
            return False
        
        self.sell_time = current_date_time        
        
        current_pnl = self.get_pnl()
        self.update_wins_data(pos_type, current_pnl)
        self.total_pnl += current_pnl
        self.current_capital += current_pnl
        self.update_transaction_record(pos_type, exit_method)
            
        util.add_or_update_val_to_key(self.pnl_per_day_dict, util.get_date(current_date_time),\
                                      current_pnl)
        ctr = 1
        if (current_pnl < 0):
            ctr = -1
        day = util.get_day_of_month(util.get_date(self.sell_time))
        if (self.pnl_per_day_of_month_dict.__contains__(day) == False):
            self.pnl_per_day_of_month_dict[day] = [0, 0, 0, 0]
        
        self.pnl_per_day_of_month_dict[day][0] += ctr
        if (ctr > 0):
            self.pnl_per_day_of_month_dict[day][1] += ctr
        else:
            self.pnl_per_day_of_month_dict[day][2] += ctr
        
        self.pnl_per_day_of_month_dict[day][3] += current_pnl
        
        self.monthly_pnl_dict[month_year] += current_pnl
        if ((self.monthly_pnl_dict[month_year] + self.monthly_cash_out_stats_dict[month_year]) /
            self.monthly_start_capital_dict[month_year] > self.monthly_target):
            target_achieved_for_month = 1
        else:
            target_achieved_for_month = 0
            
        daily_roi = 100 * (self.current_capital + self.monthly_cash_out_stats_dict[month_year] - \
            self.monthly_start_capital_dict[month_year]) / self.monthly_start_capital_dict[month_year]
        self.update_daily_pos_exit_stats(pos_type, current_date,
                                         3,\
                                         # 3 is the index of the ROI field in the map
                                         daily_roi)
        self.reset_all_state_data()
        return True
        

    def maybe_squareoff_sell_position(self, current_date_time, current_index):
        current_date = util.get_date(current_date_time)
        i = current_index
        can_close_pos = 0
        exit_method = ""
        month_year = util.get_month_year(current_date_time)
        low_prices = self.data['Low']
        high_prices = self.data['High']
        open_prices = self.data['Open']
        pos_type = "SELL"
        
        # Check if SL hit.
        if (high_prices[i] >= self.sl_price):
            #self.pos_buy_price = self.sl_price
            self.pos_buy_price = max(open_prices[i], self.sl_price)
            message = "[SL] Closing position. Time: " + str(current_date_time) + " Sell Price: " +\
                str(self.pos_sell_price) + " Buy Price: " + str(self.pos_buy_price)
            traffic_light_strategy_util_v2.print_debug_log(message, 1)
            can_close_pos = 1
            exit_method = "SL_BUY"
            self.status_list[i] = exit_method
            self.monthly_pos_exit_stats_dict_sell[month_year][ExitMethod[exit_method].value] += 1
            self.update_daily_pos_exit_stats(pos_type, current_date,\
                                             ExitMethod[exit_method].value,\
                                             self.monthly_pos_exit_stats_dict_sell[month_year][ExitMethod[exit_method].value])
        elif (low_prices[i] < self.target_price):
            self.pos_buy_price = self.target_price
            message = "[Target] Closing position. Time: " + str(current_date_time) + " Sell Price: " +\
                str(self.pos_sell_price) + " Buy Price: " + str(self.pos_buy_price)
            traffic_light_strategy_util_v2.print_debug_log(message, 1)
            can_close_pos = 1
            exit_method = "TARGET_BUY"
            self.status_list[i] = exit_method
            self.monthly_pos_exit_stats_dict_sell[month_year][ExitMethod[exit_method].value] += 1
            self.update_daily_pos_exit_stats(pos_type, current_date,\
                                             ExitMethod[exit_method].value,\
                                             self.monthly_pos_exit_stats_dict_sell[month_year][ExitMethod[exit_method].value])
        
        if can_close_pos == 0:
            return False
        
        self.buy_time = current_date_time

        current_pnl = self.get_pnl()
        self.update_wins_data(pos_type, current_pnl)
        self.total_pnl += current_pnl
        self.current_capital += current_pnl
        self.update_transaction_record(pos_type, exit_method)
        
        util.add_or_update_val_to_key(self.pnl_per_day_dict, util.get_date(current_date_time),\
                                      current_pnl)
        ctr = 1
        if (current_pnl < 0):
            ctr = -1
        day = util.get_day_of_month(util.get_date(self.sell_time))
        if (self.pnl_per_day_of_month_dict.__contains__(day) == False):
            self.pnl_per_day_of_month_dict[day] = [0, 0, 0, 0]
        
        self.pnl_per_day_of_month_dict[day][0] += ctr
        if (ctr > 0):
            self.pnl_per_day_of_month_dict[day][1] += ctr
        else:
            self.pnl_per_day_of_month_dict[day][2] += ctr
        
        self.pnl_per_day_of_month_dict[day][3] += current_pnl
        
        self.monthly_pnl_dict[month_year] += current_pnl
        if ((self.monthly_pnl_dict[month_year] + self.monthly_cash_out_stats_dict[month_year]) /
            self.monthly_start_capital_dict[month_year] > self.monthly_target):
            target_achieved_for_month = 1
        else:
            target_achieved_for_month = 0
            
        daily_roi = 100 * (self.current_capital + self.monthly_cash_out_stats_dict[month_year] - \
            self.monthly_start_capital_dict[month_year]) / self.monthly_start_capital_dict[month_year]
        self.update_daily_pos_exit_stats(pos_type, current_date, 
                                         3,\
                                         # 3 is the index of the ROI field in the map
                                         daily_roi)
        self.reset_all_state_data()
        return True
    
    def may_be_start_buy_trade(self, current_date_time, current_index):
        i = current_index
        open_prices = self.data['Open']
        current_date = util.get_date(current_date_time)
        self.pos_buy_price = max(self.high_limit_price_based_on_alert_candle +\
                                     self.execution_error_margin_ticks,\
                                 open_prices[i])

        sl_price_to_consider =\
            math.ceil(self.sl_price_based_on_alert_candle_for_long) -\
            self.sl_buffer
        
        # Setting maximum SL as 100 for every trade.  
        self.sl_price = max(math.ceil(self.pos_buy_price - self.max_buy_sl),\
                       sl_price_to_consider)
        message = "Changing SL to: " + str(self.sl_price) + " from: " +\
            str(sl_price_to_consider)
        traffic_light_strategy_util_v2.print_debug_log(message, 0)
        potential_sl = self.pos_buy_price - self.sl_price
        
        # Risk management
        num_lots = math.floor(self.current_capital / self.price_per_lot)
        max_loss = self.current_capital * self.buy_sl_pct / 100
        potential_loss_per_lot = potential_sl * self.lot_size
        # print("Potential loss per lot: " +\
        #       str(potential_loss_per_lot) + " Max loss: " +\
        #       str(max_loss))
        if potential_loss_per_lot == 0:
            num_lots_throttled = num_lots
        else:
            num_lots_throttled = math.floor(max_loss /\
                                            potential_loss_per_lot)
                
        num_lots = min(num_lots, num_lots_throttled)
        self.num_units = num_lots * self.lot_size
        
        if self.num_units == 0:
            message = "Num units based on risk is 0."
            traffic_light_strategy_util_v2.print_debug_log(message, 0)
            return False

        self.is_open_pos_buy = 1
        self.buy_time = current_date_time
        self.last_trade_ctr = i

        self.status_list[i] = "BUY"
        self.target_price = (self.pos_buy_price + self.rr_ratio * potential_sl)
        message = "BUY trade initiated at: " + str(current_date_time) +\
            " Price: " + str(self.pos_buy_price) + " Target: " +\
            str(self.target_price) + " SL: " + str(self.sl_price)
        traffic_light_strategy_util_v2.print_debug_log(message, 1)
        
        self.num_buys += 1
        util.add_or_update_val_to_key(self.num_trades_per_day_dict,\
                                      util.get_date(current_date_time), 1)
        return True
    
    def may_be_start_sell_trade(self, current_date_time, current_index):
        i = current_index
        open_prices = self.data['Open']
        current_date = util.get_date(current_date_time)
        
        self.signal_list[i] = "SELL"
        self.pos_sell_price = min(self.low_limit_price_based_on_alert_candle -\
                                      self.execution_error_margin_ticks,\
                                  open_prices[i])

        sl_price_to_consider = math.ceil(self.sl_price_based_on_alert_candle_for_short) +\
                                self.sl_buffer
        
        # Setting maximum SL as 100 for every trade.  
        self.sl_price = min(math.ceil(self.pos_sell_price + self.max_sell_sl),\
                       sl_price_to_consider)
        message = "Changing SL to: " + str(self.sl_price) + " from: " +\
            str(sl_price_to_consider)
        traffic_light_strategy_util_v2.print_debug_log(message, -1)
        potential_sl = self.sl_price - self.pos_sell_price
        
        # Risk management
        num_lots = math.floor(self.current_capital / self.price_per_lot)
        max_loss = self.current_capital * self.sell_sl_pct / 100
        potential_loss_per_lot = potential_sl * self.lot_size
        # print("Potential loss per lot: " +\
        #       str(potential_loss_per_lot) + " Max loss: " +\
        #       str(max_loss))
        if potential_loss_per_lot == 0:
            num_lots_throttled = num_lots
        else:
            num_lots_throttled = math.floor(max_loss /\
                                            potential_loss_per_lot)
                
        num_lots = min(num_lots, num_lots_throttled)
        self.num_units = num_lots * self.lot_size
        
        if self.num_units == 0:
            message = "Num units based on risk is 0."
            traffic_light_strategy_util_v2.print_debug_log(message, 0)
            return False

        self.is_open_pos_sell = 1
        self.sell_time = current_date_time
        self.last_trade_ctr = i

        self.status_list[i] = "SELL"
        self.target_price = (self.pos_sell_price - self.rr_ratio * potential_sl)
        message = "SELL trade initiated at: " + str(current_date_time) +\
            " Price: " + str(self.pos_sell_price) + " Target: " +\
            str(self.target_price) + " SL: " + str(self.sl_price)
        traffic_light_strategy_util_v2.print_debug_log(message, 1)
        
        self.num_sells += 1
        util.add_or_update_val_to_key(self.num_trades_per_day_dict,\
                                      util.get_date(current_date_time), 1)
        return True
        
    def can_start_new_trade(self, current_date_time, current_index):
        current_time = util.get_time(current_date_time)
        i = current_index
        if (current_time > self.cut_off_time_to_start):
            message = "Not trying to initate a new trade after cutoff time."
            traffic_light_strategy_util_v2.print_debug_log(message, 0)
            return False
        
        if (current_time < self.start_time):
            message = "Not trying to initate a new trade before start time."
            traffic_light_strategy_util_v2.print_debug_log(message, 0)
            return False
        
        return True
    
    def is_break_out_or_break_down_snerario(self, current_date_time,\
                                            current_index):
        current_time = util.get_time(current_date_time)
        i = current_index
        high_prices = self.data['High']
        low_prices = self.data['Low']
        return high_prices[i] > self.high_limit_price_based_on_alert_candle or\
            low_prices[i] < self.low_limit_price_based_on_alert_candle

    def may_be_start_new_trade(self, current_date_time, current_index):
        current_time = util.get_time(current_date_time)
        i = current_index
        
        current_date = util.get_date(current_date_time)
        if (self.num_trades_per_day_dict.__contains__(current_date) and\
            self.num_trades_per_day_dict[current_date] >= self.max_trades_per_day):
            message = "Max number of trades done for the day."
            traffic_light_strategy_util_v2.print_debug_log(message, 0)
            return False 
        
        if self.alert_candle_encountered == False:
            return False
        
        high_prices = self.data['High']
        low_prices = self.data['Low']
        if high_prices[i] > self.high_limit_price_based_on_alert_candle and\
            self.buy_allowed == 1:
                return self.may_be_start_buy_trade(current_date_time, current_index)
        elif low_prices[i] < self.low_limit_price_based_on_alert_candle and\
            self.sell_allowed == 1:
                return self.may_be_start_sell_trade(current_date_time, current_index)
        else:
            self.reset_all_state_data()
            
        return False
    
    def process_current_candle(self, current_date_time, current_index):
        i = current_index
        open_prices = self.data['Open']
        high_prices = self.data['High']
        low_prices = self.data['Low']
        close_prices = self.data['Close']
        
        if self.alert_candle_encountered == 1:
            message = "Not processing the current candle as alert candle already encounterd."
            traffic_light_strategy_util_v2.print_debug_log(message, 0)
            return
        
        # Alert candle not encountered till now.
        if self.green_candle_encountered == 1:
            if open_prices[i] > close_prices[i] :
                self.alert_candle_encountered = 1
                self.red_candle = CandleMetadata(current_date_time,\
                                                 open_prices[i],\
                                                 high_prices[i],\
                                                 low_prices[i],\
                                                 close_prices[i])
            elif open_prices[i] < close_prices[i] :
                self.green_candle = CandleMetadata(current_date_time,\
                                                   open_prices[i],\
                                                   high_prices[i],\
                                                   low_prices[i],\
                                                   close_prices[i])
        elif self.red_candle_encountered == 1:
            if open_prices[i] < close_prices[i]:
               self.alert_candle_encountered = 1
               self.green_candle = CandleMetadata(current_date_time,\
                                                  open_prices[i],\
                                                  high_prices[i],\
                                                  low_prices[i],\
                                                  close_prices[i])
            elif open_prices[i] > close_prices[i]:
                self.red_candle = CandleMetadata(current_date_time,\
                                                 open_prices[i],\
                                                 high_prices[i],\
                                                 low_prices[i],\
                                                 close_prices[i])
        
        if self.alert_candle_encountered == 1:
            message = "Alert candle encountered at: " + str(current_date_time)
            traffic_light_strategy_util_v2.print_debug_log(message, 0)
            self.high_limit_price_based_on_alert_candle =\
                max(self.green_candle.high_price,\
                    self.red_candle.high_price)
            self.low_limit_price_based_on_alert_candle =\
                min(self.green_candle.low_price,\
                    self.red_candle.low_price)
            
            # Setting the SLs appropriately.
            self.sl_price_based_on_alert_candle_for_long =\
                self.low_limit_price_based_on_alert_candle
            self.sl_price_based_on_alert_candle_for_short =\
                self.high_limit_price_based_on_alert_candle
            return
                    
        if open_prices[i] < close_prices[i]:
            message = "Green candle encountered at: " + str(current_date_time)
            traffic_light_strategy_util_v2.print_debug_log(message, 0)
            self.green_candle_encountered = 1
            self.green_candle = CandleMetadata(current_date_time,\
                                               open_prices[i],\
                                               high_prices[i],\
                                               low_prices[i],\
                                               close_prices[i])
        elif open_prices[i] > close_prices[i] :
            message = "Red candle encountered at: " + str(current_date_time)
            traffic_light_strategy_util_v2.print_debug_log(message, 0)
            self.red_candle_encountered = 1
            self.red_candle = CandleMetadata(current_date_time,\
                                             open_prices[i],\
                                             high_prices[i],\
                                             low_prices[i],\
                                             close_prices[i])
        
    def implement_strategy(self):
        date = self.data['Date']
        high_prices = self.data['High']
        prev_date = ""
        for i in range(len(self.data)):
            if (i < self.last_trade_ctr or i <= 1):
                continue
            
            current_time = util.get_time(date[i])
            current_date = util.get_date(date[i])
            last_date = util.get_date(date[i-1])
            
            if (last_date != current_date):
                prev_date = last_date
                
            self.initialize(date[i], prev_date)
                    
            # Early return
            if (self.current_capital <= 0):
                message = "Capital exhausted."
                traffic_light_strategy_util_v2.print_debug_log(message, 0)
                break
                
            self.cash_out(date[i])
            #self.update_high_price(date[i], high_prices[i])
            
                
            if ((self.start_date != "" and util.get_date(date[i]) < self.start_date) or\
                (self.end_date != "" and util.get_date(date[i]) > self.end_date)):
                continue
                
            if self.maybe_squareoff_if_beyond_cutoff_time(date[i], i) == 1:
                continue
                    
            if (self.is_open_pos_buy == 1):
                self.maybe_squareoff_buy_position(date[i], i)
                continue
            elif (self.is_open_pos_sell == 1):
                self.maybe_squareoff_sell_position(date[i], i)
                continue
            
            if self.can_start_new_trade(date[i], i) == 0:
                continue
            
            if self.may_be_start_new_trade(date[i], i) == 0:
                self.process_current_candle(date[i], i)
                        
        print("[Initial Capital: " + str(self.initial_capital) +\
              " -> Final capital: " + str(math.floor(self.current_capital)) + "]")
        print("Wealth: " + str(self.reserves))
        
        return self.total_pnl, self.num_buys, self.num_buy_wins, self.num_sells,\
            self.num_sell_wins, self.initial_capital, self.reserves,\
            self.status_list, self.signal_list, self.pos_type_list,\
            self.buy_time_list, self.buy_price_list, self.sell_time_list,\
            self.sell_price_list, self.pnl_list, self.exit_method_list,\
            self.num_units_list, self.current_capital_list, self.pct_pnl_list,\
            self.total_pct_pnl_list, self.target_price_list,\
            self.pnl_per_day_of_month_dict, self.monthly_cash_out_stats_dict,\
            self.monthly_pos_exit_stats_dict_buy,\
            self.daily_pos_exit_stats_dict_buy,\
            self.monthly_pos_exit_stats_dict_sell,\
            self.daily_pos_exit_stats_dict_sell