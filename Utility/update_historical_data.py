#!/usr/bin/python3

# Author: Ron Haber
# Date: 6.10.2020
# This script will access Kraken historical data for updating backtesting
# https://www.cryptodatadownload.com/data/kraken/

import os, sys
import requests
from os.path import expanduser
import argparse

def DeleteFirstRowOfCSV(holder_filename, filename):
    with open(holder_filename, 'r') as f:
        with open(filename, 'w') as f1:
            next(f) # skips the header
            for line in f:
                f1.write(line)
    os.remove(holder_filename)

parser = argparse.ArgumentParser(description="Download the required csv files.")
parser.add_argument("-c", "--currency", type=str, required=True, help="The type of currency (BTC, ETH, LTC)")
args = parser.parse_args()

currency = (args.currency).upper()
src_url = "https://www.cryptodatadownload.com/cdd/"
home = "/media/pi/server/"
file_destination = home + "Crypto_Share/Artifacts/Historical_Price_Docs/"

if(currency == "BTC"):
    csv_name = "Kraken_BTCEUR_1h.csv"
    url = src_url + csv_name
    holder_file = file_destination + "holder" + csv_name
    file_destination = file_destination + csv_name
    r = requests.get(url, verify=False)
    open(holder_file, 'wb').write(r.content)
    DeleteFirstRowOfCSV(holder_file, file_destination)
elif(currency == "ETH"):
    csv_name = "Kraken_ETHEUR_1h.csv"
    url = src_url + csv_name
    holder_file = file_destination + "holder" + csv_name
    file_destination = file_destination + csv_name
    r = requests.get(url, verify=False)
    open(holder_file, 'wb').write(r.content)
    DeleteFirstRowOfCSV(holder_file, file_destination)
elif(currency == "LTC"):
    csv_name = "Kraken_LTCEUR_1h.csv"
    url = src_url + csv_name
    holder_file = file_destination + "holder" + csv_name
    file_destination = file_destination + csv_name
    r = requests.get(url, verify=False)
    open(holder_file, 'wb').write(r.content)
    DeleteFirstRowOfCSV(holder_file, file_destination)
else:
    print("Invalid input")
    sys.exit()
print("Download of " + csv_name + " is complete!")