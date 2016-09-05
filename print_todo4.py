#!/usr/bin/env python3.5
# See Rose Perrone's answer at
# http://stackoverflow.com/questions/2429511/why-do-people-write-usr-bin-env-python-on-the-first-line-of-a-python-script?rq=1

from colorama import init, deinit, Fore, Back, Style
from datetime import datetime, timedelta
import argparse
import re
import collections
import sys
import os

def getdate(s):
    """
    Return the first date contained in input string 's'
    as a string (YYYY-MM-DD) and as a datetime.date object.
    """
    match = re.search(r'\d{4}-\d{2}-\d{2}', s)
    date = datetime.strptime(match.group(), '%Y-%m-%d').date()
    return date.strftime("%Y-%m-%d"), date

# Define shortcuts for colored text printed to terminal
red = Fore.RED + '{0}' + Style.RESET_ALL
blue = Fore.BLUE + '{0}' + Style.RESET_ALL
green = Fore.GREEN + '{0}' + Style.RESET_ALL
magenta = Fore.MAGENTA + '{0}' + Style.RESET_ALL
cyan = Fore.CYAN + '{0}' + Style.RESET_ALL
yellow = Fore.YELLOW + '{0}' + Style.RESET_ALL

# Make shortcuts for formatting output
indent1 = '  '
indent2 = '      '

print('')

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--done",
                    type = int,
                    default = -1,
                    help = "use done.txt rather than todo.txt")
args = parser.parse_args()
print(args.done)

# Determine which input file to use
if args.done >= 0:
    inputfile = "done.txt"
else:
    inputfile = "todo.txt"
fname = os.path.join(os.path.sep, 'Users','nordin','Dropbox','todo',inputfile)
print(fname)

# Open file and read contents
f = open(fname, 'r')
contents = f.read()

# Find startline according to date
if inputfile == "done.txt":
    # Get current date and starting date
    today = datetime.now().date()
    startdate = today - timedelta(days=args.done)
    startdate_string = startdate.strftime("%Y-%m-%d")
    print('Date range:', startdate, 'to', today)
    startline = contents.find(startdate_string) - 2
    #print(startline)
    #subset = contents[startline-2:]
    #lines = subset.splitlines()
else:
    startline = 0
    #lines = contents.splitlines()

# Get lines within range of dates
lines = contents[startline:-1].splitlines()
#print(lines)

# Collect items by project
jobs = {}
todo_items = []
split_line = re.compile('; |, |: |\s')
for line in lines:
    words = split_line.split(line)
    # Get first instance of a word that starts with '+'
    project = next(
              (word for word in words if word.startswith('+')),
              'no_assigned_project')
    if project not in jobs:
        jobs[project] = []
    jobs[project].append(line)

# Sort and print items
for proj in sorted(jobs):
    print(indent1, proj)
    for item in jobs[proj]:
        if ('(A)' in item):
            print(indent2, red.format(item))
        elif ('(B)' in item):
            print(indent2, blue.format(item))
        elif ('(C)' in item):
            print(indent2, green.format(item))
        else:
            print(indent2, item)
print('')
