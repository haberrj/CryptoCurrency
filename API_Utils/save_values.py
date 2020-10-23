#!/usr/bin/python3
# Author: Ron Haber
# Date: 11.10.2020
# This script will save the outputs from the API calls into json or csv files

import os, sys
import os.path
import json, csv
from datetime import datetime
import time
import ast

home = "/media/pi/HaberServer/Crypto_Share/Real_Time_Artifacts/" # This will change going forward but stays for testing

def SaveToFileType(arg_list, api_reply):
    api_dict = ast.literal_eval(api_reply)
    arg_size = len(arg_list)
    if(arg_size < 2):
        # Do nothing
        return
    arg_dict = {
        "call_name": str(arg_list[1]),
        "parameters": [],
        "type":'', # this will be public, private, trading, or funding
        "time":int(time.time())
    }
    if(arg_size > 2):
        for i in range(2, arg_size):
            arg_dict["parameters"].append(str(arg_list[i]))
    if((arg_dict["call_name"] == "Time") or (arg_dict["call_name"] == "Ticker")):
        arg_dict["type"] = "public"
        filename = WriteToCSV(arg_dict, api_dict)
    elif((arg_dict["call_name"] == "Balance") or (arg_dict["call_name"] == "TradeBalance")):
        arg_dict["type"] = "private"
        filename = WriteToCSV(arg_dict, api_dict)
    elif((arg_dict["call_name"] == "AddOrder") or (arg_dict["call_name"] == "CancelOrder")):
        arg_dict["type"] = "trading"
        filename = MadeOrdersJSON(arg_dict, api_dict)
    else:
        arg_dict["type"] = "funding"
        filename = ""
    return filename

def CheckIfFileExits(filename):
    return os.path.isfile(filename)

def WriteToCSV(arg_dict, dataset):
    name = arg_dict["call_name"]
    if(name == "Ticker"):
        csv_file = TickerCSV(arg_dict, dataset)
    elif(name == "Balance"):
        csv_file = OtherCSV(arg_dict, dataset, name)
    elif(name == "TradeBalance"):
        csv_file = OtherCSV(arg_dict, dataset, name)
    else: # Don't care otherwise
        return
    return csv_file

def TickerCSV(arg_dict, dataset):
    new_pair = ""
    ticker = ""
    pair = arg_dict["parameters"][0]
    if("xbteur" in pair):
        new_pair = "BTC_Realtime"
        ticker = "XXBTZEUR"
    elif("etheur" in pair):
        new_pair = "ETH_Realtime"
        ticker = "XETHZEUR"
    elif("ltceur" in pair):
        new_pair = "LTC_Realtime"
        ticker = "XLTCZEUR"
    else:
        print("Invalid currency")
        return
    info_dict = {
        "time" : arg_dict["time"],
        "readable_time" : convert_timestamp_to_date(arg_dict["time"]),
        "currency" : new_pair,
        "ticker": ticker,
        "price" : float(dataset["result"][ticker]["b"][0]) # gets the bid price
    }
    csv_name = home + new_pair + ".csv"
    keys = info_dict.keys()
    if(CheckIfFileExits(csv_name)):
        with open(csv_name,'a') as old_csv:
            writer = csv.writer(old_csv)
            writer.writerow([info_dict["time"], info_dict["readable_time"], info_dict["currency"], info_dict["ticker"], info_dict["price"]])
    else:
        with open(csv_name, 'w') as new_csv:
            writer = csv.DictWriter(new_csv, keys)
            writer.writeheader()
            writer.writerow(info_dict)
    return csv_name

def OtherCSV(arg_dict, dataset, name):
    reduced_dict = dataset["result"]
    holder_dict = {
        "time" : arg_dict["time"],
        "readable_time" : convert_timestamp_to_date(arg_dict["time"])
    }
    new_dict = {**holder_dict, **reduced_dict}
    csv_name = home + name + ".csv"
    keys = new_dict.keys()
    if(CheckIfFileExits(csv_name)):
        write_list = []
        for key, value in dict.iteritems():
            temp = value
            write_list.append(temp)
        with open(csv_name,'a') as old_csv:
            writer = csv.writer(old_csv)
            old_csv.write(write_list)
    else:
        with open(csv_name, 'w') as new_csv:
            writer = csv.DictWriter(new_csv, keys)
            writer.writeheader()
            new_csv.writerow(info_dict)
    return csv_name

def MadeOrdersJSON(arg_dict, dataset):
    info_dict = {
        "time" : arg_dict["time"],
        "readable_time" : convert_timestamp_to_date(arg_dict["time"]),
        "name" : arg_dict["call_name"],
        "currency" : arg_dict["parameters"][0].split('=')[-1],
        "type" : arg_dict["parameters"][1].split('=')[-1],
        "ordertype" : arg_dict["parameters"][2].split('=')[-1],
        "volume" : arg_dict["parameters"][3].split('=')[-1],
        "description" : dataset['result']['descrip']['order'],
        "id" : dataset['result']['txid']
    }
    json_name = home + str(info_dict["currency"]) + ".json" 
    if(CheckIfFileExits(json_name)):
        with open(json_name, 'r+') as json_file:
            holder = json.load(json_file)
            holder.update(info_dict)
            json.dump(holder, json_file)
    else:
        with open(json_name, 'w') as json_file:
            json.dump(info_dict, json_file)
    return json_name   

def convert_timestamp_to_date(timestamp):
    time_holder = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return time_holder