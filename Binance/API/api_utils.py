#!/usr/bin/python3

# Author: Ron Haber
# Date: 30.10.2020
# This script will grab the required API key information

import os

home = "/home/ronhaber/API_Utils/"

def GetAPIKeys(secret_file, public_file):
    with open(secret_file, 'r') as secret:
        secret_key = secret.read()
    with open(public_file, 'r') as public:
        public_key = public.read()
    return public_key, secret_key

