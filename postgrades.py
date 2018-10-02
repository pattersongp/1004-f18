from canvasapi import Canvas
import argparse
import time
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import sys

# Canvas API URL
API_URL = "https://courseworks2.columbia.edu"

# Canvas API key
API_KEY = None # YOU MUST FILL THIS IN AS A STRING

COURSE_ID = "59635"
ASSIGNMENT_ID = None # Passed in as an argument
canvas = Canvas(API_URL, API_KEY)

""" Takes in an excel sheet of grades (go to the excel sheet, File -> Download as --> .xlsx) that
represents the grades and comments for a given homework and returns a dictionary with all the data.
Namely, name, uni, canvas id, section number, total score, and comments """
def process_grading_sheet(grades, push_grade):
    rows = grades.index
    column_headers = list(grades)
    late_index = column_headers.index("ta")

    # to show students grade for each question, grade columns need to be between
    # these two column names
    comment_index = column_headers.index("Comments")
    homework_questions_list = column_headers[late_index + 1: comment_index]

    course = canvas.get_course(COURSE_ID)
    assignment = course.get_assignment(ASSIGNMENT_ID)

    for i in rows:
        row_data = grades.iloc[[i]]
        name = grades['name'][i]
        canvas_id = grades['id'][i]
        total_score = grades['Total'][i]
        comments = grades['Comments'][i]
        ta = grades['ta'][i]
        if pd.isnull(comments):
            comments = "No comments from TAs."
        comments = "\n{}\n".format(comments)
        comment_message = make_comment(row_data, homework_questions_list, comments, ta)
        if push_grade:
            try:
                submission = assignment.get_submission(canvas_id)
                submission.edit(
                    comment={'text_comment': comment_message},
                    submission={'posted_grade': total_score})
                print("Pushed grade for " + name)
            except Exception as e:
                print(e)
                print("FAILED TO PUSH GRADE FOR " + name)
        else:
            print("NAME: " + name)
            print("CANVAS ID: " + str(canvas_id))
            print("TOTAL SCORE: " + str(total_score))
            print(comment_message)
            print("--------------------")

def make_comment(row_data, homework_questions, base_comment, ta):
    comment = base_comment + "\n"
    for homework_question in homework_questions:
        score = str(homework_question) + ": " + str(row_data[homework_question].values.flatten()[0])
        comment += score + " | "

    comment += "\n\nPlease direct all inquiries to [{}] who graded the assignment.".format(ta)
    comment += "\nAny errors in grading need to be resolved within 1 week of this posting."

    return comment

def _boolean_(string):
    if string not in {'False','True'}:
        raise ValueError('Not a valid boolean string')
    return string == 'True'

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="""
                                    Program for posting grades to Canvas using
                                    the Canvas API. The last command line argument
                                    determines whether or not to push the grades to
                                    Canvas or do a trial run to see what the output
                                    would be.

                                    Note that the COURSE_ID global at the
                                    top is specific to the course that you're tryin
                                    to push grades to.
                                    """, add_help=True, prog="postgrades.py")
    parse.add_argument("-f", "--file", required=True,
                       help="File with updated grades for postgrades.py to push to Canvas",
                       dest="grading_sheet")
    parse.add_argument("-a", "--assn-id", required=True, help="Assignment ID",
                       dest="assn_id")
    parse.add_argument("-p", "--push", default=False, type=_boolean_,
                       required=True, help="post to Canvas True/False",
                       dest="push_grade")
    args = vars(parse.parse_args())

    # check API Key and course ID
    if not API_KEY:
        sys.stderr.write("Error: Need API key from Courseworks.\n")
        sys.exit(-1)
    elif not COURSE_ID:
        sys.stderr.write("Error: Need course ID from Courseworks.\n")
        sys.exit(-1)

    # Setup paramaters
    ASSIGNMENT_ID = int(args["assn_id"])
    grading_sheet = args["grading_sheet"]
    push_grade = args["push_grade"]

    # process grading sheet and post grades to Courseworks
    process_grading_sheet(pd.read_excel(grading_sheet), push_grade)

    sys.stdout.write("Successfully pushed grades for {} to canvas\n".format(ASSIGNMENT_ID))

