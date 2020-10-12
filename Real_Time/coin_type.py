#!/usr/bin/python3

# Author: Ron Haber
# Date: 12.10.2020
# This will create a class for the currency to hold relevant data

import os, sys
import json
import csv
from datetime import datetime
import time
import ast

def convert_timestamp_to_date(timestamp):
    time_holder = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return time_holder

def BuyPercentageCurrency(cash, price, commission):
    percent_currency = amount/price
    return percent_currency

def SellPercentageCurrency(currency, price, commission):
    amount = price*currency
    new_amount = amount * (1.0-2.0*commission)
    return new_amount

class Currency:
    # will add more data as things come up
    def __init__(self, name, data_direc, starting_cash, commission):
        self.name = name
        self.direc = data_direc
        self.current_price = 0 
        self.last_three_prices = [0,0,0] # ltp[0] is current price required to determine 2 first_deriv values
        self.first_deriv = [0,0] # required to determine the second derivative (first_deriv[0] is the important one here)
        self.second_deriv = 0
        self.cash = cash
        self.coin = 0
        self.commission = commission

        self.thresholds = self.GetThresholds()
        self.GetPrices()

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
            data = json_load(json_file)
        thresholds = data["threshold"]
    
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
        for i in range(0,3):
            self.last_three_prices[i] = prices[i]["price"]
        self.current_price = self.last_three_prices[0]
        return self.current_price
        
    def GetBalance(self):
        coin_value = self.coin * self.current_price
        balance = cash + coin_value
        return balance

    def FirstDerivative(self):
        price_holder = self.last_three_prices
        for i in range(0, 2): # only iterate twice
            deriv_holder = price_holder[i] - price_holder[i+1]
            self.first_deriv[i] = deriv_holder
        return self.first_deriv

    def SecondDerivative(self):
        self.second_deriv = self.first_deriv[0] - self.first_deriv[1]
        return self.second_deriv

    def DetermineTradeType(self):
        price = self.GetPrices()
        first_val = self.FirstDerivative()
        second_val = self.SecondDerivative()
        if(self.cash > 0):
            if(first_val[0] < self.thresholds[0] and second_val > self.thresholds[1]):
                self.coin = BuyPercentageCurrency(self.cash, self.current_price, self.commission)
                self.cash = 0
                networth = self.GetBalance()
                detailed = {
                    "time":convert_timestamp_to_date(time.time),
                    "transaction": "bought",
                    "price":self.current_price,
                    "cash":self.cash,
                    "coin":self.coin,
                    "networth":networth
                }
        if(self.coin > 0):
            if(first_val[0] > self.thresholds[2] and second_val > self.thresholds[3]):
                self.cash = SellPercentageCurrency(self.coin, self.current_price, self.commission)
                self.coin = 0
                networth = self.GetBalance()
                detailed = {
                    "time":convert_timestamp_to_date(time.time),
                    "transaction": "sold",
                    "price":self.current_price,
                    "cash":self.cash,
                    "coin":self.coin,
                    "networth":networth
                }
        # Write the info to a csv somewhere
        networth = self.GetBalance()
        return networth