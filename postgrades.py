import argparse
import sys
import csv
from canvasapi import Canvas

'''
    A command line program for posting grades to Courseworks through the Canvas
    API.
'''

# Canvas API URL
API_URL = "https://courseworks2.columbia.edu"
API_KEY = None # Your Canvas API key goes here
COURSE_ID = None # Course ID from Canvas
ASSIGNMENT_ID = None # Passed in as an argument
PUSH_GRADE = False
CANVAS = Canvas(API_URL, API_KEY)
TA_COMMENT = '''\n
Please direct all inquiries to {}, who graded your assignment.
All requests need to be submitted within 1 week of this posting.'''

'''
    Posts a grade and comment to Courseworks for a given csv
'''
def process_grading_sheet(grading_sheet):
    course = CANVAS.get_course(COURSE_ID)
    assignment = course.get_assignment(ASSIGNMENT_ID)
    with open(grading_sheet, "r") as grades_file:
        reader = csv.DictReader(grades_file)

        for row in reader:
            grader = row['ta']
            grade = row['total']
            student = row['name']
            sid = row['id']
            comment = row['comments']
            comment += TA_COMMENT.format(grader)

            if PUSH_GRADE:
                try:
                    submission = assignment.get_submission(sid)
                    submission.edit(comment={'text_comment' : comment},
                                    submission={'posted_grade': grade})

                    print("Pushed grade for {}".format(student))
                except Exception as excp:
                    print(excp)
                    print("failed to push grade for " + student)
            else:
                print("name: {}".format(student))
                print("canvas id: {} ".format(sid))
                print("total score: {}".format(grade))
                print("notes: {}".format(comment))
                print("--------------------")

def _boolean_(string):
    if string not in {'False', 'True'}:
        raise ValueError('Not a valid boolean string')
    return string == 'True'

if __name__ == "__main__":
    PARSE = argparse.ArgumentParser(description="""
                                    Program for posting grades to Canvas using
                                    the Canvas API. The last command line argument
                                    determines whether or not to push the grades to
                                    Canvas or do a trial run to see what the output
                                    would be.

                                    Note that the COURSE_ID global at the
                                    top is specific to the course that you're tryin
                                    to push grades to.
                                    """, add_help=True, prog="postgrades.py")
    PARSE.add_argument("-f", "--file", required=True,
                       help="File with updated grades for postgrades.py to push to Canvas",
                       dest="grading_sheet")
    PARSE.add_argument("-a", "--assn-id", required=True, help="Assignment ID",
                       dest="assn_id")
    PARSE.add_argument("-p", "--push", default=False, type=_boolean_,
                       required=True, help="post to Canvas True/False",
                       dest="push_grade")
    ARGS = vars(PARSE.parse_args())

    # check API Key and course ID
    if not API_KEY:
        sys.stderr.write("Error: Need API key from Courseworks.\n")
        sys.exit(-1)
    elif not COURSE_ID:
        sys.stderr.write("Error: Need course ID from Courseworks.\n")
        sys.exit(-1)

    # Setup paramaters
    ASSIGNMENT_ID = int(ARGS["assn_id"])
    to_post = ARGS["grading_sheet"]
    PUSH_GRADE = ARGS["push_grade"]

    # process grading sheet and post grades to Courseworks
    process_grading_sheet(to_post)

    sys.stdout.write("Successfully pushed grades for {} to canvas\n".format(ASSIGNMENT_ID))
