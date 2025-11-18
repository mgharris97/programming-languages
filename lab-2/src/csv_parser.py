# csv_parse.py
# Matthew Harris
# 241ADB166
# 11 November, 2025
# GitHub repo: https://github.com/mgharris97/programming-languages/tree/main/lab-2

import csv
from datetime import datetime
import os
import json


#CSV parse method
errors_list = []
valid_flights = []



def csv_parse(file_path):
    print(f"Opening file: {file_path}")
    with open(file_path, newline='', mode = 'r') as f:
        csv_file = csv.reader(f)
        for line_num, i in enumerate(csv_file, start=1):   

            if not i:
                continue 
            if i[0].startswith("#"):
                errors_list.append(f"Line {line_num}: {i[0]} → comment line, ignored for parsing")
                continue
            if len(i) != 6: 
                errors_list.append(f"Line {line_num}: {i} → invalid format")
                continue
            
            flight_id = i[0]
            origin = i[1]
            destination = i[2]
            departure = i[3]
            arrival = i[4]
            price = i[5] 

            #check each cell of a row one by one. If a cell is bad, print where it is bad and why
            if not (2 <= len(i[0]) <= 8 and i[0].isalnum):
                errors_list.append(f"Line {line_num}: {flight_id} → flight ID not 2-8 alphanumeric character")
                continue
            if not(origin.isupper() and len(origin) == 3 and origin.isalpha() and len(set(origin)) > 1):
                errors_list.append(f"Line {line_num}: {origin} → Invalid origin (not 3 uppercase, non-repeating letters)")
                continue
            if not(destination.isupper() and len(destination) == 3 and destination.isalpha() and len(set(destination)) > 1):
                errors_list.append(f"Line {line_num}: {destination} → Invalid destiantion (not 3 uppercase letters)")
                continue
            try:
                departure_time = datetime.strptime(departure, '%Y-%m-%d %H:%M')
                is_departure_date = True
            except ValueError:
                is_departure_date = False
            if not(is_departure_date):
                errors_list.append(f"Line {line_num}: {departure} → Invalid departure datetime")
                continue
            try:
                arrival_time = datetime.strptime(arrival, '%Y-%m-%d %H:%M')
                is_arrival_date = True
            except ValueError:
                is_arrival_date = False
            try:
                if not (is_arrival_date and (arrival_time > departure_time)):
                    errors_list.append(f"Line {line_num}: {arrival} → Arrival time occurs before departure → {departure}")
                    continue
            except ValueError:
                errors_list.append(f"Line {line_num}: {arrival} → Invalid arrival time")
                continue

            try:
                flight_price = float(price)
                if flight_price < 0:
                    errors_list.append(f"Line {line_num}: {price} → Price cannot be negative. Aint no one here paying you to fly w us")
                    continue
            except ValueError:
                errors_list.append(f"Line {line_num}: {price} → Price must be a valid float")
                continue
            #if all cells in a row (i) are good, then apped the row to the valid_flights list which is a list of dictionaries
            valid_flights.append({"flight_id": flight_id,
                                  "origin": origin,
                                  "destination": destination,
                                  "departure": departure,
                                  "arrival": arrival,
                                  "price": price
                                })
            
        return valid_flights, errors_list

    """ 
        with open("Errors.txt", mode='a') as error_file:
            error_file.write(f"--- Start of file [{os.path.basename(file_path)}] ---\n")
            for i in errors_list:
                error_file.write(i + "\n")
            error_file.write(f"--- End of file [{os.path.basename(file_path)}] ---\n\n")

        if
        with open("db.json", mode='w') as json_file:
            #json.dump(jobs_dictionary, f, indent=2)
            json.dump(valid_flights, json_file, indent=2)
    """



