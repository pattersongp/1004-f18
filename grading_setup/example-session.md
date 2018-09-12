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
➜ grading_setup $ head ~/Downloads/2018-09-12T0832_Grades-COMSW1004_001_2018_3_-_INTRO-COMPUT_SCI_PROG_IN_JAVA.csv                              (1004-summer)
Student,ID,SIS User ID,SIS Login ID,Section,Problem Set 1 (208548),Programming Project 1 (210268),Assignments Current Score,Assignments Unposted Current Score,Assignments Final Score,Assignments Unposted Final Score,Current Score,Unposted Current Score,Final Score,Unposted Final Score,Current Grade,Unposted Current Grade,Final Grade,Unposted Final Grade
    Points Possible,,,,,40.0,60.0,(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only),(read only)
"Abbamonte, Conor",366516,cma2214,cma2214,COMSW1004_001_2018_3 - INTRO-COMPUT SCI/PROG IN JAVA,,,,,0.0,0.0,,,,,,,,
"Adansi, Sena",342315,sa3523,sa3523,COMSW1004_001_2018_3 - INTRO-COMPUT SCI/PROG IN JAVA,,,,,0.0,0.0,,,,,,,,
"Ahani, Anastasia",388528,aa4277,aa4277,COMSW1004_001_2018_3 - INTRO-COMPUT SCI/PROG IN JAVA,,,,,0.0,0.0,,,,,,,,
"Alam, Shailha",390091,sa3657,sa3657,COMSW1004_001_2018_3 - INTRO-COMPUT SCI/PROG IN JAVA,,,,,0.0,0.0,,,,,,,,
"Alexander, Layla",336739,la2690,la2690,COMSW1004_001_2018_3 - INTRO-COMPUT SCI/PROG IN JAVA,,,,,0.0,0.0,,,,,,,,
"Aliev, Dee",399564,da2863,da2863,COMSW1004_001_2018_3 - INTRO-COMPUT SCI/PROG IN JAVA,,,,,0.0,0.0,,,,,,,,
"Amankwaa, Phillip",336976,poa2104,poa2104,COMSW1004_001_2018_3 - INTRO-COMPUT SCI/PROG IN JAVA,,,,,0.0,0.0,,,,,,,,
"Amirthan, Shawn",341134,saa2221,saa2221,COMSW1004_001_2018_3 - INTRO-COMPUT SCI/PROG IN JAVA,,,,,0.0,0.0,,,,,,,,
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
➜ grading_setup $ head problem-set-1-grades.csv                                                                                                 (1004-summer)
name,uni,id,ta,Comments,Total
"Abbamonte, Conor",cma2214,366516,Tim Vallancourt,,
"Adansi, Sena",sa3523,342315,Tim Vallancourt,,
"Ahani, Anastasia",aa4277,388528,Tim Vallancourt,,
"Alam, Shailha",sa3657,390091,Tim Vallancourt,,
"Alexander, Layla",la2690,336739,Tim Vallancourt,,
"Aliev, Dee",da2863,399564,Tim Vallancourt,,
"Amankwaa, Phillip",poa2104,336976,Tim Vallancourt,,
"Amirthan, Shawn",saa2221,341134,Tim Vallancourt,,
"Ardila, Ana",aa4278,388529,Tim Vallancourt,,
➜ grading_setup $ echo "Upload to Google drive now"                                                                                             (1004-summer)
Upload to Google drive now
➜ grading_setup $                                                                                                                               (1004-summer)
```
