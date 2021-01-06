#!/usr/bin/python3

# Author: Ron Haber
# Date: 12.12.2020
# This script will take an input csv file and create a database for it
# This will only work for the individual transaction files

import os, sys
import os.path
import sqlite3, csv
import argparse

parser = argparse.ArgumentParser(description="Find the ideal thresholds for any currency.")
parser.add_argument("-c", "--excel", type=str, required=True, help="The csv file that will be converted to a database")
parser.add_argument("-n", "--name", type=str, required=True, help="The name of the target database")

args = parser.parse_args()
excel = str(args.excel)
name = str(args.name) + ".db"
direc = "/root/Crypto_Share/Binance/Databases/"

def CheckIfFileExists(filename):
    # Will also remove the file if it exists
    return os.path.isfile(filename)

def CreateNewDB(value):
    new_db = direc + value
    print(value)
    with open(new_db, "w") as new_file:
        print("New DB file created at: ", new_db)
    return new_db

# For transactions
def PopulateNewTransactionsDB(db_file, csv_data):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("CREATE TABLE transactions (time, name, id, price, status, coin, type);")
    cur.executemany("INSERT INTO transactions (time, name, id, price, status, coin, type) VALUES(?, ?, ?, ?, ?, ?, ?);", csv_data)
    con.commit()
    con.close()

def AppendTransactionsDB(db_file, csv_data):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("INSERT INTO transactions (time, name, id, price, status, coin, type) VALUES(?, ?, ?, ?, ?, ?, ?);", csv_data)
    con.commit()
    con.close()

def ReadAllValuesFromTransactionsCSV(csv_file):
    with open(csv_file, "r") as data_file:
        data = csv.DictReader(data_file)
        to_db = [(i['time'], i['name'], i['id'], i['price'], i['status'], i['coin'], i['type']) for i in data]
    return to_db

def ReadMostRecentValueFromTransactionsCSV(csv_file):
    csv_data = ReadAllValuesFromTransactionsCSV(csv_file)
    relevant_data = csv_data[-1]
    return relevant_data

def CheckIfValueIsAlreadyWrittenTransactions(csv_data, db_file):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    result = cur.execute("SELECT * FROM transactions").fetchall()[-1]
    cur.close()
    if(csv_data[0] == result[0]):
        print("Value already exists")
        return True
    else:
        print("Adding new data")
        return False

# For realtime prices
def PopulateNewPricesDB(db_file, csv_data):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("CREATE TABLE prices (time, name, price, bid, ask);")
    cur.executemany("INSERT INTO prices (time, name, price, bid, ask) VALUES(?, ?, ?, ?, ?);", csv_data)
    con.commit()
    con.close()

def AppendPricesDB(db_file, csv_data):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("INSERT INTO prices (time, name, price, bid, ask) VALUES(?, ?, ?, ?, ?);", csv_data)
    con.commit()
    con.close()

def ReadAllValuesFromPricesCSV(csv_file):
    with open(csv_file, "r") as data_file:
        data = csv.DictReader(data_file)
        to_db = [(i['time'], i['name'], i['price'], i['bid'], i['ask']) for i in data]
    return to_db

def ReadMostRecentValueFromPricesCSV(csv_file):
    csv_data = ReadAllValuesFromPricesCSV(csv_file)
    relevant_data = csv_data[-1]
    return relevant_data

def CheckIfValueIsAlreadyWrittenPrices(csv_data, db_file):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    result = cur.execute("SELECT * FROM prices").fetchall()[-1]
    cur.close()
    if(csv_data[0] == result[0]):
        print("Value already exists")
        return True
    else:
        print("Adding new data")
        return False

# For cash balances
def PopulateNewCashDB(db_file, csv_data):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("CREATE TABLE cash (time, name, cash);")
    cur.executemany("INSERT INTO cash (time, name, cash) VALUES(?, ?, ?);", csv_data)
    con.commit()
    con.close()

def AppendCashDB(db_file, csv_data):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("INSERT INTO cash (time, name, cash) VALUES(?, ?, ?);", csv_data)
    con.commit()
    con.close()

def ReadAllValuesFromCashCSV(csv_file):
    with open(csv_file, "r") as data_file:
        data = csv.DictReader(data_file)
        to_db = [(i['time'], i['name'], i['cash']) for i in data]
    return to_db

def ReadMostRecentValueFromCashCSV(csv_file):
    csv_data = ReadAllValuesFromCashCSV(csv_file)
    relevant_data = csv_data[-1]
    return relevant_data

def CheckIfValueIsAlreadyWrittenCash(csv_data, db_file):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    result = cur.execute("SELECT * FROM cash").fetchall()[-1]
    cur.close()
    if(csv_data[0] == result[0]):
        print("Value already exists")
        return True
    else:
        print("Adding new data")
        return False

# Execution functions
def TransactionsExecution(db_direc, data_file):
    if(CheckIfFileExists(db_direc)):
        try:
            csv_data = ReadMostRecentValueFromTransactionsCSV(data_file)
        except FileNotFoundError:
            print("CSV file not found")
            sys.exit()
        check = CheckIfValueIsAlreadyWrittenTransactions(csv_data, db_direc)
        if(check):
            sys.exit()
        else:
            AppendTransactionsDB(db_direc, csv_data)
    else:
        new_db = CreateNewDB(name)
        print(new_db)
        csv_data = ReadAllValuesFromTransactionsCSV(data_file)
        PopulateNewTransactionsDB(new_db, csv_data)

def PricesExecution(db_direc, data_file):
    if(CheckIfFileExists(db_direc)):
        try:
            csv_data = ReadMostRecentValueFromPricesCSV(data_file)
        except FileNotFoundError:
            print("CSV file not found")
            sys.exit()
        check = CheckIfValueIsAlreadyWrittenPrices(csv_data, db_direc)
        if(check):
            sys.exit()
        else:
            AppendPricesDB(db_direc, csv_data)
    else:
        new_db = CreateNewDB(name)
        print(new_db)
        csv_data = ReadAllValuesFromPricesCSV(data_file)
        PopulateNewPricesDB(new_db, csv_data)

def CashExecution(db_direc, data_file):
    if(CheckIfFileExists(db_direc)):
        try:
            csv_data = ReadMostRecentValueFromCashCSV(data_file)
        except FileNotFoundError:
            print("CSV file not found")
            sys.exit()
        check = CheckIfValueIsAlreadyWrittenCash(csv_data, db_direc)
        if(check):
            sys.exit()
        else:
            AppendCashDB(db_direc, csv_data)
    else:
        new_db = CreateNewDB(name)
        print(new_db)
        csv_data = ReadAllValuesFromCashCSV(data_file)
        PopulateNewCashDB(new_db, csv_data)

if __name__ == "__main__":
    db_direc = direc + name
    print(excel)
    if("Transaction" in name):
        TransactionsExecution(db_direc, excel)
    elif("Balance" in name):
        CashExecution(db_direc, excel)
    elif("Realtime" in name):
        PricesExecution(db_direc, excel)
    else:
        "Not a valid csv input"
        sys.exit()
