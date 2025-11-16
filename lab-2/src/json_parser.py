import json
import os

def json_parse(file): #JSON file from a file path
    print (f"Opening file {file}")
    with open(file, 'r') as f:
        data = json.load(f)

    print(type(data))
    print(data)




