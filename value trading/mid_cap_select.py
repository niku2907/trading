#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 23:52:57 2020

@author: nishant.gupta
"""


from intrinsic_data import value_investing_data_getter

tickers = [
"SRTRANSFIN.BO",\
"M&MFIN.BO",\
"RBLBANK.BO",\
"GLENMARK.BO",\
"TATAPOWER.BO",\
"CHOLAFIN.BO",\
"LICHSGFIN.BO",\
"FEDERALBNK.BO",\
"CROMPTON.BO",\
"BHARATFORG.BO",\
"COLPAL.BO",\
"APOLLOHOSP.BO",\
"TATACONSUM.BO",\
"CONCOR.BO",\
"BIOCON.BO",\
"IDFCFIRSTB.BO",\
"VOLTAS.BO",\
"IGL.BO",\
"DIVISLAB.BO",\
"EDELWEISS.BO",\
"RAMCOCEM.BO",\
"TVSMOTOR.BO",\
"NAUKRI.BO",\
"PAGEIND.BO",\
"MRF.BO",\
"CUMMINSIND.BO",\
"EXIDEIND.BO",\
"INDHOTEL.BO",\
"RAJESHEXPO.BO"
          ]

intersting_data_dict, tickers_collated_data, df_mid_cap_select = value_investing_data_getter.get_interesting_data(tickers)
df_mid_cap_select.to_excel("mid_cap_select.xls")