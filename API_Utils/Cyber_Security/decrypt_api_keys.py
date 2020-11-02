#!/usr/bin/python3

# Author: Ron Haber
# Date 2.11.2020
# Used to decrypt the api keys so they arent saved in plain text

import os, sys
import key_operations as ko

def ReadEncryptedAPIKey(api_key):
    with open(api_key, "rn") as api:
        api_value = api.read()
    return api_value

def DecryptAPIKey(key_file, api):
    key = ko.LoadKey(key_file)
    decoded_api = ko.Decode(key, api)
    return decoded_api

def GetAPIKey(key_file, api_file):
    api = ReadEncryptedAPIKey(api_file)
    decoded_api = DecryptAPIKey(key_file, api)