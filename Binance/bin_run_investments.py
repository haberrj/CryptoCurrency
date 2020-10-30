#!/usr/bin/python3

# Author: Ron Haber
# Date: 30.10.2020
# This script will track prices and save them to a csv similar to the Kraken scripts
# Will also 

import os, sys
import os.path
import csv
import json
import time
import API.api_utils as au
import Algorithm.coin_type as ct

def CheckIfFileExits(filename):
    return os.path.isfile(filename)

def GetCoinInfo(client, names):
    # names is an array of strings
    coins = []
    for name in names:
        details = {
            "time": au.convert_timestamp_to_date(int(time.time())),
            "name": name,
            "price":float(client.GetCurrentPrice(name))
        }
        coins.append(details)
    return coins

def WriteHistoryCSV(direc, client, coins):
    files = []
    for coin in coins:
        time = coin["time"]
        name = coin["name"]
        price = coin["price"]
        filename = direc + name + "_Realtime.csv"
        # If file exists append it
        if(CheckIfFileExits(filename)):
            with open(filename,'a') as old_csv:
                writer = csv.writer(old_csv)
                writer.writerow([time, name, price])
        else:
            keys = coin.keys()
            with open(filename, 'w') as new_csv:
                writer = csv.DictWriter(new_csv, keys)
                writer.writeheader()
                writer.writerow(coin)
        files.append(filename)
    return files

def ExecuteRealTimeDemo(names, data_direc, commission):
    execs = []
    for name in names:
        coin = ct.Currency(name, data_direc, commission)
        networth = coin.DetermineTradeType()
        details = {
            "name": name,
            "networth": networth
        }
        execs.append(details)
    return execs

client = au.API_Client("/home/ronhaber/Documents/API_Utils/", False)
names = ["BTC", "ETH", "BNB"]
info = GetCoinInfo(client, names)
files = WriteHistoryCSV("/home/ronhaber/Documents/Crypto_Docs/Binance/", client, info)

