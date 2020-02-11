#!/usr/bin/python

import csv
import sys

reader = csv.reader(sys.stdin)
for row in reader:
	if row[1] != "0":
		if row[98] != "":
			print row[0], row[98]

