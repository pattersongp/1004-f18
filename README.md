# 1004-Summer

Resources for running COMS W1004 @ Columbia

## Environment Setup
I would recommend using a virtualenv, but here are the installation intructions:

Most of these grading scripts are written in Python 3.

Be sure to install:
- Python 3
- pip

Once you have installed Python and Pip, you need to install the following libraries:

`pip3 install canvasapi`

`pip3 install pandas`

`pip3 install pytz`

## Descriptions for all three programs

### make_grading_sheet.py
```
usage: make_grading_sheet.py [-h] -f STUDENT_GRADES -a ASSN_ID -d DEADLINE
                             [--grace GRACE]

Builds the grading sheet for you, merging the students grades from courseworks
and checks whether they submitted their assignment on time or not.

arguments:
  -h, --help         show this help message and exit
  -f STUDENT_GRADES  Canvas grades csv file
  -a ASSN_ID         Assignment ID
  -d DEADLINE        Assignment deadline : Y-m-d-H:M:S
  --grace GRACE      Grace hours, defaults to 2
```

### codio_ontime_scraper.py
```
usage: codio_ontime_scraper.py [-h] -c CODIO_SHEET -p OUTPUT_CSV -d DEADLINE
                               [-o OPTIONAL_NAME]

Produces a file output.csv that will have the students' marked for an ontime
or late submission based on the csv file you downloaded from Codio website.

arguments:
  -h, --help            show this help message and exit
  -c CODIO_SHEET, --codio CODIO_SHEET
                        Codio csv downloaded from Codio module
  -p OUTPUT_CSV, --previous OUTPUT_CSV
                        output.csv from the previously ran
                        make_grading_sheet.py
  -d DEADLINE, --deadline DEADLINE
                        The deadline of the assignment as: Y-m-d-H:M:S
  -o OPTIONAL_NAME, --output OPTIONAL_NAME
                        name of the file created by this script
```

### postgrades.py
```
usage: postgrades.py [-h] -f GRADING_SHEET -a ASSN_ID -p PUSH_GRADE

Program for posting grades to Canvas using the Canvas API. The last command
line argument determines whether or not to push the grades to Canvas or do a
trial run to see what the output would be. Note that the COURSE_ID_SECTION1
global at the top is specific to the course that you're tryin to push grades
to.

arguments:
  -h, --help            show this help message and exit
  -f GRADING_SHEET, --file GRADING_SHEET
                        File with updated grades for postgrades.py to push to
                        Canvas
  -a ASSN_ID, --assn-id ASSN_ID
                        Assignment ID
  -p PUSH_GRADE, --push PUSH_GRADE
                        post to Canvas True/False
```

## Everything below here is informational
For running the scripts, please see the usage above.



## make_grading_sheet.py
This script allows you to create a grading sheet to be used by TAs to enter student score's for each part of the assignment. It will output a CSV file (output.csv) that includes 'Name', 'ID', 'UNI', 'Section', 'Late (TRUE/FALSE)'.

### What You Need

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

`COURSE_ID_SECTION2 = 'COURSE_ID'`

`ASSIGNMENT_ID_SECTION1 = 'ASSIGNMENT_ID'`

`ASSIGNMENT_ID_SECTION2 = 'ASSIGNMENT_ID'`

#### Deadlines and Time Zones
In order to tell if a submission is late, you need to provide the time the assigment was due. The format should be `%Y-%m-%d-%H:%M:%S`. An example of this is `2018-03-21-23:59:59`. In addition, by default Canvas runs in GMT. To make sure the assignment deadline you set above is in EST standard time, you need to also provide the hour time difference between the assignment deadline's timezone and GMT. You can find this time difference using a [Google search](https://www.google.com/search?q=time+difference+gmt+and+new+york&oq=time+difference+gmt+and+new+york&aqs=chrome..69i57j0l3.6111j0j9&sourceid=chrome&ie=UTF-8). It's normally 4 hours when it's daylight saving time and 5 when not. Set `GMT_EST_TIME_DIFFERENCE` to this value.

#### Setting Grace Period
In 3134, we tend to offer a grace period for students. This is to reduce the number of emails sent about having submitted an assignment a few minutes late. To handle this for your class, set `GRACE_PERIOD_HOURS` to the number of hours you want to consider within this grace period.

#### Student Data
You need to provide information on students in the class (for this section, we'll call this students.csv). To get this, login to Canvas, go to the class you're working with --> Grades --> Download Current Scores (.csv). If there is more than 1 section for the class, repeat this step and then merge the files manually (remembering to only include the header this file includes once (ie. remove it when merging in other student data from sections 2+).

### How to Run
An example for running this file is the following:

`python make_grading_sheet.py students.csv`

where...

`students.csv` is the file containing student data (see [Student Data](#student-data))

The output will be a CSV file (output.csv) that includes 'Name', 'ID', 'UNI', 'Section', 'Late (TRUE/FALSE)'.

## codio_ontime_scraper.py

### What You Need

#### Deadlines and Time Zones
See this [section](#deadlines-and-time-zones)

#### Setting Grace Period
See this [section](#setting-grace-period)

#### output.csv
You'll need to use the output.csv from `make_grading_sheet.py`.

#### Codio CSV
You'll need to download the CSV from Codio to know which students marked their assignments as completed and when they submitted their project. Login to your Codio teacher account, go to the Modules for the specific class you're working with and click 'Download CSV'

### CHANGE/DO NOT GRADE
The script will normally output TRUE/FALSE for the 'Late (TRUE/FALSE)' column. However, if the student failed to mark complete on the assignment, it will output 'DO NOT GRADE' since the person did not submit the assignment. In addition, if a student cannot be found on Codio (the script currently matches students based on name), it will output 'CHANGE'. You will need to update these cases to TRUE/FALSE before you are able to post grades.

### How to Run
An example for running this file is the following:

`python codio_ontime_scraper.py codio.csv output.csv result-output.csv`

where...

`codio.csv`: file containing Codio data (see [Codio data](#codio-csv))

`output.csv`: file containing output from previous section.

`result-output.csv`: enter name for output file. You can choose any name for the csv file that will be outputted here.

The output will be a csv file that includes 'Name', 'ID', 'UNI', 'Codio Username', 'Section', 'Late (TRUE/FALSE)'.

## postgrades.py

### What You Need

#### Previous Material
You need to use the same API_URL, API key, `COURSE_ID` and `ASSIGNMENT_ID` as discussed in 'make_grading_sheet.py' section.

#### Grading Sheet
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


### How to Run
An example for running this file is the following:

`python postgrades.py grading_sheet.xlsx False`

where...

`grading_sheet.xlsx`: file containing student data (see [Student Data](#student-data))

`boolean`: if True, pushes grades/comments to Canvas. if False, just prints outputs (always spot check some outputs before setting to True)

When you actually push to Canvas, you'll get a print statement telling whether a student's grade was successfully pushed.

## Finishing the Grading Sheet
Using the output created by **make_grading_sheet.py** or **codio_ontime_scraper.py**, you'll need to add the remaining columns and sheet formulas in an Excel-like program. For our grading cases, to finish making the grading sheet you should go on Google Sheets to make a new sheet and then paste the contents of output.csv into the new file. Then, you should make a column for every question being graded with a format of `W# (MAX_POINTS)` or `P# (MAX_POINTS)` depending on whether the question is for the written or programming sections of the homework. After finishing these, make the next columns 'Comments' and 'Total' respectively.

