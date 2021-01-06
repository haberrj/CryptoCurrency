#!/bin/bash
# Author: Ron Haber
# Date: 31.10.2020
# This script will run all of the different collections for other coins

cd /home/haberrj/CryptoCurrency/
now=$(date)
echo $now

python3 /home/haberrj/CryptoCurrency/Binance/collect_coin_info.py -d /home/haberrj/Crypto_Share/Binance/ -i ADA XRP SXP DOT LINK