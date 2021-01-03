#!/usr/bin/python3
# Author: Ron Haber
# Date: 10.10.2020
# For updating the thresholds for Bitcoin
# Later for updating the price amount

import sys
import json
import argparse
from datetime import datetime
from os.path import expanduser
import threshold_calculator as tc
import derivative_algorithm as da
import get_historical_prices as ghp 

parser = argparse.ArgumentParser(description="Find the ideal thresholds for any currency.")
parser.add_argument("-c", "--cash", type=float, required=True, help="The amount of starting cash")
parser.add_argument("-i", "--currency", type=str, required=True, help="The type of currency (BTC, ETH, LTC)")
parser.add_argument("-t", "--threshold_limits", type=int, nargs=4, required=True, help="The 4 threshold limits for the algorithm")
parser.add_argument("-p", "--commission", type=float, required=True, help="The commission percentage taken by the broker")
args = parser.parse_args()

def CurrencyExecution(currency_type, price_path, csv_path, json_path, cash, commission, threshold_limits):
    if(currency_type == "BTC"):
        price_path = price_path + "Kraken_BTCEUR_1h.csv"
        json_path = json_path + "btc_thresholds.json" # Use the multiple jsons for now but need to fix later into 1 big one
        Coin = ghp.Crypto("Bitcoin_Hourly", price_path, csv_path, json_path)
        commission = 0 # Since there is a problem with entering a comission but seems to be only for bitcoin
    elif(currency_type == "ETH"):
        price_path = price_path + "Kraken_ETHEUR_1h.csv"
        json_path = json_path + "eth_thresholds.json"
        Coin = ghp.Crypto("Ethereum_Hourly", price_path, csv_path, json_path)
    elif(currency_type == "LTC"):
        price_path = price_path + "Kraken_LTCEUR_1h.csv"
        json_path = json_path + "ltc_thresholds.json"
        Coin = ghp.Crypto("Litecoin_Hourly", price_path, csv_path, json_path)
    else:
        print("Invalid currency")
        sys.exit()
    threshold_array, wallet_array = tc.CalculateThresholds(Coin, cash, commission, 
                                    threshold_limits[0], threshold_limits[1], threshold_limits[2], threshold_limits[3])
    max_threshold, max_amount = tc.GetMaxThreshold(threshold_array, wallet_array)
    WriteInfoToJson(Coin, max_threshold, max_amount, json_path)
    return max_threshold, max_amount, json_path

def WriteInfoToJson(coin_type, threshold_data, max_amount, json_path):
    data_dict = {
        "coin_name": coin_type.name,
        "threshold": threshold_data,
        "max_amount": max_amount,
        "date": datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    }
    with open(json_path, "w") as json_file:
        json.dump(data_dict, json_file) # This way only 1 entry every time... will be easier to track
    print("JSON updated at ", json_path)

if __name__ == "__main__":
    home = "/media/pi/HaberServer/Crypto_Share/Artifacts/"
    price_path = home + "Historical_Price_Docs/"
    csv_path = home + "CSV_Output_Data/"
    json_path = home + "Json_Output_Data/"
    threshold_limits = args.threshold_limits
    cash = args.cash
    currency_type = (args.currency).upper()
    commission = args.commission
    threshold, amount, json_file = CurrencyExecution(currency_type, price_path, csv_path, json_path, cash, commission, threshold_limits)
    print("The ideal thresholds are: ", threshold)
    print("That will produce a max amount of: ", "{:,.2f}".format(amount), "€")

    