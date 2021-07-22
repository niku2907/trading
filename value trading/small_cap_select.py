#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 02:09:02 2020

@author: nishant.gupta
"""


from intrinsic_data import value_investing_data_getter

tickers = [
"ESCORTS.BO",\
"KALPATPOWR.BO",\
"PVR.BO",\
"NIITTECH.BO",\
"EQUITAS.BO",\
"STAR.BO",\
"JUBLFOOD.BO",\
"BATAINDIA.BO",\
"TATAELXSI.BO",\
"KAJARIACER.BO",\
"UJJIVAN.BO",\
"MANAPPURAM.BO",\
"HEXAWARE.BO",\
"ADANIGAS.BO",\
"CANFINHOME.BO",\
"APOLLOTYRE.BO",\
"VGUARD.BO",\
"MINDTREE.BO",\
"MGL.BO",\
"NCC.BO",\
"SRF.BO",\
"GSPL.BO",\
"COROMANDEL.BO",\
"MCX.BO",\
"DELTACORP*.BO",\
"RADICO.BO",\
"HEG.BO",\
"STRTECH*.BO",\
"QUESS.BO",\
"GNFC.BO",\
"DCBBANK.BO",\
"IPCALAB.BO",\
"JUBILANT.BO",\
"PFIZER.BO",\
"SYNGENE.BO",\
"JMFINANCIL.BO",\
"SOUTHBANK.BO",\
"SANOFI.BO",\
"VIPIND.BO",\
"CYIENT.BO",\
"GRAPHITE.BO",\
"FORTIS.BO",\
"KTKBANK.BO",\
"LALPATHLAB.BO",\
"VBL.BO",\
"CUB.BO",\
"PRESTIGE.BO",\
"IDFC.BO",\
"KEC.BO",\
"PGHL.BO",\
"ENGINERSIN.BO",\
"PIIND.BO",\
"EIHOTEL.BO",\
"ASTRAL.BO",\
"CARERATING.BO",\
"PHOENIXLTD.BO",\
"JKCEMENT.BO",\
"PERSISTENT.BO",\
"THERMAX.BO"
          ]

intersting_data_dict, tickers_collated_data, df_small_cap_select = value_investing_data_getter.get_interesting_data(tickers)
df_small_cap_select.to_excel("small_cap_select.xls")