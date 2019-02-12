from canvasapi import Canvas

import argparse, csv, json, sys

'''
    A command line program for posting grades to Courseworks through the Canvas
    API.
'''

API_URL = None          # Canvas API URL
API_KEY = None          # Your Canvas API key
COURSE_ID = None        # Course ID from Canvas
ASSIGNMENT_ID = None    # Assignment ID from Canvas
CANVAS = None           # Will be initialized in main()
PUSH_GRADE = False
TA_COMMENT = '''\n
Please direct all inquiries to {}, the TA who graded your assignment.
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
    PARSE.add_argument("-e", "--env", required=True,
                       help="JSON file that contains Canvas parameters",
                       dest="env_fname")
    PARSE.add_argument("-p", "--push", default=False, type=_boolean_,
                       required=True, help="post to Canvas True/False",
                       dest="push_grade")
    ARGS = vars(PARSE.parse_args())

    # Setup paramaters
    with open(ARGS["env_fname"], 'r') as f:
        data = json.loads(f.read())
    API_URL = data['api_url']
    API_KEY = data['api_key']
    COURSE_ID = data['course_id']
    ASSIGNMENT_ID = data['assn_id']
    to_post = ARGS["grading_sheet"]
    PUSH_GRADE = ARGS["push_grade"]

    # check API Key and course ID
    if not API_KEY:
        sys.stderr.write("Error: Need API key from Courseworks.\n")
        sys.exit(-1)
    elif not COURSE_ID:
        sys.stderr.write("Error: Need course ID from Courseworks.\n")
        sys.exit(-1)

    CANVAS = Canvas(API_URL, API_KEY)

    # process grading sheet and post grades to Courseworks
    process_grading_sheet(to_post)
    if PUSH_GRADE:
    	sys.stdout.write("Successfully pushed grades for {} to Canvas\n".format(ASSIGNMENT_ID))
