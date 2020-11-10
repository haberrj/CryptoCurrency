#!/usr/bin/python3

import API.api_utils as au

client = au.API_Client("/home/ronhaber/Documents/Crypto_Docs/Binance/", False)
# print(client.GetAccountDetails())
cash = float(client.GetAssetBalance("EUR")["free"])
print(cash)
price = float(client.GetCurrentPrice("BTC"))
quantity = "{:0.0{}f}".format(float(cash/price), 5)
print(quantity)
buy_order = client.TestOrder("buy", "BTC", quantity)
print(buy_order)