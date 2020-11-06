#!/usr/bin/python3

# Author: Ron Haber
# Date: 6.11.2020
# This will execute actual trades on the Binance platform

import os, sys
import os.path
import csv, json, time
import argparse
import API.api_utils as au
import Actual_Investment.coin_type as ct

parser = argparse.ArgumentParser(description="Find the ideal thresholds for any currency.")
parser.add_argument("-d", "--home", type=str, required=True, help="The directory for artifacts")
parser.add_argument("-i", "--currencies", type=str, nargs="+", required=True, help="The names of currencies")

args = parser.parse_args()
home = str(args.home)
currencies = args.currencies
commission = float(args.commission)
names = []
for name in currencies:
    names.append(str(name).upper())

def CheckIfFileExits(filename):
    return os.path.isfile(filename)

def GetCoinInfo(client, names, direc):
    # names is an array of strings
    coins = []
    for name in names:
        try:
            balance = float(client.GetAssetBalance(name))
        except ValueError:
            balance = 0.0
        details = {
            "time": au.convert_timestamp_to_date(int(time.time())),
            "name": name,
            "price":float(client.GetCurrentPrice(name)),
            "balance": balance,
            "last_cash": GetCashValue(direc, name),
            "commission": float(client.GetCommission(name))
        }
        coins.append(details)
    actual_cash = client.GetAccountDetails()["balances"] # This will need to be changed somehow for the current cash amount
    return coins, actual_cash

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

def ExecuteRealTime(client, data_direc, info, actual_cash):
    execs = []
    order_info_array = []
    for value in info:
        name = value["name"]
        balance = value["balance"]
        cash = value["last_cash"]
        price = value["price"]
        commission = value["commission"]
        coin = ct.Currency(name, data_direc, commission, price, cash, balance) 
        action, quantity, networth = coin.DetermineTradeType() # This will need to return an action as well
        details = {
            "time": au.convert_timestamp_to_date(int(time.time())),
            "name": name,
            "action": action,
            "networth": networth
        }
        if(action == 1):
            # Buy
            if((price/actual_cash) == quantity):
                # need to implement a checker for this since the price will change between calls
                order_info = client.BuyItem(name, quantity)
                actual_cash -= (quantity * price) # checker for actual cash not sure if this will work but will have to see
            else:
                print("Insufficient Funds")
        elif(action == 2):
            # Sell
            order_info = client.SellItem(name, quantity)
            actual_cash += quantity * price
        order_info_array.append(order_info)
        execs.append(details)
    return order_info_array, execs 

def GetCashValue(direc, name):
    # Will read a .csv file for the coin in question
    csv_file = direc + name + "_Balance.csv"
    if(CheckIfFileExits(csv_file)):
        with open(csv_file, 'r') as cash_file:
            cash_values = csv.DictReader(cash_file)
            cash = list(cash_values)
        amount = float(cash[-1]["cash"])
    else:
        print("No file found")
        return
    return amount

if __name__ == "__main__":
    API_key_direc = "/media/pi/HaberServer/Crypto_Share/API_Utils/Binance/"
    actual_home = home + "Actual/"
    client = au.API_Client(API_key_direc, False)
    info, actual_cash = GetCoinInfo(client, names, actual_home) # Gets the price of the asset
    orders, executions = ExecuteRealTime(client, home, info, actual_cash)
    # Any writing to documents should be done at the end
    files = WriteHistoryCSV(home, client, info)
    # Write a history file for the orders