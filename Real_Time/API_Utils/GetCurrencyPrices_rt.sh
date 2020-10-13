#!/bin/bash
# Author: Ron Haber
# Date: 10.10.2020
# This will call the API periodically to get each type of currency's
# price data.

cd /home/pi/CryptoCurrency/
git pull

# Get price info from the ticker
python3 /home/pi/CryptoCurrency/Real_Time/API_Utils/krakenapi.py Ticker pair=xbteur
sleep 0.1
python3 /home/pi/CryptoCurrency/Real_Time/API_Utils/krakenapi.py Ticker pair=etheur
sleep 0.1
python3 /home/pi/CryptoCurrency/Real_Time/API_Utils/krakenapi.py Ticker pair=ltceur
sleep 0.1

python3 /home/pi/CryptoCurrency/Real_Time/run_investments.py -i BTC -p 0.0
sleep 0.1
python3 /home/pi/CryptoCurrency/Real_Time/run_investments.py -i ETH -p 0.0
sleep 0.1
python3 /home/pi/CryptoCurrency/Real_Time/run_investments.py -i LTC -p 0.0
sleep 0.1