#!/bin/bash
# Author: Ron Haber
# Date: 31.10.2020
# This script will run all of the different collections for other coins

cd /home/pi/CryptoCurrency/
now=$(date)
echo $now

python3 /root/CryptoCurrency/Binance/collect_coin_info.py -d /root/Crypto_Docs/Binance/ -i ADA XRP SXP DOT LINK