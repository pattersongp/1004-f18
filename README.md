# 1004-f18

Resources for running COMS W1004 @ Columbia

## Environment Setup
I would recommend using a virtualenv. Here are the installation intructions:

Most of these grading scripts are written in Python 3.

Be sure to install:
- Python 3
- pip

Once you have installed Python and Pip, you need to install the following libraries:

`pip3 install canvasapi`

`pip3 install pandas`

`pip3 install pytz`

## Descriptions for all three programs

### latehours.py
```
usage: latehours.py [-h] -a ASSN_ID -d DUE_DATE -r ROSTER_FILENAME [-p PUSH]
                    [-l LATE_ID]

Updates the late hours against the submission times of the provided assignment
id. Posts directly to CourseWorks after if argument -p is set

optional arguments:
  -h, --help            show this help message and exit
  -a ASSN_ID, --assignment ASSN_ID
                        Assignment id found on courseworks
  -d DUE_DATE, --due-date DUE_DATE
                        The date-time for due date: Y-m-d-H:M:S
  -r ROSTER_FILENAME, --roster ROSTER_FILENAME
                        The current roster downloaded from Courseworks
  -p PUSH, --push PUSH  Push update to courseworks
  -l LATE_ID, --late LATE_ID
                        Late Hours assignment ID
```
### assign_tas.py
```
usage: assign-tas.py [-h] -r STUDENT_ROSTER -t TA_ROSTER [-o OUTPUT]

Script for building the spread sheet for grading assignments

optional arguments:
  -h, --help            show this help message and exit
  -r STUDENT_ROSTER, --roster STUDENT_ROSTER
                        File downloaded from courseworks Grades tab
  -t TA_ROSTER, --ta-roster TA_ROSTER
                        csv file for with the list of TA's
  -o OUTPUT             optional output filename
```

#### Student Grades
You need to provide information on students in the class (for this section, we'll call this students.csv). To get this, login to Canvas, go to the class you're working with --> Grades --> Download Current Scores (.csv).

### postgrades.py
Script for posting grades to canvas through the Canvas API.
```
usage: postgrades.py [-h] -f GRADING_SHEET -a ASSN_ID -p PUSH_GRADE

Program for posting grades to Canvas using the Canvas API. The last command
line argument determines whether or not to push the grades to Canvas or do a
trial run to see what the output would be. Note that the COURSE_ID_SECTION1
global at the top is specific to the course that you're tryin to push grades
to.

optional arguments:
  -h, --help            show this help message and exit
  -f GRADING_SHEET, --file GRADING_SHEET
                        File with updated grades for postgrades.py to push to
                        Canvas
  -a ASSN_ID, --assn-id ASSN_ID
                        Assignment ID
  -p PUSH_GRADE, --push PUSH_GRADE
                        post to Canvas True/False
```
### Misc

#### `API_URL`
This should be the link you use to access Canvas.

An example is:
`https://CANVAS_LINK.com`

For projects at Columbia, at time of this README, the API_URL is `"https://courseworks2.columbia.edu"`

#### Canvas API Keys
To make your life easier, the grading script pulls submission times from Canvas and can automatically mark whether a given submission was late or not (it also takes into account a grace period that you can set). To do this though, you need to generate an API key for Canvas. To
generate an API token, login to [Canvas](http://www.courseworks2.columbia.edu), click on "Account" on the top left, go to "Settings", scroll down and click on "New Access Token". Use whatever configurations you want, generate a token and set `API_KEY` in the file to be that token.

#### `COURSE_ID` and `ASSIGNMENT_ID`
Along with the Canvas API Key, you need to specify the course id and assignment id that will be used. To find these values, go to the link for the specific assignment.

An example link looks like this:
`https://CANVAS_LINK/courses/COURSE_ID/assignments/ASSIGNMENT_ID`. Fill those variables in as appropriate.

The grading script is currently configured to support two sections. Modify the code as needed based on the number of sections you are handling.

For every `COURSE_ID` and `ASSIGNMENT_ID`, replace the values in the grading script with the appropriate values:

`COURSE_ID_SECTION1 = 'COURSE_ID' `

`ASSIGNMENT_ID_SECTION1 = 'ASSIGNMENT_ID'`

#### Deadlines and Time Zones
In order to tell if a submission is late, you need to provide the time the assigment was due. The format should be `%Y-%m-%d-%H:%M:%S`. An example of this is `2018-03-21-23:59:59`. In addition, by default Canvas runs in GMT. To make sure the assignment deadline you set above is in EST standard time, you need to also provide the hour time difference between the assignment deadline's timezone and GMT. You can find this time difference using a [Google search](https://www.google.com/search?q=time+difference+gmt+and+new+york&oq=time+difference+gmt+and+new+york&aqs=chrome..69i57j0l3.6111j0j9&sourceid=chrome&ie=UTF-8). It's normally 4 hours when it's daylight saving time and 5 when not. Set `GMT_EST_TIME_DIFFERENCE` to this value.

#### Grading Sheet Example
You'll need to download the grading sheet (in .xlsx format) to be able to push grades. For 3134 purposes, this is normally in a Google Drive folder. This repo also includes a template grading sheet that is in the format needed to use this grade push script.

Vaguely, the grades spreadsheet should look like this:

| Name        | ID           | UNI  | Late (TRUE/FALSE) | W1 (10) | ... | Comments | Total
| ------------- |:-------------:| -----:| ------:| ------:| ------:| --------:| ------
| Alexander Hamilton  | 812739 | ah1789 | FALSE  | 2  | ... | You must've worked non-stop! | 97
| Celie  | 783453 | ce1922 | TRUE | 5  | ... | Your code was too beautiful for words. | 100
| Pierre  |  289374 |  pb1812 | FALSE | 10 | ... | I liked the comet art! | 95
| . | . | . | . | . |.| .| .
| . | . | . | . | . |.| .| .
| . | . | . | . | . |.| .| .

