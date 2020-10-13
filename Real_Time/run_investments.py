#!/usr/bin/python3

# Author: Ron Haber
# Date: 10.10.2020
# This script will execute the appropriate trades based on the algorithm
# and respective data.
# It will also periodically write reports of the holdings

import os, sys
import json
import argparse
import subprocess
from datetime import datetime
import coin_type as ct 

# home = "/home/ronhaber/Documents/Crypto_Docs/"
# home = "/media/pi/HaberServer/Crypto_Share/Real_Time_Artifacts/"

parser = argparse.ArgumentParser(description="Find the ideal thresholds for any currency.")
parser.add_argument("-d", "--home", type=str, required=True, help="The directory for artifacts")
parser.add_argument("-i", "--currency", type=str, required=True, help="The type of currency (BTC, ETH, LTC)")
parser.add_argument("-p", "--commission", type=float, required=True, help="The commission percentage taken by the broker")

args = parser.parse_args()
home = str(args.home)
currency_name = str(args.currency).upper()
commission = float(args.commission)

crypto_curr = ct.Currency(currency_name, home, commission)
networth = crypto_curr.DetermineTradeType()
print('Current Networth is: ', networth, ' €')


