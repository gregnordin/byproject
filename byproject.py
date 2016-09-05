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

def get_start_and_end_dates_indices(lines, startdate, enddate):
    """
    Return the index of the first occurrence of startdate and last
    occurrence of enddate in the array of strings, lines.

    Arguments:
        lines - array of strings. Somewhere in each string is a date
                with format YYYY-MM-DD
        startdate, enddate - datetime object for DATES (not date and time)
    """
    index_start_date = 0
    index_end_date = 0
    continue_search_start_date = True
    for index, line in enumerate(lines):
        temp_date = getdate(line)
        if temp_date == startdate and index_start_date == 0:
            index_start_date = index
        elif temp_date == enddate + timedelta(days=1) and index_end_date == 0:
            index_end_date = index
        elif index == len(lines)-1 and index_end_date == 0:
            index_end_date = -1
    return index_start_date, index_end_date

def get_month(s):
    """
    Return first and last days as datetime.date objects
    in the month contained in input string 's' having
    the format (YYYY-MM).
    """
    # Check that string has the right format

    # Get first day of the month (easy!)

    # Get last day of the month

    # Return first and last days
    
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
parser.add_argument("-f", "--file",
                    type=str,
                    #type=argparse.FileType('r'),
                    help = "specify input file")
group = parser.add_mutually_exclusive_group()
group.add_argument("-d", "--day",
                    type = int,
                    default = -1,
                    help = "number of days prior to today")
group.add_argument("-a", "--all",
                    action="store_true",
                    help = "process all days in file")
group.add_argument("-m", "--month",
                    type = str,
                    help = "number of days prior to today")
args = parser.parse_args()
print("-f value:", args.file)
print("-d value:", args.day)
print("-a value:", args.all)
print("-m value:", args.month)

# Determine which input file to use
if args.file != None:
    fname = args.file
elif args.day >= 0:
    fname = os.path.join(os.path.sep, 'Users','nordin','Dropbox','todo',"done.txt")
else:
    fname = os.path.join(os.path.sep, 'Users','nordin','Dropbox','todo',"todo.txt")
print('filename:', fname)

# Open file and read contents
with open(fname, 'r') as f:
    contents = f.read()

# Find startline according to date
if args.all or os.path.basename(fname) == "todo.txt":
    startline = 0
    lastline = -1
elif args.month != None:
    getdate(args.month)
else:
    # Get current date and starting date
    today = datetime.now().date()
    startdate = today - timedelta(days=args.day)
    startdate_string = startdate.strftime("%Y-%m-%d")
    print('Date range:', startdate, 'to', today)
    startline = contents.find(startdate_string) - 2
    lastline = -1
    #print(startline)
    #subset = contents[startline-2:]
    #lines = subset.splitlines()

print("start line and last line:", startline, lastline)
# Get lines within range of dates
lines = contents[startline:lastline].splitlines()
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
