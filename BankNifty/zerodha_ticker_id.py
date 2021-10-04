#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 20:57:44 2021

@author: nishant.gupta
"""

name_zerodha_nse_id_realty_dict = dict({"3887105":"BRIGADE",\
                                        "3771393":"DLF",\
                                        "4576001":"GODREJPROP",\
                                        "179457":"HEMIPROP",\
                                        "3699201":"IBREALEST",\
                                        "5181953":"OBEROIRLTY",\
                                        "3725313":"PHOENIXLTD",\
                                        "5197313":"PRESTIGE",\
                                        "3539457":"SOBHA",\
                                        "4516097":"SUNTECK"})

name_zerodha_nse_id_it_dict = dict({"2955009":"COFORGE",\
                                    "4561409":"LTI",\
                                    "3675137":"MINDTREE",\
                                    "1152769":"MPHASIS",\
                                    "2748929":"OFSS"})

name_zerodha_nse_id_fmcg_dict = dict({"3876097":"COLPAL",\
                                      "197633":"DABUR",\
                                      "3460353":"EMAMI",\
                                      "2585345":"GODREJCP",\
                                      "4632577":"JUBLFOODS",\
                                      "1041153":"MARICO",\
                                      "648961":"PGHH",\
                                      "4278529":"UBL",\
                                      "2674433":"MCDOWELL",\
                                      "4843777":"VBL"})



name_zerodha_nse_id_dict = dict({"3861249":"ADANIPORT",\
                                 "60417":"ASIANPAINTS",\
                                 "1510401":"AXISBANK",\
                                 "4267265":"BAJAJ-AUTO",\
                                 "81153":"BAJFINANCE",\
                                 "4268801":"BAJAJFINSV",\
                                 "134657":"BPCL",\
                                 "2714625":"BHARTI-AIRTEL",\
                                 "140033":"BRITANIA",\
                                 "177665":"CIPLA",\
                                 "5215745":"COALINDIA",\
                                 "2800641":"DIVISLAB",\
                                 "225537":"DRREDDY",\
                                 "232961":"EICHERMOT",\
                                 "315393":"GRASIM",\
                                 "1850625":"HCLTECH",\
                                 "341249":"HDFCBANK",\
                                 "119553":"HDFCLIFE",\
                                 "345089":"HEROMOTOCO",\
                                 "348929":"HINDALCO",\
                                 "356865":"HUL",\
                                 "340481":"HDFC",\
                                 "1270529":"ICICI",\
                                 "424961":"ITC",\
                                 "415745":"IOC",\
                                 "1346049":"INDUSIND",\
                                 "408065":"INFY",\
                                 "3001089":"JSWSTEEL",\
                                 "492033":"KOTAKBANK",\
                                 "2939649":"LT",\
                                 "519937":"M&M",\
                                 "2815745":"MARUTI",\
                                 "2977281":"NTPC",\
                                 "4598529":"NESTLE",\
                                 "633601":"ONGC",\
                                 "3834113":"POWERGRID",\
                                 "738561":"RELIANCE",\
                                 "5582849":"SBILIFE",\
                                 "794369":"SHREECEM",\
                                 "779521":"SBIN",\
                                 "857857":"SUNPHARMA",\
                                 "2953217":"TCS",\
                                 "878593":"TATACONSUM",\
                                 "884737":"TATAMOTORS",\
                                 "895745":"TATASTEEL",\
                                 "3465729":"TECHM",\
                                 "897537":"TITAN",\
                                 "2889473":"UPL",\
                                 "2952193":"ULTRACEM",\
                                 "969473":"WIPRO",\
                                 "3887105":"BRIGADE",\
                                 "3771393":"DLF",\
                                 "4576001":"GODREJPROP",\
                                 "179457":"HEMIPROP",\
                                 "3699201":"IBREALEST",\
                                 "5181953":"OBEROIRLTY",\
                                 "3725313":"PHOENIXLTD",\
                                 "5197313":"PRESTIGE",\
                                 "3539457":"SOBHA",\
                                 "4516097":"SUNTECK",\
                                 "2955009":"COFORGE",\
                                 "4561409":"LTI",\
                                 "3675137":"MINDTREE",\
                                 "1152769":"MPHASIS",\
                                 "2748929":"OFSS",\
                                 "3876097":"COLPAL",\
                                 "197633":"DABUR",\
                                 "3460353":"EMAMI",\
                                 "2585345":"GODREJCP",\
                                 "4632577":"JUBLFOODS",\
                                 "1041153":"MARICO",\
                                 "648961":"PGHH",\
                                 "4278529":"UBL",\
                                 "2674433":"MCDOWELL",\
                                 "4843777":"VBL"})
    
shortlisted_tickers_dict = dict({"81153":"BAJFINANCE",\
                                 "4268801":"BAJAJFINSV",\
                                 "2714625":"BHARTI-AIRTEL",\
                                 "225537":"DRREDDY",\
                                 "232961":"EICHERMOT",\
                                 "1850625":"HCLTECH",\
                                 "348929":"HINDALCO",\
                                 "4632577":"JUBLFOODS",\
                                 "4561409":"LTI",\
                                 "519937":"M&M",\
                                 "2674433":"MCDOWELL",\
                                 "3675137":"MINDTREE",\
                                 "1152769":"MPHASIS",\
                                 "4598529":"NESTLE",\
                                 "3725313":"PHOENIXLTD",\
                                 "5197313":"PRESTIGE",\
                                 "779521":"SBIN",\
                                 "794369":"SHREECEM",\
                                 "4516097":"SUNTECK",\
                                 "2953217":"TCS",\
                                 "3465729":"TECHM",\
                                 "4278529":"UBL",\
                                 "2952193":"ULTRACEM"})

buy_stocks_dict = dict({"5215745":"COALINDIA",\
                        "2889473":"UPL",\
                        "81153":"BAJFINANCE",\
                        "895745":"TATASTEEL",\
                        "2714625":"BHARTI-AIRTEL",\
                        "779521":"SBIN",\
                        "4268801":"BAJAJFINSV",\
                        "2955009":"COFORGE",\
                        "177665":"CIPLA",\
                        "340481":"HDFC",\
                        "794369":"SHREECEM",\
                        "3675137":"MINDTREE",\
                        "1270529":"ICICI"})

sell_stocks_dict = dict({"5215745":"COALINDIA",\
                         "3699201":"IBREALEST",\
                         "4843777":"VBL",\
                         "884737":"TATAMOTORS",\
                         "738561":"RELIANCE",\
                         "179457":"HEMIPROP",\
                         "3861249":"ADANIPORT",\
                         "5197313":"PRESTIGE",\
                         "415745":"IOC",\
                         "2815745":"MARUTI",\
                         "633601":"ONGC",\
                         "2939649":"LT",\
                         "424961":"ITC",\
                         "857857":"SUNPHARMA",\
                         "3887105":"BRIGADE"})