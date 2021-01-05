#!/usr/bin/python3

# Author: Ron Haber
# Date: 19.12.2020
# This script will take an input csv with the desired value within it and plot
# time vs the desired variable. It will save the output image to the defined location

import os, sys
import os.path
import datetime
import csv, argparse
import matplotlib.pyplot as plt
from vispy.plot import Fig

parser = argparse.ArgumentParser(description="Find the ideal thresholds for any currency.")
parser.add_argument("-c", "--excel", type=str, required=True, help="The csv file that will be converted to a database")
parser.add_argument("-v", "--variable", type=str, required=True, help="The name of the target variable")
parser.add_argument("-t", "--target", type=str, required=True, help="The target directory to save the output image")

args = parser.parse_args()
excel = str(args.excel)
variable = str(args.variable)
target_direc = str(args.target)

def CheckIfFileExists(filename):
    # Will also remove the file if it exists
    return os.path.isfile(filename)

def ReadCSV(filename):
    holder = []
    last_values = []
    if(CheckIfFileExists(filename)):
        with open(filename, 'r') as csv_file:
            values = csv.DictReader(csv_file)
            for value in values:
                holder.append(value) # converts to a list appropriately
        size = len(holder) 
        if(size > 60):
            for i in range(size-60, size):
                last_values.append(holder[i])
        else:
            last_values = holder
        return last_values
    else:
        return

def GetXandYValues(csv_data, name):
    x_vector = [] # will always be time
    y_vector = []
    for value in csv_data:
        try:
            y_vector.append(float(value[name])) # conversion required
        except ValueError:
            continue
        x_vector.append(value['time'])
        # x_vector = int(datetime.datetime.timestamp(holder))
    return x_vector, y_vector

def plot(x_vector, y_vector, name, direc, excel):
    plt.plot(x_vector, y_vector)
    plt.xlabel('time')
    plt.ylabel(name)
    plt.xticks([])
    pic_name = (excel.split('/')[-1]).split('.')[0]
    save_name = direc + pic_name + '.png'
    plt.savefig(save_name)


if __name__ == "__main__":
    csv_data = ReadCSV(excel)
    x_vector, y_vector = GetXandYValues(csv_data, variable)
    plot(x_vector, y_vector, variable, target_direc, excel)
