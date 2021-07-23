#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 17:06:52 2021

@author: nishant.gupta
"""


# This class reads the data in the xls file and creates a pandas stream out of
# it.

import pandas as pd

class data_reader:
    def read(file_name):
        return pd.read_excel(file_name)
    
#exp1 = data_reader.read("Historical_data.xlsx")
#exp1.set_index('Date', inplace=True)
#exp2 = data_reader.read("Historical_data.xlsx", "July21")
