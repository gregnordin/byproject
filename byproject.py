#!/usr/bin/env python3.5
# See Rose Perrone's answer at
# http://stackoverflow.com/questions/2429511/why-do-people-write-usr-bin-env-python-on-the-first-line-of-a-python-script?rq=1

from colorama import init, deinit, Fore, Back, Style
from datetime import datetime, timedelta, date
import argparse
import re
import collections
import sys
import os

def get_date_from_line(s):
    """
    Return the first date contained in input string 's'
    as a datetime.date object.
    """
    match = re.search(r'\d{4}-\d{2}-\d{2}', s)
    date = datetime.strptime(match.group(), '%Y-%m-%d').date()
    return date

def get_start_and_end_dates_indices(lines, startdate, enddate):
    """
    Return index of the first occurrence of startdate and index of
    the last occurrence of enddate in the list of strings, `lines`.

    Arguments:
        lines - array of strings. Somewhere in each string is a date
                with format YYYY-MM-DD. Assume `lines` is sorted in
                ASCENDING date order (i.e., oldest date first and newest
                date last).
        startdate, enddate - datetime object for DATES (not both date and time)

    Notes:
        If the last occurrence of enddate is the last element of the list, return
        `index_end_date = None so` that in the routine that calls this function
        `some_list[index_start_date:index_end_date]` is
        `some_list[index_start_date:None]` which is the same as
        `some_list[index_start_date:]`, which is a range that goes to the last
        element of the list
    """
    if startdate > enddate:
        raise RuntimeError("start date is after end date")
    index_start_date = -999
    for index, line in enumerate(lines):
        temp_date = get_date_from_line(line)
        if index_start_date == -999:
            if temp_date >= startdate:
                index_start_date = index
                index_end_date = index
        else:
            if temp_date > enddate:
                index_end_date = index - 1
                break
            elif index == len(lines) - 1:
                index_end_date = None

    return index_start_date, index_end_date

def validate_date(date_text):
    try:
        return datetime.strptime(date_text, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

def validate_month(date_text):
    try:
        return datetime.strptime(date_text, '%Y-%m').date()
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM")

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)

def get_month_start_end(s):
    """
    Return first and last days as datetime.date objects
    in the month contained in input string 's' having
    the format (YYYY-MM).
    """
    # Check that string has the right format & get first day of month
    month_first_day = validate_month(s)
    # Get last day of the month
    month_last_day = last_day_of_month(month_first_day)
    return month_first_day, month_last_day

def add_line(project, jobs, line):
    """
    If `project` is not a key in the dict, `jobs`, create a new list
    in `jobs` with `project` as the key. Then append `line` to the list
    associated with the key `project` in `jobs`.
    """
    if project not in jobs:
        jobs[project] = []
    jobs[project].append(line)

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
                    help = "Specify input file name (and path), FILE")
group_dates = parser.add_mutually_exclusive_group()
group_dates.add_argument("-p", "--prev",
                    type = int,
                    default = -1,
                    help = "Number of days previous, PREV=N, to today to include")
group_dates.add_argument("-d", "--day",
                    type = str,
                    help = "Particular day, DAY=YYYY-MM-DD")
group_dates.add_argument("-m", "--month",
                    type = str,
                    help = "Specified month, MONTH=YYYY-MM")
group_dates.add_argument("-w", "--week",
                    type = str,
                    help = "Week starting from specified day, WEEK=YYYY-MM-DD")
group_dates.add_argument("-r", "--range",
                    type = str,
                    nargs = 2,
                    help = "Range of dates, RANGE=YYYY-MM-DD")
group_dates.add_argument("-a", "--all",
                    action="store_true",
                    help = "Process all days in file")
group_proj = parser.add_mutually_exclusive_group()
group_proj.add_argument("-i", "--include",
                    type = str,
                    nargs = "+",
                    help = "Include specified projects")
group_proj.add_argument("-x", "--exclude",
                    type = str,
                    nargs = "+",
                    help = "Exclude specified projects")
args = parser.parse_args()
print("-f value:", args.file)
print("-p value:", args.prev)
print("-d value:", args.day)
print("-m value:", args.month)
print("-w value:", args.week)
print("-r value:", args.range)
print("-a value:", args.all)
print("-i value:", args.include)
print("-x value:", args.exclude)

# Determine which input file to use
if args.file != None:
    fname = args.file
elif args.prev >= 0 or args.month != None or args.week != None or args.range != None or args.day != None or args.all != None:
    fname = os.path.join(os.path.sep, 'Users','nordin','Dropbox','todo',"done.txt")
else:
    fname = os.path.join(os.path.sep, 'Users','nordin','Dropbox','todo',"todo.txt")
print('filename:', fname)

# Open file and read contents
with open(fname, 'r') as f:
    alllines = [x.strip() for x in f.readlines()]

# Determine starting and ending lines corresponding to desired date range
if args.all or os.path.basename(fname) == "todo.txt":
    startline = 0
    lastline = None  # when used in somelist[startline:lastline] it means somelist[startline:]
elif args.month != None:
    startdate, enddate = get_month_start_end(args.month)
    startline, lastline = get_start_and_end_dates_indices(alllines, startdate, enddate)
    print('-m', args.month, startdate, enddate, startline, lastline)
elif args.week != None:
    startdate = get_date_from_line(args.week)
    enddate = startdate + + timedelta(days=6)
    startline, lastline = get_start_and_end_dates_indices(alllines, startdate, enddate)
    print('-w', args.week, startdate, enddate, startline, lastline)
elif args.day != None:
    startdate = get_date_from_line(args.day)
    enddate = startdate
    startline, lastline = get_start_and_end_dates_indices(alllines, startdate, enddate)
    print('-d', args.range, startdate, enddate, startline, lastline)
elif args.range != None:
    startdate = get_date_from_line(args.range[0])
    enddate = get_date_from_line(args.range[1])
    startline, lastline = get_start_and_end_dates_indices(alllines, startdate, enddate)
    print('-r', args.range, startdate, enddate, startline, lastline)
else: # This implements -p flag
    today = datetime.now().date()
    startdate = today - timedelta(days=args.prev)
    startline, lastline = get_start_and_end_dates_indices(alllines, startdate, today)
    print('-p', args.prev, startdate, today, startline, lastline)

print("start line and last line:", startline, lastline)
# Get lines within range of dates
lines = alllines[startline:lastline]
#print(lines)

# Collect items (lines) for each project and put in the dict `jobs`
jobs = {}
todo_items = []
split_line = re.compile('; |, |: |\s')
for line in lines:
    words = split_line.split(line)
    # Get first instance of a word that starts with '+'
    project = next(
              (word for word in words if word.startswith('+')),
              'no_assigned_project')
    if args.include != None:
        if project[1:] in args.include:
            add_line(project, jobs, line)
    elif args.exclude != None:
        if project[1:] not in args.exclude:
            add_line(project, jobs, line)
    else:
        add_line(project, jobs, line)
    # if project not in jobs:
    #     jobs[project] = []
    # jobs[project].append(line)

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
