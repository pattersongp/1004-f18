import time
import argparse
from datetime import datetime, timedelta
import csv
import sys
from pytz import timezone

#write assignment due date following example form below
assignment_deadline = ""

#make sure to change this to timezone you need
GMT_EST_TIME_DIFFERENCE = 4

#set grace period
GRACE_PERIOD_HOURS = 2

#change hours to whatever your classes grace period is
due_date = ""


def is_late_codio(codio_file):
    #codio formats time like this: Thu Feb 08 2018 04:29:00 GMT+0000 (UTC)
    #that's really annoying because it gives time zone name twice (GMT and UTC)
    #so let's cut the utc part: Thu Feb 08 2018 04:29:00 GMT+0000
    output_dict = {}
    late_count = 0
    ontime_count = 0
    #handle reading in header
    reader = csv.reader(codio_file)
    headers = next(reader)
    name_index = headers.index("student name")
    username_index = headers.index("username")
    submit_time_index = headers.index("completed date")
    completed_index = headers.index("completed")

    for line  in codio_file:
        line = line.strip()
        line_list = line.split(",")
        name = line_list[name_index].lower()
        username = line_list[username_index]
        submit_time = line_list[submit_time_index][:-6]
        completed_check = line_list[completed_index]

        if completed_check == 'false':
            output_dict[name] = ['DO NOT GRADE', username]
            continue
        if not submit_time:
            output_dict[name] = [True, username]
            continue

        #more on formatting here: https://docs.python.org/3/library/datetime.html#available-types
        submit_datetime = datetime_new= datetime.strptime(submit_time, '%a %b %d %Y %H:%M:%S %Z%z')
        east_time = submit_datetime - timedelta(hours=GMT_EST_TIME_DIFFERENCE)
        isLate = past_grace_period_late(east_time)
        if isLate:
            late_count += 1
        else:
            ontime_count += 1
        output_dict[name] = [isLate, username]
    print("on-time " + str(ontime_count))
    print("late-time " + str(late_count))
    return output_dict

def past_grace_period_late(submit_time):
    #explicitly make due date at top of file into eastern time zone
    localtz = timezone('America/New_York')
    localize_due_date = localtz.localize(due_date)
    return submit_time  > localize_due_date

def merge_data(grading_sheet, isLate_dict):
    result = []
    reader = csv.reader(grading_sheet)
    headers = next(reader)

    """get index of necessary comments because grading sheet can have variable
    number of questions to grade"""
    name_index = headers.index("Name")
    id_index = headers.index("ID")
    uni_index = headers.index("UNI")
    section_index = headers.index("Section")

    for line in grading_sheet:
        line = line.strip()
        line_list = line.split(",")
        name = line_list[name_index]
        canvas_id = line_list[id_index]
        uni = line_list[uni_index]
        section = line_list[section_index]
        if name.lower() in isLate_dict.keys():
            isLate = isLate_dict[name.lower()][0]
            codio_username = isLate_dict[name.lower()][1]
            result.append((name, canvas_id, uni, codio_username, section, isLate))
        else:
            #could not find if user turned in a submission on Codio
            codio_username = "N/A"
            result.append((name, canvas_id, uni, codio_username, section, "CHANGE"))
    return result

def output_result(output_list, output_name):
    with open(output_name,'w') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['Name', 'ID', 'UNI', 'Codio Username', 'Section', 'Late (TRUE/FALSE)'])
        for row in output_list:
            csv_out.writerow(row)

def main(argv):
    #sample run of this
    #python codio_ontime_scraper.py COMS_W3134_Spring_2018_Homework_2_Programming.csv output.csv codio2-output.csv
    isLate_dict = is_late_codio(open(argv[1], 'r'))
    output_result_list = merge_data(open(argv[2], 'r'), isLate_dict)
    return output_result(output_result_list, argv[3])

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="""
                                    Produces a file output.csv that will have the
                                    students' marked for an ontime or late submission
                                    based on the csv file you downloaded from
                                    Codio website.
                                    """, add_help=True)

    parse.add_argument("-c", "--codio", required=True,
                       help="Codio csv downloaded from Codio module",
                       dest="codio_sheet")

    parse.add_argument("-p", "--previous", required=True,
                       help="output.csv from the previously ran make_grading_sheet.py",
                       dest="output_csv")

    parse.add_argument("-d", "--deadline", required=True,
                       help="The deadline of the assignment as: Y-m-d-H:M:S",
                       dest="deadline")

    parse.add_argument("-o", "--output", required=False, default="output.csv",
                       help="name of the file created by this script", dest="optional_name")

    args = vars(parse.parse_args())

    # Setup data for the script
    codio_file = open(args['codio_sheet'], 'r')
    to_be_merged = open(args['output_csv'], 'r')
    output_file = args['output_name']
    assignment_deadline = datetime.strptime(args['deadline'], "%Y-%m-%d-%H:%M:%S")
    due_date = assignment_deadline + timedelta(hours=GRACE_PERIOD_HOURS)

    # Script starts here
    isLate_dict = is_late_codio(codio_file)
    output_result_list = merge_data(to_be_merged, isLate_dict)
    output_result(output_result_list, output_file)

