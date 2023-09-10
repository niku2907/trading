# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 22:38:36 2023

@author: NishantGupta
"""

# Preprocessing code to fetch id of a ticker
url = 'https://kite.zerodha.com/api/marketwatch/1440239495/items'
headers = {
    'authority': 'kite.zerodha.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'WZRK_G=9baf6448cd4743fc89275711aa5a4ea1; _hjSessionUser_896738=eyJpZCI6Ijk4NmUxMTYzLWRmM2YtNTA3Yi1hOTE1LTg3YTRhMTkxMmFlZiIsImNyZWF0ZWQiOjE2NzI4MTYwNjQxOTEsImV4aXN0aW5nIjp0cnVlfQ==; intercom-id-y72tx0ov=dab5e8a7-6f19-452f-86b0-30bb5b6a34d9; intercom-device-id-y72tx0ov=b56aab9d-127c-4012-98bf-45a85d8ac978; _ga=GA1.2.1353505318.1652246977; _ga_X88LHJCZCR=GS1.1.1673342377.20.1.1673342404.0.0.0; _cfuvid=_g4vANIKUHV7DD7nn1aXX5nBz5VNVyWQ.9RznRYj7HU-1690475567842-0-604800000; kf_session=PCpI9LhU4yeRxMQiOfvljnjvw9rVxbWV; user_id=JB7207; public_token=aiQvzBE5wQRaiCM2rPpicD4sivBdVlsf; enctoken=JHI9cXHPn3Jm9tO12Qua/3aUSDWjoMxS4Eco8/KunQju6q2EyPYC1oGgygfSYorlo16aN2Ay4EAil2ySwlwtvaLpg6GcB28+L0fTxLe8868HhMf/C334Kw==',
    'origin': 'https://kite.zerodha.com',
    'referer': 'https://kite.zerodha.com/chart/web/tvc/NSE/ZENSARTECH/275457',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'x-csrftoken': 'aiQvzBE5wQRaiCM2rPpicD4sivBdVlsf',
    'x-kite-app-uuid': '736d2aec-dc90-471f-aeb9-3b28f03280da',
    'x-kite-userid': 'JB7207',
    'x-kite-version': '3.0.0',
}



def should_process_stock(stock):
    missing_stocks = []
    interesting_id = -1
    for ticker_id, ticker_name in done_dict.items():
        if ticker_name == stock:
            return False
        
    return True
        
    return interesting_id

missing_stocks_dict = {}
for stock in missing_stocks:
    if should_process_stock(stock) == False:
        continue
    data = {
        'segment': 'BSE',
        'tradingsymbol': stock,
        'watch_id': '1440239495',
        'weight': '1',
    }
    
    response = requests.post(url, headers=headers, data=data)
    stock_id = -1
    if response.status_code == 200:
        stock_id = int(response.json()['data']['instrument_token'])
    else:
        print("Stock: " + stock + " Request failed:", response)
        
    missing_stocks_dict.update({stock_id: stock})
    
# Use the following to convert an in-memory dict to a text form
missing_stocks_dict_new = {str(key): value for key, value in missing_stocks_dict.items()}
text_representation_final = "dict(" + pprint.pformat(missing_stocks_dict_new, width=40) + ")"