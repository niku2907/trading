#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 18:08:48 2021

@author: nishant.gupta
"""


class util:
    def get_date(data):
        # date = '2020-07-28T15:25:00+0530'
        return data.split('T')[0]
    
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