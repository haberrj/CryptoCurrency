#!/bin/bash
# Author: Ron Haber
# Date: 14.11.2020
# This will execute the price collection and currency trading for Binance

cd /home/pi/CryptoCurrency/
now=$(date)
echo $now
git pull

python3 /home/pi/CryptoCurrency/Binance/bin_actual_investments.py -d /media/pi/HaberServer/Crypto_Share/Binance/ -i BTC ETH LTC BNB -r 1

# conversione to db files

# Transaction Data
python3 /home/pi/CryptoCurrency/Utility/create_sqldb.py -c /media/pi/HaberServer/Crypto_Share/Binance/Actual/CSV_Transactions/BTC_transactions.csv -n BTC_Transactions
python3 /home/pi/CryptoCurrency/Utility/create_sqldb.py -c /media/pi/HaberServer/Crypto_Share/Binance/Actual/CSV_Transactions/ETH_transactions.csv -n ETH_Transactions
python3 /home/pi/CryptoCurrency/Utility/create_sqldb.py -c /media/pi/HaberServer/Crypto_Share/Binance/Actual/CSV_Transactions/LTC_transactions.csv -n LTC_Transactions
python3 /home/pi/CryptoCurrency/Utility/create_sqldb.py -c /media/pi/HaberServer/Crypto_Share/Binance/Actual/CSV_Transactions/BNB_transactions.csv -n BNB_Transactions
# Price Data
python3 /home/pi/CryptoCurrency/Utility/create_sqldb.py -c /media/pi/HaberServer/Crypto_Share/Binance/BTC_Realtime.csv -n BTC_Realtime
python3 /home/pi/CryptoCurrency/Utility/create_sqldb.py -c /media/pi/HaberServer/Crypto_Share/Binance/ETH_Realtime.csv -n ETH_Realtime
python3 /home/pi/CryptoCurrency/Utility/create_sqldb.py -c /media/pi/HaberServer/Crypto_Share/Binance/LTC_Realtime.csv -n LTC_Realtime
python3 /home/pi/CryptoCurrency/Utility/create_sqldb.py -c /media/pi/HaberServer/Crypto_Share/Binance/BNB_Realtime.csv -n BNB_Realtime
# Cash Data
python3 /home/pi/CryptoCurrency/Utility/create_sqldb.py -c /media/pi/HaberServer/Crypto_Share/Binance/Actual/Balances/BTC_Balance.csv -n BTC_Balance
python3 /home/pi/CryptoCurrency/Utility/create_sqldb.py -c /media/pi/HaberServer/Crypto_Share/Binance/Actual/Balances/ETH_Balance.csv -n ETH_Balance
python3 /home/pi/CryptoCurrency/Utility/create_sqldb.py -c /media/pi/HaberServer/Crypto_Share/Binance/Actual/Balances/LTC_Balance.csv -n LTC_Balance
python3 /home/pi/CryptoCurrency/Utility/create_sqldb.py -c /media/pi/HaberServer/Crypto_Share/Binance/Actual/Balances/BNB_Balance.csv -n BNB_Balance