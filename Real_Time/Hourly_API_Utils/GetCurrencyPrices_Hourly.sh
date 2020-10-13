#!/bin/bash
# Author: Ron Haber
# Date: 13.10.2020
# This will call the API periodically to get each type of currency's
# price data. (Hourly to be called by the API hourly)

cd /home/pi/CryptoCurrency/
git pull

# Get price info from the ticker
python3 /home/pi/CryptoCurrency/Real_Time/Hourly_API_Utils/krakenapi.py Ticker pair=xbteur
sleep 0.1
python3 /home/pi/CryptoCurrency/Real_Time/Hourly_API_Utils/krakenapi.py Ticker pair=etheur
sleep 0.1
python3 /home/pi/CryptoCurrency/Real_Time/Hourly_API_Utils/krakenapi.py Ticker pair=ltceur
sleep 0.1

python3 /home/pi/CryptoCurrency/Real_Time/run_investments.py -d /media/pi/HaberServer/Crypto_Share/Real_Time_Artifacts/Hourly/ -i BTC -p 0.0
sleep 0.1
python3 /home/pi/CryptoCurrency/Real_Time/run_investments.py -d /media/pi/HaberServer/Crypto_Share/Real_Time_Artifacts/Hourly/ -i ETH -p 0.0
sleep 0.1 
python3 /home/pi/CryptoCurrency/Real_Time/run_investments.py -d /media/pi/HaberServer/Crypto_Share/Real_Time_Artifacts/Hourly/ -i LTC -p 0.0
sleep 0.1