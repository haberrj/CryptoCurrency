#!/usr/bin/python3

import API.api_utils as au

client = au.API_Client("/home/ronhaber/Documents/Crypto_Docs/Binance/", False)
print(client.GetAccountDetails())
buy_order = client.TestOrder("buy", "BTC", 2)
print(buy_order)