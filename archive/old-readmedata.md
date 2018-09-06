

### codio_ontime_scraper.py
This script produces a file
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

#### output.csv
You'll need to use the output.csv from `make_grading_sheet.py`.

#### Codio CSV
You'll need to download the CSV from Codio to know which students marked their assignments as completed and when they submitted their project. Login to your Codio teacher account, go to the Modules for the specific class you're working with and click 'Download CSV'

## make_grading_sheet.py


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




### How to Run
An example for running this file is the following:

`python postgrades.py grading_sheet.xlsx False`

where...

`grading_sheet.xlsx`: file containing student data (see [Student Data](#student-data))

`boolean`: if True, pushes grades/comments to Canvas. if False, just prints outputs (always spot check some outputs before setting to True)

When you actually push to Canvas, you'll get a print statement telling whether a student's grade was successfully pushed.

## Finishing the Grading Sheet
Using the output created by **make_grading_sheet.py** or **codio_ontime_scraper.py**, you'll need to add the remaining columns and sheet formulas in an Excel-like program. For our grading cases, to finish making the grading sheet you should go on Google Sheets to make a new sheet and then paste the contents of output.csv into the new file. Then, you should make a column for every question being graded with a format of `W# (MAX_POINTS)` or `P# (MAX_POINTS)` depending on whether the question is for the written or programming sections of the homework. After finishing these, make the next columns 'Comments' and 'Total' respectively.

