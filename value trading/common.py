#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 21:58:05 2020

@author: nishant.gupta
"""


ticker_symbol_id = dict({"ASIANPAINT.BO":   500820,\
                         "AXISBANK.BO":     532215,\
                         "BAJAJ-AUTO.BO":   532977,\
                         "BHARTIARTL.BO":   532454,\
                         "HCLTECH.BO":      532281,\
                         "HDFCBANK.BO":     500180,\
                         "HEROMOTOCO.BO":   500182,\
                         "HINDUNILVR.BO":   500696,\
                         "INDUSINDBK.BO":   532187,\
                         "INFY.BO":         500209,\
                         "ITC.BO":          500875,\
                         "KOTAKBANK.BO":    500247,\
                         "LT.BO":           500510,\
                         "M&M.BO":          500520,\
                         "MARUTI.BO":       532500,\
                         "NESTLEIND.BO":    500790,\
                         "NTPC.BO":         532555,\
                         "ONGC.BO":         500312,\
                         "POWERGRID.BO":    532898,\
                         "SBIN.BO":         500112,\
                         "SUNPHARMA.BO":    524715,\
                         "TATASTEEL.BO":    500470,\
                         "TCS.BO":          532540,\
                         "TECHM.BO":        532755,\
                         "ULTRACEMCO.BO":   532538,\
                         "BAJFINANCE.BO":   500034,\
                         "HDFC.BO":         500010,\
                         "ICICIBANK.BO":    532174,\
                         "RELIANCE.BO":     500325,\
                         "TITAN.BO":        500114,\
                         "ADANIPORTS.BO":   532921,\
                         "BAJAJFINSV.BO":   532978,\
                         "BPCL.BO":         500547,\
                         "BRITANNIA.BO":    500825,\
                         "CIPLA.BO":        500087,\
                         "COALINDIA.BO":    533278,\
                         "DRREDDY.BO":      500124,\
                         "EICHERMOT.BO":    505200,\
                         "GAIL.BO":         532155,\
                         "GODREJCP.BO":     532424,\
                         "GRASIM.BO":       500300,\
                         "HINDALCO.BO":     500440,\
                         "IBULHSGFIN.BO":   535789,\
                         "IOC.BO":          530965,\
                         "JSWSTEEL.BO":     500228,\
                         "TATAMOTORS.BO":   500570,\
                         "TATAMTRDVR.BO":   570001,\
                         "UPL.BO":          512070,\
                         "VEDL.BO":         500295,\
                         "WIPRO.BO":        507685,\
                         "YESBANK.BO":      532648,\
                         "DLF.BO":          532868,\
                         "GODREJPROP.BO":   533150,\
                         "IBREALEST.BO":    532832,\
                         "MAHLIFE.BO":      532313,\
                         "OBEROIRLTY.BO":   533273,\
                         "OMAXE.BO":        532880,\
                         "PHOENIXLTD.BO":   503100,\
                         "PRESTIGE.BO":     533274,\
                         "SOBHA.BO":        532784,\
                         "SUNTECK.BO":      512179,\
                         "ADANIPOWER.BO":   533096,\
                         "ADANITRANS.BO":   539254,\
                         "BHEL.BO":         500103,\
                         "CESC.BO":         500084,\
                         "KALPATPOWER.BO":  522287,\
                         "KEC.BO":          532714,\
                         "NHPC.BO":         533098,\
                         "NTPC.BO":         532555,\
                         "POWERGRID.BO":    532898,\
                         "SIEMENS.BO":      500550,\
                         "TATAPOWER.BO":    500400,\
                         "THERMAX.BO":      500411,\
                         "TORNTPOWER.BO":   532779,\
                         "BPCL.BO":         500547,\
                         "CASTROLIND.BO":   500870,\
                         "GAIL.BO":         532155,\
                         "GSPL.BO":         532702,\
                         "HINDPETRO.BO":    500104,\
                         "IGL.BO":          532514,\
                         "IOC.BO":          530965,\
                         "ONGC.BO":         500312,\
                         "PETRONET.BO":     532522,\
                         "RELIANCE.BO":     500325,\
                         "COALINDIA.BO":    533278,\
                         "HINDALCO.BO":     500440,\
                         "HINDZINC.BO":     500188,\
                         "JINDALSTEL.BO":   532286,\
                         "JSWSTEEL.BO":     500228,\
                         "NATIONALUM.BO":   532234,\
                         "NMDC.BO":         526371,\
                         "SAIL.BO":         500113,\
                         "TATASTEEL.BO":    500470,\
                         "VEDL.BO":         500295,\
                         "ADFFOODS.BO":     519183,\
                         "APOLLO.BO":       540879,\
                         "ARVSMART.BO":     539301,\
                         "CENTURYPLY.BO":   532548,\
                         "CGCL.BO":         531595,\
                         "DBREALTY.BO":     533160,\
                         "DEEPALFERT.BO":   500645,\
                         "DFM.BO":          519588,\
                         "DHANUKA.BO":      507717,\
                         "FELDVR.BO":       570002,\
                         "GAYAPROJ.BO":     532767,\
                         "HIKAL.BO":        524735,\
                         "HLVLTD.BO":       500193,\
                         "INDIACEM.BO":     530005,\
                         "INOXWIND.BO":     539083,\
                         "JBMA.BO":         532605,\
                         "JISLDVREQS.BO":   570004,\
                         "JUBILANT.BO":     530019,\
                         "JISLJALEQS.BO":   500219,\
                         "KRIINFRA.BO":     533482,\
                         "MCLEODRUSS.BO":   532654,\
                         "MUKANDLTD.BO":    500460,\
                         "NFL.BO":          523630,\
                         "PROZONINTU.BO":   534675,\
                         "RANKY.BO":        533262,\
                         "RCF.BO":          524230,\
                         "SADBHAV.BO":      532710,\
                         "SALASAR.BO":      540602,\
                         "SANGHIIND.BO":    526521,\
                         "SEYAIND.BO":      524324,\
                         "SKIPPER.BO":      538562,\
                         "SPENCER.BO":      542337,\
                         "TAJGVK.BO":       532390,\
                         "ZENSARTECH.BO":   504067,\
                         "NAUKRI.BO":       532777,\
                         "TATACONSUM.BO":   500800,\
                         "DIVISLAB.BO":     532488,\
                         "FEDERALBNK.BO":   500469,\
                         "BIOCON.BO":       532523,\
                         "LICHSGFIN.BO":    500253,\
                         "UBL.BO":          532478,\
                         "ALKEM.BO":        539523,\
                         "BALKRISIND.BO":   502355,\
                         "CUMMINSIND.BO":   500480,\
                         "NATCOPHARM.BO":   524816,\
                         "TVSMOTOR.BO":     532343,\
                         "RBLBANK.BO":      540065,\
                         "SRTRANSFIN.BO":   511218,\
                         "BERGEPAINT.BO":   509480,\
                         "GLAXO.BO":        500660,\
                         "GLENMARK.BO":     532296,\
                         "CRISIL.BO":       500092,\
                         "L&TFH.BO":        533519,\
                         "PGHH.BO":         500459,\
                         "GODREJIND.BO":    500164,\
                         "FRETAIL.BO":      540064,\
                         "CANBK.BO":        532483,\
                         "ISEC.BO":         541179,\
                         "HONAUT.BO":       517174,\
                         "CROMPTON.BO":     539876,\
                         "WHIRLPOOL.BO":    500238,\
                         "NBCC.BO":         534309,\
                         "IDFCFIRSTB.BO":   539437,\
                         "M&MFIN.BO":       532720,\
                         "GMRINFRA.BO":     532754,\
                         "INDIANB.BO":      532814,\
                         "ABCAPITAL.BO":    540691,\
                         "JSWENERGY.BO":    533148,\
                         "3MINDIA.BO":      523395,\
                         "BANKINDIA.BO":    532149,\
                         "PNBHOUSING.BO":   540173,\
                         "CHOLAHLDNG.BO":   504973,\
                         "NAM-INDIA.BO":    540767,\
                         "GODREJAGRO.BO":   540743,\
                         "COLPAL.BO":       500830,\
                         "IDBI.BO":         500116,\
                         "UNIONBANK.BO":    532477,\
                         "MRF.BO":          500290,\
                         "VARROC.BO":       541578,\
                         "NLCINDIA.BO":     513683,\
                         "GILLETTE.BO":     507815,\
                         "SJVN.BO":         533206,\
                         "AUBANK.BO":       540611,\
                         "KIOCL.BO":        540680,\
                         "LTI.BO":          540005,\
                         "MRPL.BO":         500109,\
                         "SHRIRAMCIT.BO":   532498,\
                         "CENTRALBK.BO":    532885,\
                         "ADANIENT.BO":     512599,\
                         "SUNTV.BO":        532733,\
                         "AJANTPHARM.BO":   532331,\
                         "CONCOR.BO":       531344,\
                         "KANSAINER.BO":    500165,\
                         "HUDCO.BO":        540530,\
                         "RAJESHEXPO.BO":   531500,\
                         "MUTHOOTFIN.BO":   533398,\
                         "PAGEIND.BO":      532827,\
                         "BHARATFORG.BO":   500493,\
                         "MFSL.BO":         500271,\
                         "ENDURANCE.BO":    540153,\
                         "CHOLAFIN.BO":     511243,\
                         "ABFRL.BO":        535755,\
                         "BAYERCROP.BO":    506285,\
                         "BAJAJHLDNG.BO":   500490,\
                         "OFSS.BO":         532466,\
                         "SUPREMEIND.BO":   509930,\
                         "MOTILALOFS*.BO":  532892,\
                         "OIL.BO":          533106,\
                         "HAL.BO":          541154,\
                         "EDELWEISS.BO":    532922,\
                         "VOLTAS.BO":       500575,\
                         "INDHOTEL.BO":     500850,\
                         "EMAMILTD*.BO":    531162,\
                         "AMARAJABAT.BO":   500008,\
                         "EXIDEIND.BO":     500086,\
                         "TORNTPHARM.BO":   500420,\
                         "RAMCOCEM.BO":     500260,\
                         "MPHASIS.BO":      526299,\
                         "BEL.BO":          500049,\
                         "APOLLOHOSP.BO":   508869,\
                         "SRTRANSFIN.BO":   511218,\
                         "M&MFIN.BO":532720,\
                         "RBLBANK.BO":540065,\
                         "GLENMARK.BO":532296,\
                         "TATAPOWER.BO":500400,\
                         "CHOLAFIN.BO":511243,\
                         "LICHSGFIN.BO":500253,\
                         "FEDERALBNK.BO":500469,\
                         "CROMPTON.BO":539876,\
                         "BHARATFORG.BO":500493,\
                         "COLPAL.BO":500830,\
                         "APOLLOHOSP.BO":508869,\
                         "TATACONSUM.BO":500800,\
                         "CONCOR.BO":531344,\
                         "BIOCON.BO":532523,\
                         "IDFCFIRSTB.BO":539437,\
                         "VOLTAS.BO":500575,\
                         "IGL.BO":532514,\
                         "DIVISLAB.BO":532488,\
                         "EDELWEISS.BO":532922,\
                         "RAMCOCEM.BO":500260,\
                         "TVSMOTOR.BO":532343,\
                         "NAUKRI.BO":532777,\
                         "PAGEIND.BO":532827,\
                         "MRF.BO":500290,\
                         "CUMMINSIND.BO":500480,\
                         "EXIDEIND.BO":500086,\
                         "INDHOTEL.BO":500850,\
                         "RAJESHEXPO.BO":531500,\
                             "ESCORTS.BO":500495,\
"KALPATPOWR.BO":522287,\
"PVR.BO":532689,\
"NIITTECH.BO":532541,\
"EQUITAS.BO":539844,\
"STAR.BO":532531,\
"JUBLFOOD.BO":533155,\
"BATAINDIA.BO":500043,\
"TATAELXSI.BO":500408,\
"KAJARIACER.BO":500233,\
"UJJIVAN.BO":539874,\
"MANAPPURAM.BO":531213,\
"HEXAWARE.BO":532129,\
"ADANIGAS.BO":542066,\
"CANFINHOME.BO":511196,\
"APOLLOTYRE.BO":500877,\
"VGUARD.BO":532953,\
"MINDTREE.BO":532819,\
"MGL.BO":539957,\
"NCC.BO":500294,\
"SRF.BO":503806,\
"GSPL.BO":532702,\
"COROMANDEL.BO":506395,\
"MCX.BO":534091,\
"DELTACORP*.BO":532848,\
"RADICO.BO":532497,\
"HEG.BO":509631,\
"STRTECH*.BO":532374,\
"QUESS.BO":539978,\
"GNFC.BO":500670,\
"DCBBANK.BO":532772,\
"IPCALAB.BO":524494,\
"JUBILANT.BO":530019,\
"PFIZER.BO":500680,\
"SYNGENE.BO":539268,\
"JMFINANCIL.BO":523405,\
"SOUTHBANK.BO":532218,\
"SANOFI.BO":500674,\
"VIPIND.BO":507880,\
"CYIENT.BO":532175,\
"GRAPHITE.BO":509488,\
"FORTIS.BO":532843,\
"KTKBANK.BO":532652,\
"LALPATHLAB.BO":539524,\
"VBL.BO":540180,\
"CUB.BO":532210,\
"PRESTIGE.BO":533274,\
"IDFC.BO":532659,\
"KEC.BO":532714,\
"PGHL.BO":500126,\
"ENGINERSIN.BO":532178,\
"PIIND.BO":523642,\
"EIHOTEL.BO":500840,\
"ASTRAL.BO":532830,\
"CARERATING.BO":534804,\
"PHOENIXLTD.BO":503100,\
"JKCEMENT.BO":532644,\
"PERSISTENT.BO":533179,\
"THERMAX.BO":500411,\
    "INDIACEM.BO":530005,\
"ESCORTS.BO":500495,\
"KALPATPOWR.BO":522287,\
"PVR.BO":532689,\
"NIITTECH.BO":532541,\
"EQUITAS.BO":539844,\
"STAR.BO":532531,\
"JUBLFOOD.BO":533155,\
"BATAINDIA.BO":500043,\
"LAXMIMACH.BO":500252,\
"TATAELXSI.BO":500408,\
"ARVIND.BO":500101,\
"JUSTDIAL.BO":535648,\
"KAJARIACER.BO":500233,\
"SPICEJET.BO":500285,\
"NOCIL.BO":500730,\
"UJJIVAN.BO":539874,\
"MANAPPURAM.BO":531213,\
"APLLTD.BO":533573,\
"DEEPAKNI.BO":506401,\
"SPENCER.BO":542337,\
"SUZLON.BO":532667,\
"IOLCP.BO":524164,\
"BEML.BO":500048,\
"HEXAWARE.BO":532129,\
"ADANIGAS.BO":542066,\
"HAWKINCOOK.BO":508486,\
"ASTRAZEN.BO":506820,\
"GODFRYPHLP.BO":500163,\
"CANFINHOME.BO":511196,\
"ARVINDFASN.BO":542484,\
"NATPEROX.BO":500298,\
"APOLLOTYRE.BO":500877,\
"DALBHARAT*.BO":542216,\
"VGUARD.BO":532953,\
"MINDTREE.BO":532819,\
"OMAXE.BO":532880,\
"MGL.BO":539957,\
"NCC.BO":500294,\
"SRF.BO":503806,\
"PHILIPCARB.BO":506590,\
"INOXLEISUR.BO":532706,\
"SPARC.BO":532872,\
"GMM.BO":505255,\
"ATULAUTO.BO":531795,\
"GRANULES.BO":532482,\
"GSPL.BO":532702,\
"COROMANDEL.BO":506395,\
"ASTEC.BO":533138,\
"MCX.BO":534091,\
"SUBEX.BO":532348,\
"IBULISL.BO":533520,\
"LAURUSLABS.BO":540222,\
"LEMONTREE.BO":541233,\
"WOCKPHARMA.BO":532300,\
"CESC.BO":500084,\
"CEATLTD.BO":500878,\
"TRENT.BO":500251,\
"DELTACORP*.BO":532848,\
"CGCL.BO":531595,\
"MIDHANI.BO":541195,\
"RADICO.BO":532497,\
"CHAMBLFERT.BO":500085,\
"RELAXO.BO":530517,\
"IBREALEST.BO":532832,\
"BALRAMCHIN.BO":500038,\
"HEG.BO":509631,\
"TVSSRICHAK.BO":509243,\
"POLYCAB.BO":542652,\
"STRTECH*.BO":532374,\
"QUESS.BO":539978,\
"GNFC.BO":500670,\
"JBCHEPHARM.BO":506943,\
"DCBBANK.BO":532772,\
"IPCALAB.BO":524494,\
"KIRIINDUS.BO":532967,\
"UFLEX.BO":500148,\
"AARTIDRUGS.BO":524348,\
"APOLLOTRI.BO":538566,\
"JUBILANT.BO":530019,\
"RAIN.BO":500339,\
"QUICKHEAL.BO":539678,\
"VSTIND.BO":509966,\
"LTTS.BO":540115,\
"HSCL.BO":500184,\
"BSOFT.BO":532400,\
"CIGNITI.BO":534758,\
"DLINKINDIA.BO":533146,\
"NAVINFLUOR.BO":532504,\
"PFIZER.BO":500680,\
"WABCOINDIA.BO":533023,\
"ADANIGREEN.BO":541450,\
"ASALCBR.BO":507526,\
"SHILPAMED.BO":530549,\
"SYNGENE.BO":539268,\
"JMFINANCIL.BO":523405,\
"TEJASNET.BO":540595,\
"AVANTI.BO":512573,\
"JKLAKSHMI.BO":500380,\
"ABBOTINDIA.BO":500488,\
"BIRLACORPN.BO":500335,\
"HEIDELBERG.BO":500292,\
"DHAMPURSUG.BO":500119,\
"SOUTHBANK.BO":532218,\
"RCF.BO":524230,\
"TV18BRDCST.BO":532800,\
"JAICORPLTD.BO":512237,\
"ALKYLAMINE.BO":506767,\
"SCHNEIDER.BO":534139,\
"RVNL.BO":542649,\
"SANOFI.BO":500674,\
"DEEPAKFERT.BO":500645,\
"TINPLATE.BO":504966,\
"GARFIBRES.BO":509557,\
"RITES.BO":541556,\
"RPOWER.BO":532939,\
"SCI.BO":523598,\
"BASF.BO":500042,\
"VIPIND.BO":507880,\
"JKTYRE.BO":530007,\
"BLISSGVS.BO":506197,\
"FERMENTA.BO":506414,\
"RESPONIND.BO":505509,\
"INDIAGLYCO.BO":500201,\
"DIXON.BO":540699,\
"NIITLTD.BO":500304,\
"DBL.BO":540047,\
"BALAMINES.BO":530999,\
"CYIENT.BO":532175,\
"GRAPHITE.BO":509488,\
"TRANSPEK.BO":506687,\
"RAYMOND.BO":500330,\
"SUDARSCHEM.BO":506655,\
"VINATIORGA.BO":524200,\
"FORTIS.BO":532843,\
"GPPL.BO":533248,\
"HFCL.BO":500183,\
"DBREALTY.BO":533160,\
"PRAJIND.BO":522205,\
"KTKBANK.BO":532652,\
"TRIVENI.BO":532356,\
"TRIDENT.BO":521064,\
"AMBIKCO.BO":531978,\
"SWANENERGY.BO":503310,\
"ALBERTDA.BO":524075,\
"ATUL.BO":500027,\
"LALPATHLAB.BO":539524,\
"SUNTECK.BO":512179,\
"CHENNPETRO.BO":500110,\
"SONATSOFTW.BO":532221,\
"BOSCHLTD.BO":500530,\
""
                         })