#!/usr/bin/python3

import API.api_utils as au

client = au.API_Client("/media/pi/HaberServer/Crypto_Share/API_Utils/Binance/", False)
# print(client.GetAccountDetails())
BNB = float(client.GetAssetBalance("BNB")["free"])
print(BNB)
commission = client.GetCommission("BNB") * 0.75
print(commission)
commission = client.GetCommission("LINK") * 0.75
print(commission)
# cash = 1000.0
# print(cash)
# price = float(client.GetCurrentPrice("LINK"))
# detailed = client.GetDetailedPrices("LINK")
# print(detailed)
# quantity = "{:0.0{}f}".format(float(cash/price), 3)
# print(quantity)
# print(float(quantity)*float(detailed["bid"]))
# d_quantity = "{:0.0{}f}".format(float(cash/float(detailed["ask"])), 3)
# print(d_quantity)
# print(float(d_quantity)*float(detailed["bid"]))
# buy_order = client.TestOrder("buy", "LINK", quantity)
# print(buy_order)