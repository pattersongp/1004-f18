from canvasapi import Canvas
import argparse
import time
from datetime import datetime, timedelta
import csv
import pandas as pd
import sys

# Canvas API URL
API_URL = "https://courseworks2.columbia.edu"

# Canvas API key
API_KEY = "YOU MUST FILL THIS IN"
COURSE_ID_SECTION1 = "YOU MUST FILL THIS IN"
ASSIGNMENT_ID_SECTION1 = '00000'

#make sure to change this to timezone you need
GMT_EST_TIME_DIFFERENCE = 4

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

def get_submission_times(canvas, due_date, assn_id):

    result_dict = {}
    submitted_results = []
    course_section1 = canvas.get_course(COURSE_ID_SECTION1)

    # Makes API calls here:
    try:
        submissions_section1 = course_section1.get_assignment(assn_id).get_submissions()
    except canvasapi.exceptions.ResourceDoesNotExist as e:
        sys.stderr.write("Assignment ID wasn't found.\n {}".format(e))

    for submit_id in submissions_section1:
        submitted_results.append(submit_id)

    for submission in submitted_results:
        if submission.submitted_at is None:
            output = (submission.user_id, True)
            result_dict[str(submission.user_id)] = True
        else:
            if submission.late:
                cleaned_date = clean_date(submission.submitted_at)
                east_time = cleaned_date - timedelta(hours=GMT_EST_TIME_DIFFERENCE)

    # Deleted grace period check, because there is no grace period for this course
                output = (submission.user_id, False)
                result_dict[str(submission.user_id)] = False
            else:
                output = (submission.user_id, False)
                result_dict[str(submission.user_id)] = False
    return result_dict


def output_result(output_list, filename = "output.csv"):
    with open(filename,'w', newline='') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['Name', 'ID', 'UNI', 'Section', 'Late (TRUE/FALSE)'])
        for row in output_list:
            csv_out.writerow(row)

def clean_date(submit_time):
    submit_time = submit_time.replace('T', '-')
    submit_time = submit_time.replace('Z', '')
    return datetime.strptime(submit_time, "%Y-%m-%d-%H:%M:%S")

def past_grace_period_late(submit_time):
    return submit_time > due_date

def merge_data(student_grades, submission_dict):
    result = []
    count = 0
    for row in student_grades:
        #hacky way to skip first two rows of grades.csv file
        if count < 2:
            count +=1
            pass
        else:
            row = row.strip()
            row_list = row.split(",")
            name = str(row_list[1] + " " + row_list[0]).replace('"', '')
            canvas_id = str(row_list[2])
            uni = row_list[3]

            #this is hacky and assumes section looks like COMSW3134_001_2018_1 - DATA STRUCTURES IN JAVA
            #it pulls section by taking the 12th index value which should be the section
            try:
                section = row_list[4][12]
            except:
                section = ""

            if canvas_id in submission_dict.keys():
                output = (name, canvas_id, uni, section, submission_dict[row_list[2]])
            else:
                output = (name, canvas_id, uni, section, True)
                pass
            result.append(output)
            count+=1
        result.sort(key=lambda tup: tup[2])
    return result

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="""
                                    Builds the grading sheet for you, merging the
                                    students grades from courseworks and checks
                                    whether they submitted their assignment on
                                    time or not.
                                    """, add_help=True, prog="make_grading_sheet.py")
    parse.add_argument("-f", required=True, help="Canvas grades csv file", dest="student_grades")
    parse.add_argument("-a", required=True, help="Assignment ID", dest="assn_id")
    parse.add_argument("-d", required=True, help="Assignment deadline : Y-m-d-H:M:S", dest="deadline")
    parse.add_argument("--grace", default=2, help="Grace hours, defaults to 2", dest="grace")
    args = vars(parse.parse_args())

    deadline = assignment_deadline = datetime.strptime(args['deadline'], "%Y-%m-%d-%H:%M:%S")
    # change hours to whatever your classes grace period is
    due_date = deadline + timedelta(hours=int(args["grace"]))

    # make sure to change this to timezone you need
    GMT_EST_TIME_DIFFERENCE = 4

    # Initialize a new Canvas object
    canvas = Canvas(API_URL, API_KEY)

    #returns a dict where key is canvas id and value is boolean for whether assignment was late
    submission_dict = get_submission_times(canvas, args["deadline"], args["assn_id"])

    with open(args["student_grades"], "r") as f:
        # assumes you have an output.csv that came from making a written homework grading sheet
        output_result_list = merge_data(f, submission_dict, )
        output_result(output_result_list)

    sys.stdout.write("Successfully created grades sheet\n")

