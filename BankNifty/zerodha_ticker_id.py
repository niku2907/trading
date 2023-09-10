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
                                    "4561409":"LTIM",\
                                    "3675137":"MINDTREE",\
                                    "1152769":"MPHASIS",\
                                    "2748929":"OFSS"})

name_zerodha_nse_id_fmcg_dict = dict({"3876097":"COLPAL",\
                                      "197633":"DABUR",\
                                      "3460353":"EMAMI",\
                                      "2585345":"GODREJCP",\
                                      "4632577":"JUBLFOOD",\
                                      "1041153":"MARICO",\
                                      "648961":"PGHH",\
                                      "4278529":"UBL",\
                                      "2674433":"MCDOWELL-N",\
                                      "4843777":"VBL"})



name_zerodha_nse_id_dict = dict({"3861249":"ADANIPORTS",\
                                 "60417":"ASIANPAINT",\
                                 "1510401":"AXISBANK",\
                                 "4267265":"BAJAJ-AUTO",\
                                 "81153":"BAJFINANCE",\
                                 "4268801":"BAJAJFINSV",\
                                 "134657":"BPCL",\
                                 "2714625":"BHARTI-AIRTEL",\
                                 "140033":"BRITANNIA",\
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
                                 "4632577":"JUBLFOOD",\
                                 "1041153":"MARICO",\
                                 "648961":"PGHH",\
                                 "4278529":"UBL",\
                                 "2674433":"MCDOWELL-N",\
                                 "4843777":"VBL"})
    
shortlisted_tickers_dict = dict({"81153":"BAJFINANCE",\
                                 "4268801":"BAJAJFINSV",\
                                 "2714625":"BHARTI-AIRTEL",\
                                 "225537":"DRREDDY",\
                                 "232961":"EICHERMOT",\
                                 "1850625":"HCLTECH",\
                                 "348929":"HINDALCO",\
                                 "4632577":"JUBLFOOD",\
                                 "4561409":"LTI",\
                                 "519937":"M&M",\
                                 "2674433":"MCDOWELL-N",\
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
                         "3861249":"ADANIPORTS",\
                         "5197313":"PRESTIGE",\
                         "415745":"IOC",\
                         "2815745":"MARUTI",\
                         "633601":"ONGC",\
                         "2939649":"LT",\
                         "424961":"ITC",\
                         "857857":"SUNPHARMA",\
                         "3887105":"BRIGADE"})
    
mid_cap_stocks_dict = dict({"5436929":"AUBANK",\
                            "25601":"AMARAJABAT",\
                            "41729":"APOLLOTYRE",\
                            "54273":"ASHOKLEY",\
                            "85761":"BALKRISIND",\
                            "1195009":"BANKBARODA",\
                            "1214721":"BANKINDIA",\
                            "94977":"BATAINDIA",\
                            "98049":"BEL",\
                            "108033":"BHARATFORGE",\
                            "112129":"BHEL",\
                            "2763265":"CANBK",\
                            "320001":"CASTROLIND",\
                            "175361":"CHOLAFIN",\
                            "2955009":"COFORGE",\
                            "1215745":"CONCOR",\
                            "486657":"CUMMINSIND",\
                            "245249":"ESCORTS",\
                            "173057":"EXIDEIND",\
                            "261889":"FEDERALBANK",\
                            "3463169":"GMRINFRA",\
                            "4576001":"GODREJPROP",\
                            "2863105":"IDFCFIRSTB",\
                            "7712001":"IBULHSGFIN",\
                            "3484417":"IRCTC",\
                            "1723649":"JINDALSTEL",\
                            "6386689":"LTFH",\
                            "511233":"LICHSGFIN",\
                            "4488705":"MGL",\
                            "3400961":"M&MFIN",\
                            "4879617":"MANAPPURAM",\
                            "548353":"MFSL",\
                            "3675137":"MINDTREE",\
                            "3689729":"PAGEIND",\
                            "3660545":"PFC",\
                            "4708097":"RBLBANK",\
                            "3930881":"RECLTD",\
                            "837889":"SRF",\
                            "1102337":"SHRIRAMFIN",\
                            "758529":"SAIL",\
                            "3431425":"SUNTV",\
                            "2170625":"TVSMOTOR",\
                            "877057":"TATAPOWER",\
                            "523009":"RAMCOCEM",\
                            "3529217":"TORENTPOWER",\
                            "2752769":"UNIONBANK",\
                            "3677697":"IDEA",\
                            "951809":"VOLTAS",\
                            "975873":"ZEEL"})
    
mid_cap_sell_stocks_dict = dict({"2752769":"UNIONBANK",\
                                 "1723649":"JINDALSTEL",\
                                 "975873":"ZEEL",\
                                 "3484417":"IRCTC",\
                                 "758529":"SAIL",\
                                 "2763265":"CANBK",\
                                 "112129":"BHEL",\
                                 "245249":"ESCORTS",\
                                 "3400961":"MMFIN",\
                                 "41729":"APOLLOTYRE",\
                                 "3677697":"IDEA",\
                                 "1214721":"BANKINDIA",\
                                 "3463169":"GMRINFRA"})
    
next_fifty_stocks_dict = dict({"5633":"ACC",\
                            "4583169":"ABOTTINDIA",\
                            "6401":"ADANIENT",\
                            "912129":"ADANIGREEN",\
                            #"138049028":"ADANITRANS",\
                            "2995969":"ALKEM",\
                            "325121":"AMBUJACEM",\
                            "40193":"APOLLOHOSP",\
                            "70401":"AUROPHARMA",\
                            "5097729":"DMART",\
                            "78081":"BAJAJHLDNG",\
                            "579329":"BANDHANBNK",\
                            "103425":"BERGERPAINT",\
                            "2911489":"BIOCON",\
                            "558337":"BOSCHLTD",\
                            "2029825":"ZYDUSLIFE",\
                            "3876097":"COLPAL",\
                            "3771393":"DLF",\
                            "197633":"DABUR",\
                            "1207553":"GAIL",\
                            "2585345":"GODREJCP",\
                            "1086465":"HDFCAMC",\
                            "2513665":"HAVELLS",\
                            "359937":"HINDPETRO",\
                            "5573121":"ICICIGI",\
                            "4774913":"ICICIPRULI",\
                            "2883073":"IGL",\
                            "7458561":"INDUSTOWER",\
                            "3520257":"NAUKRI",\
                            "2865921":"INDIGO",\
                            "4632577":"JUBLFOOD",\
                            "4561409":"LTI",\
                            "2672641":"LUPIN",\
                            "582913":"MRF",\
                            "1041153":"MARICO",\
                            "1076225":"MOTHERSON",\
                            "6054401":"MUTHOOTFIN",\
                            "3924993":"NMDC",\
                            "2905857":"PETRONET",\
                            "681985":"PIDILITIND",\
                            "617473":"PEL",\
                            "648961":"PGHH",\
                            "2730497":"PNB",\
                            "4600577":"SBICARD",\
                            "806401":"SIEMENS",\
                            "900609":"TORNTPHARM",\
                            "4278529":"UBL",\
                            "2674433":"MCDOWELL-N",\
                            "784129":"VEDL",\
                            "3050241":"YESBANK"})
    
buy_stocks_dict_low_capital = dict({"2714625":"BHARTI-AIRTEL",\
                            "6401":"ADANIENT",\
                            "3675137":"MINDTREE",\
                            "7712001":"IBULHSGFIN",\
                            "895745":"TATASTEEL",\
                            "2889473":"UPL",\
                            "4268801":"BAJAJFINSV",\
                            "2955009":"COFORGE"})

sell_stocks_dict_low_capital = dict({"2752769":"UNIONBANK",\
                                     "5215745":"COALINDIA",\
                                     "3699201":"IBREALEST",\
                                     "4843777":"VBL",\
                                     "738561":"RELIANCE",\
                                     "112129":"BHEL",\
                                     "1723649":"JINDALSTEL",\
                                     "3484417":"IRCTC",\
                                     "2865921":"INDIGO",\
                                     "975873":"ZEEL",\
                                     "579329":"BANDHANBNK",\
                                     "179457":"HEMIPROP",\
                                     "3677697":"IDEA",\
                                     "877057":"TATAPOWER",\
                                     "1214721":"BANKINDIA"})
    
sell_stocks_dict_low_capital_new = dict({
                                     "3699201":"IBREALEST",\
                                     "179457":"HEMIPROP",\
                                     "2752769":"UNIONBANK",\
                                     "3887105":"BRIGADE",\
                                     "4843777":"VBL",\
                                     "1214721":"BANKINDIA",\
                                     "884737":"TATAMOTORS",\
                                     "320001":"CASTROLIND",\
                                     "877057":"TATAPOWER",\
                                     "41729":"APOLLOTYRE",\
                                     "3677697":"IDEA",\
                                     "5181953":"OBEROIRLTY",\
                                     "112129":"BHEL",\
                                     "4708097":"RBLBANK",\
                                     "3484417":"IRCTC",\
                                     "633601":"ONGC",\
                                     "579329":"BANDHANBNK"
                                     })

current_stocks_dict = dict({"3699201":"IBREALEST",\
                            "256265":"NIFTY"})

screener_stocks_dict = dict({"4592385":"HINDCOPPER",\
                             "108033":"BHARATFORG",\
                             "3060993":"IDFC",\
                             "5533185":"ABCAPITAL",\
                             "300545":"GNFC",\
                             "1517057":"INTELLECT",\
                             "3329":"ABB",\
                             "4752385":"LTTS",\
                             "952577":"TATACOMM"
                            })

name_zerodha_nse_fno_dict = dict({
                                    "4267265":"BAJAJ-AUTO",\
                                    "81153":"BAJFINANCE",\
                                    "4268801":"BAJAJFINSV",\
                                    "85761":"BALKRISIND",\
                                    "1195009":"BANKBARODA",\
                                    "1214721":"BANKINDIA",\
                                    "579329":"BANDHANBNK",\
                                    "98049":"BEL",\
                                    "103425":"BERGEPAINT",\
                                    "108033":"BHARATFORGE",\
                                    "2714625":"BHARTIARTL",\
                                    "112129":"BHEL",\
                                    "2911489":"BIOCON",\
                                    "558337":"BOSCHLTD",\
                                    "134657":"BPCL",\
                                    "140033":"BRITANNIA",\
                                    "1790465":"BSOFT",\
                                    "2029825":"ZYDUSLIFE",\
                                    "2763265":"CANBK",\
                                    "149249":"CANFINHOME",\
                                    "163073":"CHAMBLFERT",\
                                    "175361":"CHOLAFIN",\
                                    "177665":"CIPLA",\
                                    "5215745":"COALINDIA",\
                                    "2955009":"COFORGE",\
                                    "3876097":"COLPAL",\
                                    "1215745":"CONCOR",\
                                    "189185":"COROMANDEL",\
                                    "4376065":"CROMPTON",\
                                    "1459457":"CUB",\
                                    "486657":"CUMMINSIND",\
                                    "197633":"DABUR",\
                                    "2067201":"DALBHARAT",\
                                    "5105409":"DEEPAKNTR",\
                                    "3851265":"DELTACORP",\
                                    "2800641":"DIVISLAB",\
                                    "3771393":"DLF",\
                                    "225537":"DRREDDY",\
                                    "232961":"EICHERMOT",\
                                    "245249":"ESCORTS",\
                                    "173057":"EXIDEIND",\
                                    "261889":"FEDERALBANK",\
                                    "3661825":"FSL",\
                                    "1207553":"GAIL",\
                                    "1895937":"GLENMARK",\
                                    "3463169":"GMRINFRA",\
                                    "4576001":"GODREJPROP",\
                                    "2585345":"GODREJCP",\
                                    "3039233":"GRANULES",\
                                    "315393":"GRASIM",\
                                    "3378433":"GSPL",\
                                    "2713345":"GUJGASLTD",\
                                    "589569":"HAL",\
                                    "2513665":"HAVELLS",\
                                    "1850625":"HCLTECH",\
                                    "341249":"HDFCBANK",\
                                    "119553":"HDFCLIFE",\
                                    "345089":"HEROMOTOCO",\
                                    "348929":"HINDALCO",\
                                    "340481":"HDFC",\
                                    "1086465":"HDFCAMC",\
                                    "356865":"HUL",\
                                    "359937":"HINDPETRO",\
                                    "7712001":"IBULHSGFIN",\
                                    "1270529":"ICICI",\
                                    "5573121":"ICICIGI",\
                                    "4774913":"ICICIPRULI",\
                                    "3677697":"IDEA",\
                                    "2863105":"IDFCFIRSTB",\
                                    "56321":"IEX",\
                                    "2883073":"IGL",\
                                    "387073":"INDHOTEL",\
                                    "387841":"INDIACEM",\
                                    "2745857":"INDIAMART",\
                                    "2865921":"INDIGO",\
                                    "1346049":"INDUSINDBK",\
                                    "7458561":"INDUSTOWER",\
                                    "415745":"IOC",\
                                    "408065":"INFY",\
                                    "418049":"IPCALAB",\
                                    "3484417":"IRCTC",\
                                    "424961":"ITC",\
                                    "1723649":"JINDALSTEL",\
                                    "3397121":"JKCEMENT",\
                                    "3001089":"JSWSTEEL",\
                                    "4632577":"JUBLFOOD",\
                                    "492033":"KOTAKBANK",\
                                    "6386689":"L&TFH",\
                                    "2983425":"LALPATHLAB",\
                                    "4923905":"LAURASLABS",\
                                    "511233":"LICHSGFIN",\
                                    "519937":"M&M",\
                                    "3400961":"M&MFIN",\
                                    "4879617":"MANAPPURAM",\
                                    "1041153":"MARICO",\
                                    "2815745":"MARUTI",\
                                    "2674433":"MCDOWELL-N",\
                                    "7982337":"MCX",\
                                    "2452737":"METROPOLIS",\
                                    "548353":"MFSL",\
                                    "4488705":"MGL",\
                                    "3675137":"MINDTREE",\
                                    "1152769":"MPHASIS",\
                                    "1076225":"MOTHERSON",\
                                    "1152769":"MPHASIS",\
                                    "582913":"MRF",\
                                    "6054401":"MUTHOOTFIN",\
                                    "91393":"NAM-INDIA",\
                                    "1629185":"NATIONALUM",\
                                    "3520257":"NAUKRI",\
                                    "3756033":"NAVINFLUOR",\
                                    "4598529":"NESTLE",\
                                    "3924993":"NMDC",\
                                    "2977281":"NTPC",\
                                    "5181953":"OBEROIRLTY",\
                                    "2748929":"OFSS",\
                                    "633601":"ONGC",\
                                    "3689729":"PAGEIND",\
                                    "617473":"PEL",\
                                    "4701441":"PERSISTENT",\
                                    "2905857":"PETRONET",\
                                    "3660545":"PFC",\
                                    "676609":"PFIZER",\
                                    "681985":"PIDILITIND",\
                                    "6191105":"PIIND",\
                                    "2730497":"PNB",\
                                    "2455041":"POLYCAB",\
                                    "3834113":"POWERGRID",\
                                    "3365633":"PVR",\
                                    "523009":"RAMCOCEM",\
                                    "4708097":"RBLBANK",\
                                    "3930881":"RECLTD",\
                                    "738561":"RELIANCE",\
                                    "758529":"SAIL",\
                                    "4600577":"SBICARD",\
                                    "5582849":"SBILIFE",\
                                    "794369":"SHREECEM",\
                                    "779521":"SBIN",\
                                    "806401":"SIEMENS",\
                                    "837889":"SRF",\
                                    "1102337":"SHRIRAMFIN",\
                                    "1887745":"STAR",\
                                    "857857":"SUNPHARMA",\
                                    "3431425":"SUNTV",\
                                    "2622209":"SYNGENE",\
                                    "871681":"TATACHEM",\
                                    "878593":"TATACONSUM",\
                                    "884737":"TATAMOTORS",\
                                    "895745":"TATASTEEL",\
                                    "877057":"TATAPOWER",\
                                    "2953217":"TCS",\
                                    "3465729":"TECHM",\
                                    "897537":"TITAN",\
                                    "900609":"TORNTPHARM",\
                                    "3529217":"TORNTPOWER",\
                                    "502785":"TRENT",\
                                    "2170625":"TVSMOTOR",\
                                    "4278529":"UBL",\
                                    "2952193":"ULTRACEMCO",\
                                    "2889473":"UPL",\
                                    "784129":"VEDL",\
                                    "951809":"VOLTAS",\
                                    "4610817":"WHIRLPOOL",\
                                    "969473":"WIPRO",\
                                    "975873":"ZEEL",\
                                    
                                    "6483969":"APLLTD",\
                                    "40193":"APOLLOHOSP",\
                                    "70401":"AUROPHARMA",\
                                    "41729":"APOLLOTYRE",\
                                    "54273":"ASHOKLEY",\
                                    "60417":"ASIANPAINT",\
                                    "1510401":"AXISBANK",\
                                    "3691009":"ASTRAL",\
                                    "67329":"ATUL",\
                                    "5436929":"AUBANK",\
                                    "1790465":"BSOFT",\
                                    
                                    "1793":"AARTIND",\
                                    "4583169":"ABBOTINDIA",\
                                    "7707649":"ABFRL",\
                                    "5633":"ACC",\
                                    "6401":"ADANIENT",\
                                    "3861249":"ADANIPORTS",\
                                    "2995969":"ALKEM",\
                                    "25601":"AMARAJABAT",\
                                    "325121":"AMBUJACEM"})

fno_shortlists_dict = ({"3660545":"PFC",\
                        "163073":"CHAMBLFERT",\
                        "1887745":"STAR",\
                        "884737":"TATAMOTORS"})
    
rsi_screener_tickers = dict({'258049': 'FACT',
 '111617': 'IFGLEXPOR',
 '125185': 'ICEMAKE',
 '1307649': 'KPIGREEN',
 '1471489': 'CYIENT',
 '152321': 'CARBORUNIV',
 '1700609': 'SJS',
 '1853953': 'METROBRAND',
 '1865473': 'JTLIND',
 '194561': 'CGPOWER',
 '2408449': 'RAINBOW',
 '2707713': 'KRBL',
 '2828801': 'SIRCA',
 '2916865': 'ZOTA',
 '2927361': 'SPANDANA',
 '2941697': 'APARINDS',
 '3015169': 'GOKEX',
 '3024129': 'SHOPERSTOP',
 '3247617': 'MBAPL',
 '3444993': 'KAMDHENU',
 '3478273': 'ACE',
 '3509761': 'FIEMIND',
 '3522817': 'BBL',
 '3553281': 'BANCOINDIA',
 '3618305': 'PITTIENG',
 '3692289': 'LAOPALA',
 '3717889': 'ICRA',
 '3817473': 'KPRMILL',
 '3885825': 'ECLERX',
 '3905025': 'CEATLTD',
 '3945985': 'TITAGARH',
 '416513': 'LINDEINDIA',
 '4326401': 'DPWIRES',
 '4565249': 'AHLUCONT',
 '4569857': 'DLINKINDIA',
 '462849': 'KAJARIACER',
 '4690177': 'LGBBROSLTD',
 '4776705': 'MARATHON',
 '492289': 'WEALTH',
 '5013761': 'BSE',
 '533761': 'MAHSCOOTER',
 '5359617': 'KIRLOSENG',
 '5415425': 'ERIS',
 '615937': 'NEULANDLAB',
 '7426049': 'SUNCLAYLTD',
 '774145': 'JINDALSAW',
 '8705': 'ADORWELD',
 '873217': 'TATAELXSI',
 '889601': 'THERMAX',
 '964097': 'WHEELS',
 '1199105': 'SONACOMS',
 '1134849': 'HITECHGEAR',
 '1215233': 'INDNIPPON',
 '1520129': 'MONTECARLO',
 '162305': 'IGARASHI',
 '1741569': 'STEELCAS',
 '2079745': 'AJANTPHARM',
 '2269697': 'CHOICEIN',
 '2295809': 'HARIOMPIPE',
 '2395137': 'MSTCLTD',
 '244481': 'ESABINDIA',
 '2445569': 'PRUDENT',
 '2455553': 'VENUSPIPES',
 '2478849': 'KPITTECH',
 '274689': 'FOSECOIND',
 '2762497': 'NUCLEUS',
 '2876417': 'JSL',
 '2877185': 'NSIL',
 '2918145': 'SALZERELEC',
 '2974209': 'ASTRAMICRO',
 '2983681': 'JBMA',
 '302337': 'GODFRYPHLP',
 '304641': 'FMGOETZE',
 '3116289': 'HNDFDS',
 '3288833': 'KRISHANA',
 '3336961': 'SAFARI',
 '3343617': '360ONE',
 '3394561': 'KEC',
 '3453697': 'JKLAKSHMI',
 '3465217': 'VIDHIING',
 '3526657': 'GESHIP',
 '3552001': 'JINDRILL',
 '361473': 'AGI',
 '3623425': 'UNOMINDA',
 '3663105': 'INDIANB',
 '3816449': 'KDDL',
 '42497': 'ANDHRAPAP',
 '4512001': 'MOLDTECH',
 '4873217': 'PODDARMENT',
 '5102337': 'ORISSAMINE',
 '534529': 'MAHSEAMLES',
 '5409537': 'TEJASNET',
 '5506049': 'COCHINSHIP',
 '582401': 'IRISDOREME',
 '6194177': 'VADILALIND',
 '619777': 'NILKAMAL',
 '630529': 'MIDHANI',
 '79873': 'TIINDIA',
 '824321': 'LODHA',
 '941057': 'VESUVIUS',
 '6546945': 'SHAKTIPUMP',
 '10241': 'AEGISCHEM',
 '1147137': 'AARTIDRUGS',
 '1158401': 'DYNAMATECH',
 '1253889': 'FDC',
 '1401601': 'GRSE',
 '1472257': 'SANSERA',
 '1552897': 'ATGL',
 '1750017': 'FOCUS',
 '1883649': 'DATAPATTNS',
 '2039041': 'MALLCOM',
 '2127617': 'BLUESTARCO',
 '2412033': 'SILVERTUC',
 '2695681': 'SHARDAMOTR',
 '2707969': 'MPSLTD',
 '2708481': 'TCI',
 '275457': 'ZENSARTECH',
 '2920193': 'XPROINDIA',
 '2968577': 'LINCOLN',
 '3006209': 'JINDALPHOT',
 '3348737': 'TRIVENI',
 '3425537': 'KKCL',
 '3492609': 'ELECON',
 '3579393': 'JASH',
 '3641089': 'TIIL',
 '3670785': 'GANESHHOUC',
 '3732993': 'SRHHYPOLTD',
 '3752193': 'INSECTICID',
 '3849985': 'CERA',
 '3871745': 'KOLTEPATIL',
 '39425': 'APCOTEXIND',
 '3944705': 'NESCO',
 '4281601': 'RPGLIFE',
 '4306177': 'VINYLINDIA',
 '4417537': 'ALBERTDAVD',
 '4453633': 'PREMEXPLN',
 '4724993': 'POWERINDIA',
 '4756737': 'KIRLOSBROS',
 '4849665': 'KINGFA',
 '5058817': 'ADFFOODS',
 '506625': 'LAXMIMACH',
 '5565441': 'CHOLAHLDNG',
 '5691649': 'DHUNINV',
 '613633': 'SANDHAR',
 '6549505': 'TRITURBINE',
 '731905': 'RAYMOND',
 '7685889': 'ATULAUTO',
 '7977729': 'RHIM',
 '867585': 'AGARIND',
 '966657': 'IWEL',
 '993281': 'SOMANYCERA',
 '635137': 'ONWARDTEC',
 '1128961': 'JAGSNPHARM',
 '1191937': 'SBCL',
 '122881': 'BIRLACORPN',
 '1329153': 'KOVAI',
 '1688577': 'SONATSOFTW',
 '1718529': 'MOLDTKPAC',
 '1719809': 'SAPPHIRE',
 '1768449': 'VISHNU',
 '1779457': 'LINC',
 '1922049': 'ZENTEC',
 '2060801': 'MAHLIFE',
 '2307585': 'ANUP',
 '2461953': 'SPLPETRO',
 '258817': 'SCHAEFFLER',
 '2753281': 'APTECHT',
 '2895105': 'BALAXI',
 '3026177': 'WELCORP',
 '308481': 'GOODYEAR',
 '32769': 'ROUTE',
 '3374593': 'ROHLTD',
 '3406081': 'CENTURYPLY',
 '3471361': 'GRINDWELL',
 '3544065': 'MMFL',
 '3587585': 'LUMAXTECH',
 '3598849': 'SANGHVIMOV',
 '3634689': 'TIMKEN',
 '3877377': 'JYOTHYLAB',
 '408833': 'INGERRAND',
 '441857': 'JBCHEPHARM',
 '4460545': 'GLOBUSSPR',
 '4474113': 'CONTROLPR',
 '4476417': 'EXPLEOSOL',
 '4546049': 'SARDAEN',
 '4547585': 'REFEX',
 '498945': 'KSB',
 '5168129': 'WABAG',
 '5256705': 'GRAVITA',
 '6491649': 'PGEL',
 '693505': 'MTARTECH',
 '71169': 'AUTOAXLES',
 '716545': 'CHEMFAB',
 '730625': 'CRAFTSMAN',
 '7452929': 'CARERATING',
 '764929': 'SANDESH',
 '803329': 'HONDAPOWER',
 '8065793': 'JPOLYINVST',
 '82945': 'ANGELONE',
 '867073': 'SMLISUZU',
 '894209': 'TINPLATE',
 '923393': 'UNIVCABLES',
 '136233732': 'SAREGAMA',
 '113921': '5PAISA',
 '1568001': 'GOODLUCK',
 '1586689': 'FCL',
 '160001': 'CENTURYTEX',
 '1805569': 'ACCELYA',
 '1946369': 'CMSINFO',
 '2187777': 'CHALET',
 '2226177': 'VRLLOG',
 '2402561': 'PNCINFRA',
 '265729': 'FINCABLES',
 '2676993': 'ARVSMART',
 '2681089': 'POWERMECH',
 '2723073': 'OLECTRA',
 '2729217': 'PONNIERODE',
 '2855681': 'CREATIVE',
 '2883841': 'TVSELECT',
 '2964481': 'WESTLIFE',
 '297985': 'NEWGEN',
 '3020289': 'ALLSEC',
 '3023105': 'IIFL',
 '3475713': 'VOLTAMP',
 '3835393': 'CENTUM',
 '414977': 'TATAINVEST',
 '4330241': 'ZFCVINDIA',
 '4369665': 'UJJIVAN',
 '4419329': 'ARMANFIN',
 '4437249': 'MHRIL',
 '47105': 'TCPLPACK',
 '516609': 'LUMAXIND',
 '524545': 'CHENNPETRO',
 '5284353': 'JINDWORLD',
 '5344513': 'PSPPROJECT',
 '5476353': 'MAGADSUGAR',
 '6576641': 'DSSL',
 '692481': 'PRAJIND',
 '724225': 'ANURAS',
 '850945': 'SUBROS',
 '860929': 'SUPREMEIND',
 '999937': 'CAPLIPOINT',
 '4066049': 'HINDWAREAP',
 '1050881': 'SILINV',
 '1131777': 'CREDITACC',
 '1327617': 'STYLAMIND',
 '1649921': 'TECHNOE',
 '1753089': 'GREENLAM',
 '1818881': 'TEGA',
 '1894657': 'RAJESHEXPO',
 '193793': 'CRISIL',
 '2263041': 'USHAMART',
 '2316545': 'ROTO',
 '254209': 'EVERESTIND',
 '2924289': 'DATAMATICS',
 '2931713': 'CCL',
 '2992385': 'SUPRAJIT',
 '3065601': 'RML',
 '3350017': 'AIAENG',
 '3353857': 'VIMTALABS',
 '3412993': 'SOLARINDS',
 '342529': 'SDBL',
 '3433985': 'RSYSTEMS',
 '3493889': 'TALBROAUTO',
 '351233': 'HINDCOMPOS',
 '364545': 'HINDZINC',
 '3646721': 'TVSSRICHAK',
 '3676417': 'APOLLOPIPE',
 '3742209': 'CHEMBOND',
 '375553': 'AKZOINDIA',
 '3908097': 'JKIL',
 '3982081': 'HCG',
 '428033': 'HGINFRA',
 '4286721': 'RBL',
 '4399617': 'SHRIPISTON',
 '4430593': 'AJMERA',
 '462081': 'KABRAEXTRU',
 '4638209': 'THANGAMAYL',
 '4672513': 'SPAL',
 '4754177': 'GNA',
 '481025': 'CARYSIL',
 '4835585': 'KSL',
 '4870401': 'KIRLOSIND',
 '4966657': 'BOROLTD',
 '5154305': 'RAMKY',
 '5404929': 'BFINVEST',
 '5446401': 'SUMMITSEC',
 '548865': 'BDL',
 '6629633': 'MINDACORP',
 '728065': 'RANEHOLDIN',
 '787969': 'SHANTIGEAR',
 '815617': 'SKFINDIA',
 '866305': 'SWARAJENG',
 '526337': 'HOMEFIRST',
 '1041153': 'MARICO',
 '108033': 'BHARATFORG',
 '1102337': 'SHRIRAMFIN',
 '1346049': 'INDUSINDBK',
 '140033': 'BRITANNIA',
 '1723649': 'JINDALSTEL',
 '175361': 'CHOLAFIN',
 '177665': 'CIPLA',
 '1790465': 'BSOFT',
 '1850625': 'HCLTECH',
 '1895937': 'GLENMARK',
 '2029825': 'ZYDUSLIFE',
 '225537': 'DRREDDY',
 '232961': 'EICHERMOT',
 '245249': 'ESCORTS',
 '2455041': 'POLYCAB',
 '2585345': 'GODREJCP',
 '2622209': 'SYNGENE',
 '2674433': 'MCDOWELL-N',
 '2714625': 'BHARTIARTL',
 '2745857': 'INDIAMART',
 '2748929': 'OFSS',
 '2865921': 'INDIGO',
 '2952193': 'ULTRACEMCO',
 '2995969': 'ALKEM',
 '3001089': 'JSWSTEEL',
 '315393': 'GRASIM',
 '3329': 'ABB',
 '3397121': 'JKCEMENT',
 '341249': 'HDFCBANK',
 '3529217': 'TORNTPOWER',
 '3691009': 'ASTRAL',
 '3725313': 'PHOENIXLTD',
 '3756033': 'NAVINFLUOR',
 '3876097': 'COLPAL',
 '424961': 'ITC',
 '4278529': 'UBL',
 '4583169': 'ABBOTINDIA',
 '502785': 'TRENT',
 '5181953': 'OBEROIRLTY',
 '5436929': 'AUBANK',
 '5633': 'ACC',
 '60417': 'ASIANPAINT',
 '6191105': 'PIIND',
 '6401': 'ADANIENT',
 '70401': 'AUROPHARMA',
 '779521': 'SBIN',
 '806401': 'SIEMENS',
 '85761': 'BALKRISIND',
 '900609': 'TORNTPHARM',
 '1003009': 'NATCOPHARM',
 '1027585': 'NAVA',
 '149249': 'CANFINHOME',
 '1510401': 'AXISBANK',
 '189185': 'COROMANDEL',
 '1965825': 'MONARCH',
 '2067201': 'DALBHARAT',
 '239873': 'ELGIEQUIP',
 '2496001': 'ETHOSLTD',
 '2538753': 'NEOGEN',
 '2672641': 'LUPIN',
 '2763265': 'CANBK',
 '2919169': 'POONAWALLA',
 '2939649': 'LT',
 '3019265': 'SAKSOFT',
 '3031041': 'NH',
 '325121': 'AMBUJACEM',
 '3360257': 'REPRO',
 '3400961': 'M&MFIN',
 '3407361': 'KEI',
 '3424257': 'UTTAMSUGAR',
 '3481089': 'SELAN',
 '3703297': 'KIRLFER',
 '3771393': 'DLF',
 '3823873': 'CIEINDIA',
 '386049': 'ASTERDM',
 '387073': 'INDHOTEL',
 '3887105': 'BRIGADE',
 '3913729': 'HERCULES',
 '40193': 'APOLLOHOSP',
 '4107521': 'PRINCEPIPE',
 '41729': 'APOLLOTYRE',
 '4305665': 'QNIFTY',
 '4343041': 'TATAMTRDVR',
 '4488705': 'MGL',
 '4701441': 'PERSISTENT',
 '486657': 'CUMMINSIND',
 '5197313': 'PRESTIGE',
 '519937': 'M&M',
 '5582849': 'SBILIFE',
 '558337': 'BOSCHLTD',
 '5728513': 'MAXHEALTH',
 '6936321': 'SWANENERGY',
 '78081': 'BAJAJHLDNG',
 '854785': 'SUNDARMFIN',
 '857857': 'SUNPHARMA',
 '864001': 'SURYAROSNI',
 '884737': 'TATAMOTORS',
 '897537': 'TITAN',
 '945665': 'VINDHYATEL',
 '952577': 'TATACOMM',
 '837889': 'SRF',
 '1014529': 'GOCLCORP',
 '1084161': 'WENDT',
 '1095425': 'DENORA',
 '1100545': 'STERTOOLS',
 '1240833': 'KIMS',
 '130305': 'MAZDOCK',
 '1316353': 'CIGNITITEC',
 '1351425': 'ROLEXRINGS',
 '1436161': 'ASTRAZEN',
 '1577985': 'BHAGCHEM',
 '1777665': 'GANECOS',
 '2090753': 'MANYAVAR',
 '2170625': 'TVSMOTOR',
 '2305793': 'NOVARTIND',
 '2813441': 'RADICO',
 '2815745': 'MARUTI',
 '2910465': 'TTKHLTCARE',
 '2921217': 'RKFORGE',
 '2962689': 'FORCEMOT',
 '3031297': 'KENNAMET',
 '3432705': 'GPIL',
 '3443457': 'RATNAMANI',
 '3613697': 'GANDHITUBE',
 '3650561': 'PGIL',
 '3708161': 'THEMISMED',
 '3735553': 'FORTIS',
 '3848705': 'BAJAJELEC',
 '3942145': 'EIHAHOTELS',
 '416769': 'BECTORFOOD',
 '437249': 'JAYBARMARU',
 '4598529': 'NESTLEIND',
 '4840449': 'PNBHOUSING',
 '4843777': 'VBL',
 '4865': 'STYRENIX',
 '5204225': 'CGCL',
 '589569': 'HAL',
 '6054401': 'MUTHOOTFIN',
 '6218753': 'VSTTILLERS',
 '637185': 'ISEC',
 '643329': 'BCLIND',
 '6500353': 'PANAMAPET',
 '6583809': 'POLYMED',
 '6599681': 'APLAPOLLO',
 '7401729': 'ROSSELLIND',
 '768513': 'WONDERLA',
 '852225': 'ISGEC',
 '856321': 'SUNDRMFAST',
 '878593': 'TATACONSUM',
 '953345': 'VSTIND',
 '962817': 'RITES',
 '136363012': 'AURIONPRO',
 '1234433': 'DODLA',
 '1270529': 'ICICIBANK',
 '1829121': 'ANANDRATHI',
 '3048705': 'SWELECTES',
 '3577857': 'TANLA',
 '417281': 'IONEXCHANG',
 '4267265': 'BAJAJ-AUTO',
 '464385': 'KPIL',
 '801025': 'SHREYAS',
 '1614849': 'APOLSINHOT',
 '1676545': 'GRPLTD',
 '1992449': 'BCONCEPTS',
 '2019585': 'MHLXMIRU',
 '2026241': 'EIMCOELECO',
 '207873': 'BSHSL',
 '2087937': 'MEGASTAR',
 '2371585': 'ARROWGREEN',
 '2416641': 'AXISCADES',
 '3062785': 'REVATHI',
 '3360001': 'KERNEX',
 '3399169': 'INDOTECH',
 '3556865': 'HIRECT',
 '3844609': 'MAANALU',
 '4289281': 'RANEENGINE',
 '4359681': 'PATANJALI',
 '4444161': 'GKWLIMITED',
 '4588545': 'GEEKAYWIRE',
 '4704001': 'NDGL',
 '4830721': 'MAZDA',
 '5041921': 'JITFINFRA',
 '5069825': 'WELINV',
 '5697793': 'NDRAUTO',
 '6556673': 'INDOTHAI',
 '138152964':'BESTAGRO'})