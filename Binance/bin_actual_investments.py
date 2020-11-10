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
names = []
for name in currencies:
    names.append(str(name).upper())

def CheckIfFileExits(filename):
    return os.path.isfile(filename)

def GetCoinInfo(client, names, direc):
    # names is an array of strings
    coins = []
    direc = direc + "Balances/"
    for name in names:
        try:
            balance = float(client.GetAssetBalance(name))
        except ValueError:
            balance = 0.0
        except TypeError:
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
    actual_cash = client.GetAssetBalance("EUR")["free"] # This will need to be changed somehow for the current cash amount
    print(actual_cash)
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
            keys = list(coin.keys())
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
        print(name)
        print("price: ", price)
        coin = ct.Currency(name, data_direc, commission, price, cash, balance) 
        action, quantity, networth = coin.DetermineTradeType() # This will need to return an action as well
        print("Actions ", action, " ", quantity, " ", networth, " ", cash)
        # action = 2
        details = {
            "time": au.convert_timestamp_to_date(int(time.time())),
            "name": name,
            "action": action,
            "networth": networth
        }
        order_info = False
        if(action == 1):
            # Buy
            new_price = float(client.GetCurrentPrice(name))
            print("new_price", new_price)
            if(name == "BTC" or name == "ETH"):
                quantity = "{:0.0{}f}".format(float(cash/new_price), 5)
            else:
                quantity = "{:0.0{}f}".format(float(cash/new_price), 3)
            print("quantity: ", quantity)
            order_info = client.BuyItem(name, quantity)
            # order_info = client.TestOrder("buy", name, quantity)
            print(order_info)
            if(order_info == False):
                print("Insufficient Funds")
        elif(action == 2):
            # Sell
            # new_price = float(client.GetCurrentPrice(name))
            if(name == "BTC" or name == "ETH"):
                quantity = "{:0.0{}f}".format(quantity, 5)
            else:
                quantity = "{:0.0{}f}".format(quantity, 3)
            print(quantity)
            order_info = client.SellItem(name, quantity)
            # order_info = client.TestOrder("sell", name, quantity)
            if(order_info == False):
                print("Error with order")
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

def CheckOrderStatuses(direc, orders):
    data_direc = direc + "/Actual/CSV_Transactions/"
    transaction_files = []
    cash_files = []
    for order in orders:
        if(order == False):
            continue
        print(order["name"])
        print(order["status"])
        if(order["side"] == "SELL"):
            name = order["name"]
            price = order["price"]
            quantity = order["coin"]
            data_direc = direc + "Actual/Balances/"
            cash = float(price) * float(quantity)
            cash = "{:0.0{}f}".format(quantity, 2)
            print(cash)
            cash_files.append(WriteNewCashAmount(data_direc, name, cash))
        transaction_files.append(WriteTransactionInfo(direc, order["name"], order))
    return transaction_files, cash_files

def WriteNewCashAmount(data_direc, name, cash):
    filename = data_direc + name + "_Balance.csv"
    time = au.convert_timestamp_to_date(int(time.time()))
    if(CheckIfFileExits(filename)):
        with open(filename,'a') as old_csv:
            writer = csv.writer(old_csv)
            writer.writerow([time, name, price])
    else:
        details = {
            "time": time,
            "name": name,
            "cash": cash
        }
        keys = list(details.keys())
        with open(filename, 'w') as new_csv:
            writer = csv.DictWriter(new_csv, keys)
            writer.writeheader()
            writer.writerow(details)
    return filename

def WriteTransactionInfo(direc, name, order):
    filename = data_direc + order["name"] + "_transactions.csv"
    keys = list(order.keys())
    if(CheckIfFileExits(filename)):
        with open(filename,'a') as old_csv:
            writer = csv.writer(old_csv)
            writer.writerow([time, name, price])
    else:
        with open(filename, 'w') as new_csv:
            writer = csv.DictWriter(new_csv, keys)
            writer.writeheader()
            writer.writerow(order)
    return filename
    
if __name__ == "__main__":
    API_key_direc = "/media/pi/HaberServer/Crypto_Share/API_Utils/Binance/"
    actual_home = home + "Actual/"
    client = au.API_Client(API_key_direc, False)
    info, actual_cash = GetCoinInfo(client, names, actual_home) # Gets the price of the asset
    orders, executions = ExecuteRealTime(client, home, info, actual_cash)
    transaction_files, cash_files = CheckOrderStatuses(home, orders)
    print(transaction_files)
    print(cash_files)
    # Any writing to documents should be done at the end
    files = WriteHistoryCSV(home, client, info)
    print(files)
    # Write a history file for the orders