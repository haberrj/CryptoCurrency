#!/usr/bin/python3

# Author: Ron Haber
# Date: 17.12.2020
# This script will execute the other python file since the shell script doesn't seem to work

import os, sys
import time

os.system("/etc/init.d/apache2 restart")

while(True):
    os.system("python3  /scripts/Backend/python/create_sqldb.py -c /database_files/Binance/Actual/CSV_Transactions/BTC_transactions.csv -n BTC_Transactions")
    os.system("python3  /scripts/Backend/python/create_sqldb.py -c /database_files/Binance/Actual/CSV_Transactions/ETH_transactions.csv -n ETH_Transactions")
    os.system("python3  /scripts/Backend/python/create_sqldb.py -c /database_files/Binance/Actual/CSV_Transactions/LTC_transactions.csv -n LTC_Transactions")
    os.system("python3  /scripts/Backend/python/create_sqldb.py -c /database_files/Binance/Actual/CSV_Transactions/BNB_transactions.csv -n BNB_Transactions")
    # Prices
    os.system("python3  /scripts/Backend/python/create_sqldb.py -c /database_files/Binance/BTC_Realtime.csv -n BTC_Realtime")
    os.system("python3  /scripts/Backend/python/create_sqldb.py -c /database_files/Binance/ETH_Realtime.csv -n ETH_Realtime")
    os.system("python3  /scripts/Backend/python/create_sqldb.py -c /database_files/Binance/LTC_Realtime.csv -n LTC_Realtime")
    os.system("python3  /scripts/Backend/python/create_sqldb.py -c /database_files/Binance/BNB_Realtime.csv -n BNB_Realtime")
    # Cash
    os.system("python3  /scripts/Backend/python/create_sqldb.py -c /database_files/Binance/Actual/Balances/BTC_Balance.csv -n BTC_Balance")
    os.system("python3  /scripts/Backend/python/create_sqldb.py -c /database_files/Binance/Actual/Balances/ETH_Balance.csv -n ETH_Balance")
    os.system("python3  /scripts/Backend/python/create_sqldb.py -c /database_files/Binance/Actual/Balances/LTC_Balance.csv -n LTC_Balance")
    os.system("python3  /scripts/Backend/python/create_sqldb.py -c /database_files/Binance/Actual/Balances/BNB_Balance.csv -n BNB_Balance")
    print("Complete!")
    time.sleep(30) # sleep for 30 seconds before executing