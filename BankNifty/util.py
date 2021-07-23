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
    
    def add_or_update_val_to_key(dictionary, key, val):
        if (dictionary.__contains__(key)):
            dictionary[key] += val;
        else:
            dictionary[key] = val
            
    def check_if_val_within_limit(dictionary, key, limit):
        if (dictionary.__contains__(key)):
            return abs(dictionary[key]) < limit
        
        return True
        