from canvasapi import Canvas
from canvasapi.assignment import Assignment
from canvasapi.requester import Requester
import argparse
import time
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import sys

# Canvas API URL and Key
API_URL = "https://courseworks2.columbia.edu"
API_KEY = "1396~IRD9JnuAmX2mush0297wIRxhGOqREhYkqntq2nSo4vkG0mzrLyRDIKq9O9X6O3E5"

COURSE_ID = "59635" # None # YOU MUST FILL THIS IN
assignment_id = '-1'
canvas = Canvas(API_URL, API_KEY)

def get_submissions(assn_id):
    course = canvas.get_course(COURSE_ID)
    submissions = course.list_submissions(assn_id)
    return submissions


def compute_hours(submissions):
    for sub in submissions:
        if sub.late:
            print("Is late: {}".format(sub))

def update_CourseWorks():
    pass

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="""
            Updates the late hours against the submission times of the
            provided assignment id.

            Posts directly to CourseWorks after if argument -p is set
                                    """, add_help=True, prog="latehours.py")
    parse.add_argument("-a", "--assignment", required=True,
                       help="Assignment id found on courseworks",
                       type=int, dest="assn_id")
    parse.add_argument("-p", "--push", help="Push update to courseworks",
                       default=False, dest="push")
    args = vars(parse.parse_args())

    print(args)

    # check API Key and course ID
    if not API_KEY:
        sys.stderr.write("Error: Need API key from Courseworks.\n")
        sys.exit(-1)
    elif not COURSE_ID:
        sys.stderr.write("Error: Need course ID from Courseworks.\n")
        sys.exit(-1)

    # Setup paramaters
    assignment_id = args["assn_id"]

    submissions = get_submissions(assignment_id)
    x = compute_hours(submissions)

    sys.stdout.write("Successfully updated latehours for assignment".format(assignment_id))

