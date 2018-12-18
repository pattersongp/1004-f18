```
➜ grading_setup $ l                                                                                                                             (1004-summer)
      __init__.py       assign_tas.py       make_roster.py       ta-roster.csv
➜ grading_setup $ cat ta-roster.csv                                                                                                             (1004-summer)
type,name,email
hta,Graham Patterson,gpp2109@columbia.edu
hta,Yuxuan Mei,ym2552@columbia.edu
ta,Anmolpreet Singh Kandola,a.kandola@columbia.edu
ta,Jess Bunnag,tb2663@columbia.edu
ta,Zachary Tyler Boughner,ztb2003@columbia.edu
ta,Sarah Xinyi Yuan,sxy2003@columbia.edu
ta,Nhu Doan,nhu.doan@columbia.edu
ta,Edward Hyunbin Yoo,hy2506@columbia.edu
ta,Dominique L Gordon,dlg2156@columbia.edu
ta,Mariya Grigorova Delyakova,mgd2140@columbia.edu
ta,Tim Vallancourt,t.vallancourt@columbia.edu
ta,Gitika Bose,gb2606@columbia.edu
ta,Jack Winkler,j.winkler@columbia.edu
ta,Yunchu He,yh3050@columbia.edu
ta,Kevin Mejia,kevin.mejia@columbia.edu
ta,Sharon Jin,sj2846@columbia.edu
ta,Christian James Kowalczyk,cjk2159@columbia.edu
ta,Nathalie Marie Hager,nathalie.hager@columbia.edu
ta,Ignacio Ramirez,ir2331@columbia.edu

➜ grading_setup $ python assign_tas.py --help                                                                                                   (1004-summer)
usage: assign-tas.py [-h] -r STUDENT_ROSTER -t TA_ROSTER [-o OUTPUT]

Script for building the spread sheet for grading assignments

optional arguments:
  -h, --help            show this help message and exit
  -r STUDENT_ROSTER, --roster STUDENT_ROSTER
                        File downloaded from courseworks Grades tab
  -t TA_ROSTER, --ta-roster TA_ROSTER
                        csv file for with the list of TA's
  -o OUTPUT             optional output filename
➜ grading_setup $ python assign_tas.py -r ~/Downloads/2018-09-12T0832_Grades-COMSW1004_001_2018_3_-_INTRO-COMPUT_SCI_PROG_IN_JAVA.csv -t ta-roster.csv -o problem-set-1-grades.csv
➜ grading_setup $ l                                                                                                                             (1004-summer)
      __init__.py       __pycache__/      assign_tas.py       make_roster.py       problem-set-1-grades.csv       ta-roster.csv
```
