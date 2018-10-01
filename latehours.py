from canvasapi.assignment import Assignment
from canvasapi.requester import Requester
from canvasapi import Canvas

from grading_setup import make_roster

from datetime import datetime, timedelta
import argparse, math, sys

# Canvas API URL and Key
API_URL = "https://courseworks2.columbia.edu"
API_KEY =  None
COURSE_ID = "59635" # YOU MUST FILL THIS IN
GMT_EST_TIME_DIFFERENCE = 4

'''
    Hits canvas API for submissions
        WARNING: list_submissions is deprecated and will need to change soon
'''
def fetch_submissions(assn_id):
    submissions = course.list_submissions(assn_id)
    return submissions

'''
    Finds the students with late submissions, then computes their hours
    left, returning a list of dictionaries to be updated on courseworks
'''
def compute_hours(submissions, due_date, curr_hours):
    late_submissions = list()
    for sub in submissions:
        if sub.late:

            # compute the hours lost
            cleaned_date = clean_date(sub.submitted_at)
            east_time = cleaned_date - timedelta(hours=GMT_EST_TIME_DIFFERENCE)
            due_date_stripped = datetime.strptime(due_date, "%Y-%m-%d-%H:%M:%S")
            difference = east_time - due_date_stripped
            hours_lost = int(math.ceil(abs(difference).total_seconds() / 3600.0))
            try:
                hours = curr_hours[sub.user_id] - hours_lost
                new_hours = max(hours, 0)

                if hours < 0:
                    print("Student [{}] used [{}] extra hours!".format(sub.user_id, hours))

                # store for updating later
                student = { 'id':sub.user_id, 'hours_left':new_hours }
                late_submissions.append(student)
            except KeyError:
                print("Unable to find current hours for: {}".format(sub.user_id))

    return late_submissions

'''
    Parses a submission date from Canvas
'''
def clean_date(submit_time):
    submit_time = submit_time.replace('T', '-')
    submit_time = submit_time.replace('Z', '')
    return datetime.strptime(submit_time, "%Y-%m-%d-%H:%M:%S")

'''
    Makes calls to Canvas API to update the grades
'''
def update_courseworks(course_obj, comment, late_subs, latehours_id):
    for item in late_subs:
        course_obj.update_submission(
            latehours_id,
            item['id'],
            comment = {'text_comment':comment},
            submission = {'posted_grade':item['hours_left']}
        )

'''
    Builds a dictionary of student id's and current late hours left
'''
def filter_roster(roster, latehours_id):
    to_return = dict()
    latehours_key = "Late Hours ({})".format(latehours_id)
    for item in roster:
        hours = int(float(item[latehours_key])) if item[latehours_key] else 170
        student_id = int(item["ID"])
        to_return[student_id] = hours
    return to_return


if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="""
            Updates the late hours against the submission times of the
            provided assignment id.

            Posts directly to CourseWorks after if argument -p is set
                                    """, add_help=True, prog="latehours.py")
    parse.add_argument("-a", "--assignment", required=True,
                       help="Assignment id found on courseworks",
                       type=int, dest="assn_id")
    parse.add_argument("-d", "--due-date", required=True,
                       help="The date-time for due date: Y-m-d-H:M:S",
                       dest="due_date")
    parse.add_argument("-r", "--roster", required=True,
                       help="The current roster downloaded from Courseworks",
                       dest="roster_filename")
    parse.add_argument("-p", "--push", help="Push update to courseworks",
                       type=bool, default=False, dest="push")
    parse.add_argument("-l", "--late", help="Late Hours assignment ID",
                       dest="late_id")
    args = vars(parse.parse_args())

    # check API Key and course ID
    if not API_KEY:
        sys.stderr.write("Error: Need API key from Courseworks.\n")
        sys.exit(-1)
    elif not COURSE_ID:
        sys.stderr.write("Error: Need course ID from Courseworks.\n")
        sys.exit(-1)

    # Setup paramaters
    assignment_id = args["assn_id"]
    latehours_id  = args["late_id"]
    rost_filename = args["roster_filename"]
    push          = args["push"]

    # Script starts here
    canvas = Canvas(API_URL, API_KEY)
    course = canvas.get_course(COURSE_ID)
    submissions = fetch_submissions(assignment_id)

    roster = make_roster.read_csv(rost_filename)
    # skip the first because its an extra line from CW
    curr_hours = filter_roster(roster[2:], latehours_id)
    late_subs  = compute_hours(submissions, args["due_date"], curr_hours)

    print("Planning to update:")
    for item in late_subs:
        print(item)

    # Only push to CourseWorks when ready
    if push:
        comment = "Deducting late hours for {}".format(assignment_id)
        update_courseworks(course, comment, late_subs, latehours_id)
        sys.stdout.write("Successfully updated latehours for assignment".format(assignment_id))

