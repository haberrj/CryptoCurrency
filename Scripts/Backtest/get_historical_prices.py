#!/usr/bin/python3

# Author: Ron Haber
# Date: 6.10.2020
# The purpose of this script to pull historical data for the following crypto-currencies:
# Bitcoin (BTC), Ethereum (ETH), Litecoin (LTC) relative to EUR
# The eventual trajectory of this script will pull fiat currencies too (i.e. USD/EU, CAD/USD, etc.)
import os
import csv
import matplotlib.pyplot as plt
from datetime import datetime

def convert_timestamp_to_date(timestamp):
    time_holder = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return time_holder

class Crypto:
    # This class reads a CSV input and creates a list of dictionaries with the respective price and timestamp
    # There is also a CSV file saved to a desire directory
    def __init__(self, name, history_data, csv_data, json_data):
        self.name = name
        self.history_file = history_data
        self.csv_data = csv_data
        self.json_data = json_data
        # init methods
        self.dict_values = self.decode_csv()
        self.relevant_info = self.format_dict_values()
        self.csv_creation = self.CreateNewCSV()
        
    def decode_csv(self):
        holder = []
        with open(self.history_file) as csvfile:
            history_values = csv.DictReader(csvfile)
            for value in history_values:
                holder.append(value)
        return holder

    def print_dataset_size(self):
        print(len(self.relevant_info))

    def print_1_value(self, index):
        print(self.relevant_info[index])

    def print_all_values(self):
        for row in self.relevant_info:
            print(row)

    def format_dict_values(self):
        holder = []
        for row in self.dict_values:
            sub_dict = { #this will cut the useless info I don't care about
                "timestamp": 0,
                "price": 0
            }
            sub_dict["timestamp"] = int(row['Unix Timestamp'])
            sub_dict["price"] = (float(row["Open"]) + float(row["Close"]))/2.0 #taking the average price for the time frame
            holder.append(sub_dict)
        oldest_to_newest = list(reversed(holder))
        return oldest_to_newest

    def CreateNewCSV(self):
        new_file_name = self.csv_data + self.name + '.csv'
        keys = self.relevant_info[0].keys()
        with open(new_file_name, 'w') as new_file:
            writer = csv.DictWriter(new_file, keys)
            writer.writeheader()
            writer.writerows(self.relevant_info)
        return new_file_name

    def GetCoinPriceList(self):
        return self.relevant_info

    def CreatePriceGraph(self):
        # Beware system requirements may limit this since it is a lot of data to plot
        # set up x & y (timestamp, price)
        x_axis = []
        y_axis = []
        for row in self.relevant_info:
            time_holder = self.convert_timestamp_to_date(row['timestamp'])
            x_axis.append(time_holder)
            y_axis.append(row['price'])
        plt.plot(x_axis, y_axis)
        plt.xlabel('Time/Date')
        plt.ylabel('Price (€)')
        plt.title(self.name)
        plt.show()