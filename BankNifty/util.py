#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 18:08:48 2021

@author: nishant.gupta
"""

import math
from datetime import date, datetime, timedelta

class util:
    def get_year(data):
        # data = '2020-07-28T15:25:00'
        return int(data.split('T')[0].split('-')[0])
    
    def get_month(data):
        # data = '2020-07-28T15:25:00'
        return int(data.split('T')[0].split('-')[1])
    
    def get_only_date(data):
        # data = '2020-07-28T15:25:00'
        return int(data.split('T')[0].split('-')[2])
    
    def get_date_object(data):
        # data = '2020-07-28T15:25:00'
        return date(util.get_year(data), util.get_month(data),\
                    util.get_only_date(data))
            
    def get_last_day_date_object(data):
        # data = '2020-07-28T15:25:00'
        return util.get_date_object(data) - timedelta(days=1)
    
    def get_future_day_object(data, delta):
        # data = '2020-07-28T15:25:00'
        return util.get_date_object(data) + timedelta(days=delta)
    
    def get_past_day_object(data, delta):
        # data = '2020-07-28T15:25:00'
        return util.get_date_object(data) - timedelta(days=delta)
        
    def is_one_day_ahead(date1, date2):
        # date1 should be the later one compared to date2
        one_day = timedelta(days=1)
        return date1 - date2 == one_day

    def get_time_minutes_before_ts(ts, diff):
        # ts = '2020-07-28T15:25:00'
        ts_format = '%Y-%m-%dT%H:%M:%S'
        date_time = datetime.strptime(ts, ts_format)
        return (date_time - timedelta(minutes = diff)).strftime(ts_format)
    
    def get_time_minutes_after_ts(ts, diff):
        # ts = '2020-07-28T15:25:00'
        ts_format = '%Y-%m-%dT%H:%M:%S'
        date_time = datetime.strptime(ts, ts_format)
        return (date_time + timedelta(minutes = diff)).strftime(ts_format)
        
    def get_time_diff_minutes(ts1, ts2):
        # ts1 = '2020-07-28T15:25:00+0530'
        #print("TS1: " + ts1 + " TS2: " + ts2)
        FMT = '%H:%M:%S'
        tdelta = datetime.strptime(util.get_time(ts2), FMT) -\
            datetime.strptime(util.get_time(ts1), FMT)
        return math.floor(tdelta.seconds / 60)
   
    def get_last_month(data):
        # data = '2017-08'
        year = int(data.split('-')[0])
        month = int(data.split('-')[1])
        if month == 1:
            month = 12
            year = year - 1
        else:
            month = month - 1
        return str(year) + '-' + "{0:0=2d}".format(month)
    
    def is_first_before_than_second(ts1, ts2):
        # ts1 = '2020-07-28T15:25:00+0530'
        # ts2 = '2020-07-29T15:25:00+0530'
        date1_str = ts1.split('T')[0]
        date2_str = ts2.split('T')[0]
        date1 = datetime(int(date1_str.split('-')[0]),\
                         int(date1_str.split('-')[1]),\
                         int(date1_str.split('-')[2]))
        date2 = datetime(int(date2_str.split('-')[0]),\
                         int(date2_str.split('-')[1]),\
                         int(date2_str.split('-')[2]))    
        return date1 < date2
        
    def get_date(data):
        # date = '2020-07-28T15:25:00+0530'
        return data.split('T')[0]
    
    def get_day_of_month(data):
        #print("Data: " + str(data))
        return data.split('-')[2]
    
    def get_time(data):
        # data = '2020-07-28T15:25:00+0530'
        return data.split('T')[1].split('+')[0]
    
    def get_date_time(data):
        # data = '2020-07-28T15:25:00+0530'
        return data.split('+')[0]
    
    def get_month_year(data):
        # data = '2020-07-28T15:25:00+0530'
        return (data.split('T')[0].split('-')[0] + '-' + data.split('T')[0].split('-')[1])
    
    def add_or_update_val_to_key(dictionary, key, val):
        if (dictionary.__contains__(key)):
            dictionary[key] += val;
        else:
            dictionary[key] = val
            
    def check_if_val_within_limit(dictionary, key, up_limit, down_limit):
        if (dictionary.__contains__(key)):
            #return abs(dictionary[key]) < up_limit
        
            return (dictionary[key] < 0 and abs(dictionary[key]) < down_limit) or\
                (dictionary[key] > 0 and dictionary[key] < up_limit)
            #if (dictionary[key] < 0):
            #    return abs(dictionary[key]) < down_limit
        
        return True
    
    def check_if_trades_limit_not_reached(dictionary, key, limit):
        if (dictionary.__contains__(key)):
            return dictionary[key] < limit
        return True
        
    def get_pnl(buy_price, sell_price, num_lots, lot_size):
        brokerage = 40
        transaction_charges = (.002/100) * (buy_price + sell_price) * num_lots * lot_size
        stt = (.01/100) * sell_price * num_lots * lot_size
        stamp_duty = (.002/100) * buy_price * num_lots * lot_size
        sebi_charges = (10/100) * stamp_duty
        gst = (18/100) * (brokerage + transaction_charges)
        total_charges = brokerage + transaction_charges + stt + stamp_duty + sebi_charges + gst
        pnl = (sell_price - buy_price) * num_lots * lot_size - total_charges
        return pnl
        
#pnl = util.get_pnl(35000, 34025, 1, 25)