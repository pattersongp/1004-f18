#!/usr/local/bin/python3

# Usage: cat a column of numbers into the program

import sys
from statistics import mean, median, stdev

data = [float(i.strip('\n')) for i in sys.stdin]
print('''Count: {0}
Mean: {1:.2f}
Low: {2}
High: {3}
Median: {4}
Stdev: {5:.2f}'''.format(len(data),
                     mean(data),
                     min(data),
                     max(data),
                     median(data),
                     stdev(data)))
