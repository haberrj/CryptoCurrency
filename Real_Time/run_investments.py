#!/usr/bin/python3

# Author: Ron Haber
# Date: 10.10.2020
# This script will execute the appropriate trades based on the algorithm
# and respective data.
# It will also periodically write reports of the holdings

import os, sys
import json
from os.path import expanduser
from datetime import datetime
import derivative_algorithm as da
import coin_type as ct 

def GetThresholds(currency_type):
    direc = expanduser("~") + "/Crypto_Share/Artifacts/Json_Output_Data/"
    if(currency_type.name == "BTC"):
        file_name = direc + "btc_thresholds.json"
    elif(currency_type.name == "ETH"):
        file_name = direc + "eth_thresholds.json"
    elif(currency_type.name == "ETH"):
        file_name = direc + "ltc_thresholds.json"
    else:
        print("Invalid type")
        return
    with open(file_name, 'r') as json_file:
        data = json.load(json_file)
    threshold = data["threshold"]
    return threshold