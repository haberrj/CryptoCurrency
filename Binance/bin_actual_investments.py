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
parser.add_argument("-p", "--commission", type=float, required=True, help="The commission percentage taken by the broker")
parser.add_argument("-t", "--test", type=int, required=True, help="Should the program run a demo on the prices, 1 to execute, 0 for just prices")

args = parser.parse_args()
home = str(args.home)
currencies = args.currencies
commission = float(args.commission)
test = bool(args.test)
names = []
for name in currencies:
    names.append(str(name).upper())

if __name__ == "__main__":
    API_key_direc = "/media/pi/HaberServer/Crypto_Share/API_Utils/Binance/"
    # client = au.API_Client(API_key_direc, False)
    # info = bri.GetCoinInfo(client, names)
    print("Works")