import argparse, random, sys
from make_roster import parse_roster, read_csv, write_csv

'''
    Assigns the amount of students each TA will grade

    @param ta_list {list of dictionaries}
    @param roster {list of dictionaries}
'''
def distribute_students(ta_list, roster):
    random.shuffle(ta_list)
    expected = len(roster) // len(ta_list)
    leftovers = len(roster) % len(ta_list)

    # over distribute expected amount
    for ta in ta_list:
        ta['assigned'] = expected

    # Give half of HTA's students to TA's
    leftovers += expected
    if expected % 2 == 1:
        leftovers += 1
        expected  -= 1

    # reduce HTA's assigned students
    for ta in ta_list:
        if ta['type'] == 'hta':
            ta['assigned'] = expected // 2

    # Distribute leftovers to TA's
    while leftovers > 0:
        for ta in ta_list:
            if ta['type'] != 'hta' and leftovers > 0:
                ta['assigned'] += 1
                leftovers -= 1

    return ta_list

'''
    Assigns TA's to a specific student
    NOTE: this is where the shuffling occurs for TA's

    @param ta_list {list of dictionaries}
    @param roster {list of dictionaries}
'''
def assign_tas(ta_list, roster):
    current_student = 0
    for ta in ta_list:
        while ta['assigned'] > 0:
            try:
                roster[current_student]['ta'] = ta['name']
                current_student += 1
                ta['assigned'] -= 1
            except IndexError:
                sys.stderr.write("Error when assigning TA's:\nTA:{} Student Index{}\n"
                                 .format(ta, current_student))
    return roster

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="""
            Script for building the spread sheet for grading assignments
                                    """, add_help=True, prog="assign-tas.py")
    parse.add_argument("-r", "--roster", required=True, dest="student_roster",
                       help="File downloaded from courseworks Grades tab")
    parse.add_argument("-t", "--ta-roster", required=True, dest="ta_roster",
                       help="csv file for with the list of TA's")
    parse.add_argument("-o", dest="output", help="optional output filename")
    args=vars(parse.parse_args())

    roster=parse_roster(args['student_roster'])
    ta_roster=read_csv(args['ta_roster'])
    if not roster or not ta_roster:
        sys.stderr.write("Error either {} or {} does not exist\n"
                         .format(args['student_roster'],args['ta_roster']))
        sys.exit(-1)

    ta_list = distribute_students(ta_roster,roster)
    annotated_roster = assign_tas(ta_list, roster)

    filename = args['output'] if args['output'] else 'ta-assignments.csv'
    write_csv(filename, roster,
              fieldnames=list(annotated_roster[0].keys()) + ['Comments','Total'])

