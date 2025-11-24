# dir_parser.py
# Matthew Harris
# 241ADB166
# 11 November, 2025
# GitHub repo: https://github.com/mgharris97/programming-languages/tree/main/lab-2

import glob
from csv_parser import csv_parse
import csv 
import os


def dir_parse(dir_path):
    files = glob.glob(dir_path + "/*.csv")

    valid_flights = []
    errors = []

    if not files:
        #f.write(f"No CSV files were found in: {dir_path}\n\n")
        print (f"No CSV files in {dir_path}")
        errors.append(f"No CSV files were found in: {dir_path} ")
        return valid_flights, errors
        #Take one file at a time and if it ends with .csv -> send to csv_parse
    
    for i in files:

        if i.endswith(".csv"):
            print(f"Parsing: {i}")
            valid, err = csv_parse(i)
            valid_flights.extend(valid)
            errors.extend(err)
    return valid_flights, errors
               #print(j + '\n')   
         
