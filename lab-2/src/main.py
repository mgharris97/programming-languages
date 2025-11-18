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
    
    valid_flights = []
    errors = []

    #---------------------------------------------
    # -i: parse 1 csv file
    #---------------------------------------------
    if args.input:
        single_file_path = args.input
        valid, error = csv_parse(single_file_path) #implement parse_directory
        valid_flights = valid
        errors = error
        with open("Errors.txt", 'a') as f:
            f.write(f"===Start of file [{os.path.basename(single_file_path)}]===\n")
            for i in error:
                f.write(i + "\n")
            f.write(f"===End of file [{os.path.basename(single_file_path)}]===\n\n")

    #---------------------------------------------
    # -d: parse a directory of csv files
    #---------------------------------------------
    elif args.directory:
        dir_path = args.directory
        valid, error = dir_parse(dir_path)
        valid_flights = valid
        erros = error

    #---------------------------------------------
    # -j: load an existing JSON
    #---------------------------------------------
    elif args.json:
        try:
            with open(args.json, 'r') as f:
                valid_flights = json.load(f)
        except FileNotFoundError:
            print (f"No JSON file found at {args.json}")
        errors = []
        #for i in valid_flights:
            #print (i)

    else:
        print("No input file or directory specified\n")
        return
    #---------------------------------------------
    # -o: write valid flights
    #---------------------------------------------
    if args.output:
        json_out_path = args.output
        with open(json_out_path, mode = 'w') as json_file:
            json.dump(valid, json_file, indent=2)

    #---------------------------------------------
    # -q: load and process queries
    #---------------------------------------------
   if args.query:
    try: 
        with open(args.query, 'r') as f:
            queries = json.load(f)
    except FileNotFoundError:
        print("No query file provided\n")
        return
    

    def normalize_queries(queries):
        if isinstance(queries, dict):  # single query → wrap into list
            return [queries]
        return queries  # already a list
        

    queries = normalize_queries(queries)

    # ----------------------------------------
    # Process Queries
    # ----------------------------------------

    def run_queries(valid_flights, queries):
        results = []

        for q in queries:
            # q is a dictionary of conditions, e.g.:
            # { "origin": "RIX" } or { "price": 200 }

            filtered = []

            for flight in valid_flights:
                match = True
                for key, value in q.items():
                    # If a flight doesn't have the field or doesn't match → skip
                    if key not in flight or flight[key] != value:
                        match = False
                        break
                if match:
                    filtered.append(flight)

            results.append({
                "query": q,
                "matches": filtered
            })

        return results
    

    # Run query filtering
    query_results = run_queries(valid_flights, queries)

    # Save to output JSON (default file name)
    output_file = "query_results.json"
    with open(output_file, 'w') as out:
        json.dump(query_results, out, indent=2)

    print(f"Query results written to {output_file}")
            


#call to main()    
if __name__ == "__main__":
    main()

