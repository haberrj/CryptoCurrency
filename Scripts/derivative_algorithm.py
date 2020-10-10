#!/usr/bin/python3

# Author: Ron Haber
# Date: 6.10.2020
# The purpose of the is script is to implement the algorithm for determining investment strategy
# The algorithm with consist of taking the first and second derivative of the respective curves.
# The 1st derivative will provide the user with the speed at which price changes are occurring
# i.e. whether it is moving up, peaking, moving down, or flooring
# The 2nd derivative will provide the user with the acceleration at which the price is changing
# i.e. degree to which it is increasing or decreasing
# Class structures will not be implemented as this meant to be usable functions

import os
import csv
import get_historical_prices as ghp

def FirstDerivative2Data(dataset):
    # dataset is a list of dicts relevant to a specific currency
    # The dict should consist of timestamp and price values
    # Will begin with a derivative of between 2 data points
    first_derivative = []
    data_size = len(dataset)
    for i in range(1, data_size):
        deriv_holder = dataset[i]["price"] - dataset[i-1]["price"]
        sub_dict = {
            "time":dataset[i]["timestamp"],
            "price_deriv":deriv_holder
        }
        first_derivative.append(sub_dict)
    return first_derivative

def SecondDerivative2Data(first_deriv):
    # first_deriv is a list of price derivatives
    # Will begin with the 2nd derivative of every 2 data points
    second_derivative = []
    data_size = len(first_deriv)
    for i in range(1, data_size):
        deriv_holder = first_deriv[i]["price_deriv"] - first_deriv[i-1]["price_deriv"]
        sub_dict = {
            "time":first_deriv[i]["time"],
            "price_deriv":deriv_holder
        }
        second_derivative.append(sub_dict)
    return second_derivative

def BuyPercentageCurrency(amount, price, commission):
    # amount is the amount of money the user can spend
    # price is the current price of the currency
    # will return a float of currency repping a percentage (e.g. 0.75 BTC)
    percent_currency = amount/price
    return percent_currency

def SellPercentageCurrency(currency, price, commission):
    # currency is the amount of currency (e.g. 0.75 BTC)
    # price is the current price of the currency
    # will return a float of the amount of money the currency was worth (e.g. 9000.58€)
    amount = price*currency
    new_amount = amount * (1.0-2.0*commission)
    return new_amount

def TradingCurrency(price_data, first_deriv, second_deriv, starting_amount, commission, thresholds):
    # Thresholds are the thresholds for buying and selling
    # Since buy and selling separately wasn't realistic let's try it a different way
    # I will have a starting amount that will change as things are bought and sold
    # I can see what the end outcome is at the very end as well as logging amounts as
    # time progresses to see what happened
    #thresholds
    first_buy_thresh = thresholds[0]
    first_sell_thresh = thresholds[1]
    second_buy_thresh = thresholds[2]
    second_sell_thresh = thresholds[3]
    
    net = [0.0, 0.0, 0.0, 0.0] # captial gains for each respective year
    tax_applied = [False, False, False, False]
    income_tax_percent = 0.42 # 42% income tax
    last_buy_price = 0.0
    cash = starting_amount
    wallet = 0 # number of coins in possession
    transaction_data = []
    data_len = len(second_deriv)

    for i in range(0, data_len):
        time = price_data[i+2]["timestamp"]
        price = price_data[i+2]["price"]
        first_val = first_deriv[i+1]["price_deriv"]
        second_val = second_deriv[i]["price_deriv"]
        # Buy 
        # I will assume that I will always spend everything
        if(cash > 0): # >0 since I have no idea if I'll be negative
            if(first_val < first_buy_thresh and second_val > second_buy_thresh):
                wallet = BuyPercentageCurrency(cash, price, commission)
                cash = 0
                detailed = {
                    "time":ghp.convert_timestamp_to_date(time),
                    "transaction": "bought",
                    "price":price,
                    "cash":cash,
                    "coin":wallet,
                    "networth":SellPercentageCurrency(wallet, price, commission)
                }
                last_buy_price = price
                transaction_data.append(detailed)
        if(wallet > 0):
            if(first_val > first_sell_thresh and second_val < second_sell_thresh):
                cash = SellPercentageCurrency(wallet, price, commission)
                wallet = 0
                detailed = {
                    "time":ghp.convert_timestamp_to_date(time),
                    "transaction": "sold",
                    "price":price,
                    "cash":cash,
                    "coin":wallet,
                    "networth": cash
                }
                if("2017" in detailed["time"]):
                    net[0] = net[0] + (price - last_buy_price)
                elif("2018" in detailed["time"]):
                    net[1] = net[1] + (price - last_buy_price)
                elif("2019" in detailed["time"]):
                    net[2] = net[2] + (price - last_buy_price)
                elif("2020" in detailed["time"]):
                    net[3] = net[3] + (price - last_buy_price)
                transaction_data.append(detailed)
    final = transaction_data[-1]["networth"]
    return transaction_data, final, net