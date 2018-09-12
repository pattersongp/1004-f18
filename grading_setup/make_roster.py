'''
    Written by Graham Patterson
    COMS W1004

    Helper functions for assign_tas.py
'''
import argparse, csv, sys


'''
    Function for parsing the student roster from the Grades tab on courseworks
    returns a list of dictionaries, or False on failure
'''
def parse_roster(filename):
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            data = list()
            for row in reader:
                to_add = {
                          'name':row['Student'].strip('"'),
                          'uni':row['SIS User ID'],
                          'id':row['ID']
                          }
                if to_add['id']:
                    data.append(to_add)
            return data
    except OSError:
        return False

'''
    General function for reading a csv file and returning a list of dictionaries
'''
def read_csv(filename):
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            data = list()
            for row in reader:
                data.append(row)
            return data
    except OSError:
        return False

'''
    General function for writing a list of dictionaries to csv
'''
def write_csv(filename, data, fieldnames=None):
    if not fieldnames:
        fieldnames=data[0].keys()
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

