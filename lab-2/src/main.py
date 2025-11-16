# main.py
# Matthew Harris
# 241ADB166
# 11 November, 2025
# GitHub repo: https://github.com/mgharris97/programming-languages/tree/main/lab-2

import argparse
import csv
import os
import json
from csv_parser import csv_parse
from dir_parser import dir_parse


def main():
    ##Adding arguments to the Argument Parser
    ##Specifying metavar display name for arguments to be empty to avoid --INPUT, etc.
    parser = argparse.ArgumentParser(description="Flight Schedule Parser and Query Tool")
    parser.add_argument("-i", "--input", metavar="", help="Parse a single CSV file. Format: -i path/to/file.csv")
    parser.add_argument("-d", "--directory", metavar="", help="Parse all .csv files in a folder and combine results. Format: -d path/to/folder/")
    parser.add_argument("-o", "--output", metavar="", help="Optional custom output path for valid flights JSON. Format: -o path/to/output.json")
    parser.add_argument("-j","--json", metavar="", help="Load existing JSON database instead of parsing CSVs. Format: -j path/to/db.json")
    parser.add_argument("-q", "--query", metavar="", help="Execute queries defined in a JSON file on the loaded database. Format: -q path/to/query.json	")
    args = parser.parse_args()
    single_file_path = None
    dir_path = None
    json_path = None
    
    if args.input:
        single_file_path = args.input
        valid, error = csv_parse(single_file_path) #implement parse_directory
        with open("Errors.txt", 'a') as f:
            f.write(f"===Start of file [{os.path.basename(single_file_path)}]===\n")
            for i in error:
                f.write(i + "\n")
            f.write(f"===End of file [{os.path.basename(single_file_path)}]===\n\n")
    elif args.directory:
        dir_path = args.directory
        dir_parse(dir_path)
    elif args.json:
        with open(args.json, 'r') as f:
            valid_flights = json.load(f)
        for i in valid_flights:
            print (i)
    else:
        print("No input file or directory specified")


    if args.output:
        json_out_path = args.output
        with open(json_out_path, mode = 'w') as json_file:
            json.dump(valid, json_file, indent=2)



#call to main()    
if __name__ == "__main__":
    main()

