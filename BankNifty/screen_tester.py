# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 00:43:35 2023

@author: NishantGupta
"""
from data_reader import data_reader 
from enum import Enum
from util import util

class Signal(Enum):
    BUY = 0
    SELL = 1
    INVALID = 2
        
class Mode(Enum):
    INTRADAY = 0
    SWING = 1
    INVALID = 1
    
class ScreenTester:
    rr_ratio = 2
    num_minute_data = "5"
    look_back_days = 2
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
    start_date = "2019-01-01"
    start_date = ""
    end_date = "2019-12-31"
    end_date = ""
    
    
    def __init__(self, ticker_name, interesting_dates, mode, prev_num_years,\
                 signal):
        self.ticker_name = ticker_name
        # This is going to be a dictionary of date objects on which we got a\
        # signal to trade the stock from the screener.
        self.interesting_dates = interesting_dates
        self.mode = mode
        self.prev_num_years = prev_num_years
        self.file_prefix = str(int(prev_num_years)) + "_YEAR_TICKER_DATA/"
        self.num_two_months = prev_num_years * 6
        self.signal = signal
        stock_file_name = self.file_prefix + self.stock_name + "_" +\
            str(self.num_months) + "_MONTH_" +\
            self.num_minute_data + "_MINUTE_DATA.xlsx"
        self.five_minute_data = data_reader.read(stock_file_name)

    @staticmethod
    def print_debug_log(message, level):
        if (level > 1):
            print("[DEBUG] ", message)
            
    def can_trade(self, current_date):
        valid_date = util.get_last_day_date_object(current_date) in\
            self.interesting_dates.values()
        if valid_date == False:
            return False
        
        current_time = util.get_time(current_date)
        if (current_time > self.cut_off_time_to_start):
            message = "Not trying to initate a new trade after cutoff time."
            ScreenTester.print_debug_log(message, 0)
            return False
        
        if (current_time < self.start_time):
            message = "Not trying to initate a new trade before start time."
            ScreenTester.print_debug_log(message, 0)
            return False
        
        return True
            
    def get_pnl(self):
        message = "Profit of: " + str(self.pos_sell_price - self.pos_buy_price) + " per unit"
        if (self.pos_buy_price > self.pos_sell_price):
            message = "Loss of: " + str(self.pos_buy_price - self.pos_sell_price) + " per unit"
        
        ScreenTester.print_debug_log(message, 1)
        return ScreenTester.get_pnl_including_taxes(self.pos_buy_price,\
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
    
    def maybe_squareoff_if_beyond_cutoff_time(self, current_date_time, current_index):
        i = current_index
        current_time = util.get_time(current_date_time)
        if current_time < self.cut_off_time_to_close:
            return False
        if self.is_open_pos_buy == 0 and self.is_open_pos_sell == 0:
            return True
        
        open_prices = self.five_minute_data['Open']
        if self.is_open_pos_buy == 1:
            
            current_pnl = self.get_pnl()
            self.update_wins_data(pos_type, current_pnl)
            self.total_pnl += current_pnl
            self.current_capital += current_pnl
        else :
            self.squareoff_sell_position_beyond_cutoff(open_prices[i],\
                                                       current_date_time,\
                                                       current_index)

        #self.reset_all_state_data()
        return True
            
    def trade(self):
        print("********************************************************************")
        print("Processing stock: ", self.ticker_name)
        date = self.five_minute_data['Date']
        high_prices = self.five_minute_data['High']
        for i in range(len(self.five_minute_data)):
            if self.can_trade(date[i]) == False:
                continue
            
            if (self.current_capital <= 0):
                message = "Capital exhausted."
                ScreenTester.print_debug_log(message, 0)
                break
            
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
            
            
            
                
            
             
         
            
    