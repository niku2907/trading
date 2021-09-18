#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 20:35:33 2021

@author: nishant.gupta
"""

from data_reader import data_reader 

one_minute_data = data_reader.read("NIFTYBANK_ONE_YEAR_DATA.xlsx")
five_minute_data = one_minute_data.iloc[::5]