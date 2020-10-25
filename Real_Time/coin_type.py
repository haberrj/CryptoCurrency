#!/usr/bin/python3

# Author: Ron Haber
# Date: 12.10.2020
# This will create a class for the currency to hold relevant data

import os, sys
import os.path
import json
import csv
from datetime import datetime
import time
import ast

def convert_timestamp_to_date(timestamp):
    time_holder = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return time_holder

def BuyPercentageCurrency(cash, price, commission):
    percent_currency = cash/price * (1.0-commission)
    return percent_currency

def SellPercentageCurrency(currency, price, commission):
    amount = price*currency
    new_amount = amount * (1.0-commission)
    return new_amount

def CheckIfFileExits(filename):
    return os.path.isfile(filename)

class Currency:
    # will add more data as things come up
    def __init__(self, name, data_direc, commission):
        self.name = name
        self.direc = data_direc
        self.current_price = 0.0 
        self.last_three_prices = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] # ltp[0] is current price required to determine 2 first_deriv values
        self.first_deriv = [0.0,0.0] # required to determine the second derivative (first_deriv[0] is the important one here)
        self.second_deriv = 0.0
        self.cash = self.GetLastCashAmount()
        self.coin = self.GetLastCoinAmount()
        self.commission = commission
        self.current_holding_price = 0.0 

        self.thresholds = self.GetThresholds()
        self.GetPrices()
    
    def GetLastCashAmount(self):
        cash = 0.0
        if(self.name == "BTC"):
            csv_name = self.direc + "CSV_Transaction_Data/BTC_Transactions.csv"
        elif(self.name == "ETH"):
            csv_name = self.direc + "CSV_Transaction_Data/ETH_Transactions.csv"
        elif(self.name == "LTC"):
            csv_name = self.direc + "CSV_Transaction_Data/LTC_Transactions.csv"
        else:
            print("Invalid currency")
            return
        with open(csv_name, "r") as transaction_data:
            history_values = csv.DictReader(transaction_data)
            holder = []
            for value in history_values: 
                holder.append(value)
        transactions = list(reversed(holder))
        cash = float(transactions[0]["cash"])
        return cash

    def GetLastCoinAmount(self):
        coin = 0.0
        if(self.name == "BTC"):
            csv_name = self.direc + "CSV_Transaction_Data/BTC_Transactions.csv"
        elif(self.name == "ETH"):
            csv_name = self.direc + "CSV_Transaction_Data/ETH_Transactions.csv"
        elif(self.name == "LTC"):
            csv_name = self.direc + "CSV_Transaction_Data/LTC_Transactions.csv"
        else:
            print("Invalid currency")
            return
        with open(csv_name, "r") as transaction_data:
            history_values = csv.DictReader(transaction_data)
            holder = []
            for value in history_values: 
                holder.append(value)
        transactions = list(reversed(holder))
        coin = float(transactions[0]["coin"])
        return coin

    def GetThresholds(self):
        thresholds = []
        if(self.name == "BTC"):
            json_name = self.direc + "Json_Output_Data/btc_thresholds.json"
        elif(self.name == "ETH"):
            json_name = self.direc + "Json_Output_Data/eth_thresholds.json"
        elif(self.name == "LTC"):
            json_name = self.direc + "Json_Output_Data/ltc_thresholds.json"
        else:
            print("Invalid currency")
            return
        with open(json_name, "r") as json_file:
            data = json.load(json_file)
        thresholds = data["threshold"]
        return thresholds
    
    def GetPrices(self):
        prices = []
        if(self.name == "BTC"):
            csv_name = self.direc + "BTC_Realtime.csv"
        elif(self.name == "ETH"):
            csv_name = self.direc + "ETH_Realtime.csv"
        elif(self.name == "LTC"):
            csv_name = self.direc + "LTC_Realtime.csv"
        else:
            print("Invalid currency")
            return
        with open(csv_name, "r") as price_data:
            history_values = csv.DictReader(price_data)
            holder = []
            for value in history_values: 
                holder.append(value)
        prices = list(reversed(holder))
        for i in range(0,10):
            self.last_three_prices[i] = float(prices[i]["price"])
        self.current_price = self.last_three_prices[0]
        return self.current_price
        
    def GetBalance(self):
        coin_value = self.coin * self.current_price
        balance = self.cash + coin_value
        return balance

    def FirstDerivative(self):
        price_holder = self.last_three_prices
        for i in range(0, 2): # only iterate 2 times
            deriv_holder = (price_holder[i] - price_holder[i+2])/3.0 # captures the price over the last 3 points
            self.first_deriv[i] = deriv_holder
        return self.first_deriv

    def SecondDerivative(self):
        self.second_deriv = self.first_deriv[0] - self.first_deriv[1]
        return self.second_deriv

    def DetermineTradeType(self):
        price = self.GetPrices()
        first_val = self.FirstDerivative()
        second_val = self.SecondDerivative()
        self.thresholds = self.GetThresholds()
        if(self.cash > 0):
            if(first_val[0] < self.thresholds[0] and second_val > self.thresholds[1]):
                self.coin = BuyPercentageCurrency(self.cash, self.current_price, self.commission)
                self.cash = 0
                networth = self.GetBalance()
                print(networth)
                detailed = {
                    "time":convert_timestamp_to_date(int(time.time())),
                    "transaction": "bought",
                    "price":self.current_price,
                    "cash":self.cash,
                    "coin":self.coin,
                    "networth":networth
                }
                self.WriteSaleDataToCSV(detailed)
                self.WriteLastTransactionJson(detailed)
                self.current_holding_price = self.current_price
        if(self.coin > 0):
            if((self.current_holding_price < (self.current_price*0.75)) or (first_val[0] > self.thresholds[2] and second_val > self.thresholds[3])):
                # the addition of the holding price becoming too low will auto cause a sale of the asset itself
                # this will prevent severe loss in the case of the underlying losing value
                if((self.isProfitable(self.current_holding_price, self.current_price, self.commission)) or (self.current_holding_price < (self.current_price*0.98))):
                    # This will only sell if the current holding is profitable or if the above values are 
                    self.cash = SellPercentageCurrency(self.coin, self.current_price, self.commission)
                    self.coin = 0
                    networth = self.GetBalance()
                    detailed = {
                        "time":convert_timestamp_to_date(int(time.time())),
                        "transaction": "sold",
                        "price":self.current_price,
                        "cash":self.cash,
                        "coin":self.coin,
                        "networth":networth
                    }
                    self.WriteSaleDataToCSV(detailed)
                    self.WriteLastTransactionJson(detailed)
        # Write the info to a csv somewhere
        networth = self.GetBalance()
        return networth

    def WriteSaleDataToCSV(self, details):
        if(self.name == "BTC"):
            csv_name = self.direc + "CSV_Transaction_Data/BTC_Transactions.csv"
        elif(self.name == "ETH"):
            csv_name = self.direc + "CSV_Transaction_Data/ETH_Transactions.csv"
        elif(self.name == "LTC"):
            csv_name = self.direc + "CSV_Transaction_Data/LTC_Transactions.csv"
        else:
            print("Invalid currency")
            return
        if(CheckIfFileExits(csv_name)):
            with open(csv_name,'a') as old_csv:
                writer = csv.writer(old_csv)
                writer.writerow([details["time"], details["transaction"], details["price"], details["cash"], details["coin"], details["networth"]])
        else:
            with open(csv_name, 'w') as new_csv:
                writer = csv.DictWriter(new_csv, keys)
                writer.writeheader()
                writer.writerow(info_dict)
        return csv_name
    
    def WriteLastTransactionJson(self, details):
        if(self.name == "BTC"):
            json_name = self.direc + "Json_Transaction_Data/BTC_Last_Transaction.json"
        elif(self.name == "ETH"):
            json_name = self.direc + "Json_Transaction_Data/ETH_Last_Transaction.json"
        elif(self.name == "LTC"):
            json_name = self.direc + "Json_Transaction_Data/LTC_Last_Transaction.json"
        else:
            print("Invalid currency")
            return
        with open(json_name, "w") as new_json:
            json.dump(details, new_json)
        return json_name

    def isProfitable(self, last_price, current_price, commission, networth):
        previous_commission = commission * last_price
        current_commission = current_price * commission
        total_comm = previous_commission + current_commission
        revenue = current_price - last_price
        profit = revenue - total_comm
        if(profit >= 0):
            # This will make the system only choose profitable transactions
            return True
        else:
            return False