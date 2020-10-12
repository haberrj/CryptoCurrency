#!/bin/bash
# Author: Ron Haber
# Date: 10.10.2020
# This script will run all of the different threshold executions for the
# different currencies.
# The inputs will be the thresholds themselves.

# cd /home/pi/CryptoCurrency/
# git pull


python3 /home/ronhaber/CryptoCurrency/Real_Time/Real_Time_Test/threshold_executer.py -c 1000.00 -i BTC -t 300 10 10 10 -p 0.00 &
P1=$!
python3 /home/ronhaber/CryptoCurrency/Real_Time/Real_Time_Test/threshold_executer.py -c 1000.00 -i LTC -t 300 10 10 10 -p 0.00 &
P2=$!
python3 /home/ronhaber/CryptoCurrency/Real_Time/Real_Time_Test/threshold_executer.py -c 1000.00 -i ETH -t 300 10 10 10 -p 0.00 &
P3=$!
wait $P1 $P2 $P3