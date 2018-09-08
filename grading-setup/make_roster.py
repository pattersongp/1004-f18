'''
    Written by Graham Patterson
    COMS W1004
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
def write_csv(filename, data):
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        for item in data:
            writer.writerow(item)

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="""
                                    Parses the student roster downloaded from
                                    courseworks under the Grades tab
                                    """, add_help=True, prog="make-roster.py")
    parse.add_argument("-r", "--roster", required=True, dest="student_roster",
                       help="File downloaded from courseworks Grades tab")
    args=vars(parse.parse_args())
    roster=parse_roster(args['student_roster'])
    if not roster:
        sys.stderr.write("Error {} does not exist\n".format(args['student_roster']))
        sys.exit(-1)
    write_csv("parsed-roster.csv", roster)
