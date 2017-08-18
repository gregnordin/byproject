#!/Users/nordin/anaconda3/bin/python
"""
Print tasks organized by project for specified date(s).

usage: byproject.py [-h] [-f FILE] [-v]
                    [-p PREV | -d DAY | -m MONTH | -w WEEK | -r RANGE RANGE | -a]
                    [-i INCLUDE [INCLUDE ...] | -x EXCLUDE [EXCLUDE ...]]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Specify input file name (and path), FILE
  -v, --verbose         Print extra debug information
  -p PREV, --prev PREV  Number of days previous, PREV=N, to today to include
  -d DAY, --day DAY     Particular day, DAY=YYYY-MM-DD
  -m MONTH, --month MONTH
                        Specified month, MONTH=YYYY-MM
  -w WEEK, --week WEEK  Week starting from specified day, WEEK=YYYY-MM-DD
  -r RANGE RANGE, --range RANGE RANGE
                        Range of dates, RANGE=YYYY-MM-DD
  -a, --all             Process all days in file
  -i INCLUDE [INCLUDE ...], --include INCLUDE [INCLUDE ...]
                        Include specified projects
  -x EXCLUDE [EXCLUDE ...], --exclude EXCLUDE [EXCLUDE ...]
                        Exclude specified projects

Examples using the alias,

    alias bp='~/Documents/Projects/todo/byproject.py'

and byproject.py is executable (chmod +x byproject.py):

    # Show contents of todo.txt by project
    bp
    # Show items in todo.txt with project tags "proposals" and "whitepapers"
    bp -i proposals whitepapers
    # Show items in todo.txt except for those with project tag "personal" and "home"
    bp -x personal home
    # Show items for today in done.txt
    bp -p 0
    # Show items for last 3 days in done.txt
    bp -p 3
    # Show items for last week in temp.txt
    bp -p 7 -f temp.txt
    # Show items for last week in done.txt with project tag "make3dprinter"
    bp -p 7 -i make3dprinter
    # Show items for last week in temp.txt with project tag "make3dprinter"
    bp -p 7 -i make3dprinter -f temp.txt
    # Show items for last week in done.txt except for those with project tag "groceries"
    bp -p 7 -x groceries
    # Show all items in done.txt
    bp -a
    # Show items for specified day in done.txt
    bp -d YYYY-MM-DD
    # Show items for week starting on specified day in done.txt
    bp -w YYYY-MM-DD
    # Show items for month in done.txt
    bp -m YYYY-MM
    # Show items in specified date range in done.txt
    bp -r YYYY-MM-DD YYYY-MM-DD
    # Show items in specified date range in done.txt with project tag "make3dprinter"
    bp -r YYYY-MM-DD YYYY-MM-DD -i make3dprinter
"""

from colorama import Fore, Style
from datetime import datetime, timedelta
import argparse
import re
import os


def get_date_from_line(s):
    """
    Return the first date contained in input string 's'
    as a datetime.date object.
    """
    match = re.search(r'\d{4}-\d{2}-\d{2}', s)
    first_date = datetime.strptime(match.group(), '%Y-%m-%d').date()
    return first_date


def get_indices_for_start_and_end_dates(lines, startdate, enddate):
    """
    Return index of the first occurrence of startdate and index of
    the last occurrence of enddate in the list of strings, `lines`,
    which is assumed to be in chronological order.

    Arguments:
        lines - array of strings. Somewhere in each string is a date
                with format YYYY-MM-DD. Assume `lines` is sorted in
                ASCENDING date order (i.e., oldest date first and newest
                date last).
        startdate, enddate - datetime object for DATES (i.e., not date and time)

    Notes:
        In routine that calls this function, get all lines for desired range of
        dates with `some_list[index_start_date:index_end_date + 1]` except if
        `index_end_date = None`. In this case use
        `some_list[index_start_date:None]` or the equivalent
        `some_list[index_start_date:]`, which is a range that goes to the last
        element of the list
    """
    if startdate > enddate:
        raise RuntimeError("start date must be earlier than end date")
    index_start_date = -999
    index_end_date = -999
    for index, line in enumerate(lines):
        temp_date = get_date_from_line(line)
        if index_start_date == -999:
            if temp_date >= startdate:
                index_start_date = index
                if index == len(lines) - 1:
                    index_end_date = None
                else:
                    index_end_date = index
        else:
            if temp_date > enddate:
                index_end_date = index - 1
                break
            elif index == len(lines) - 1:
                index_end_date = None
    if index_start_date == -999:
        print('Desired date is later than last date in file. Aborting...')
        exit()
    if index_end_date == -999:
        raise ValueError("index_end_date has not been set")
    print('Start and end indices:', index_start_date, index_end_date)
    return index_start_date, index_end_date


def validate_date(date_text):
    try:
        return datetime.strptime(date_text, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")


def validate_month(date_text):
    try:
        return datetime.strptime(date_text, '%Y-%m').date()
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM")


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
indent1 = '    '
indent2 = '        '

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file",
                    type=str,
                    # type=argparse.FileType('r'),
                    help="Specify input file name (and path), FILE")
parser.add_argument("-v", "--verbose",
                    action="store_true",
                    help="Print extra debug information")
group_dates = parser.add_mutually_exclusive_group()
group_dates.add_argument("-p", "--prev",
                         type=int,
                         default=-1,
                         help="Number of days previous, PREV=N, to today to include")
group_dates.add_argument("-d", "--day",
                         type=str,
                         help="Particular day, DAY=YYYY-MM-DD")
group_dates.add_argument("-m", "--month",
                         type=str,
                         help="Specified month, MONTH=YYYY-MM")
group_dates.add_argument("-w", "--week",
                         type=str,
                         help="Week starting from specified day, WEEK=YYYY-MM-DD")
group_dates.add_argument("-r", "--range",
                         type=str,
                         nargs=2,
                         help="Range of dates, RANGE=YYYY-MM-DD")
group_dates.add_argument("-a", "--all",
                         action="store_true",
                         help="Process all days in file")
group_proj = parser.add_mutually_exclusive_group()
group_proj.add_argument("-i", "--include",
                        type=str,
                        nargs="+",
                        help="Include specified projects")
group_proj.add_argument("-x", "--exclude",
                        type=str,
                        nargs="+",
                        help="Exclude specified projects")
args = parser.parse_args()
if args.verbose:
    print("-v value:", args.verbose)
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
if args.file is not None:
    fname = args.file
elif args.prev >= 0 or args.month is not None or args.week is not None or \
        args.range is not None or args.day is not None or args.all:
    fname = os.path.join(os.path.sep, 'Users', 'nordin', 'Dropbox', 'todo', "done.txt")
else:
    fname = os.path.join(os.path.sep, 'Users', 'nordin', 'Dropbox', 'todo', "todo.txt")
print('')
print('====================================================')
print('File:', fname, ' ')

# Open file and read contents
with open(fname, 'r') as f:
    alllines = [x.strip() for x in f.readlines()]

# Determine starting and ending lines corresponding to desired date range
if args.all or os.path.basename(fname) == "todo.txt":
    startline = 0
    lastline = None  # when used in somelist[startline:lastline] it means somelist[startline:]
elif args.month is not None:
    startdate, enddate = get_month_start_end(args.month)
    startline, lastline = get_indices_for_start_and_end_dates(alllines, startdate, enddate)
    if args.verbose:
        print('-m', args.month, startdate, enddate, startline, lastline)
elif args.week is not None:
    startdate = get_date_from_line(args.week)
    enddate = startdate + + timedelta(days=6)
    startline, lastline = get_indices_for_start_and_end_dates(alllines, startdate, enddate)
    if args.verbose:
        print('-w', args.week, startdate, enddate, startline, lastline)
elif args.day is not None:
    startdate = get_date_from_line(args.day)
    enddate = startdate
    startline, lastline = get_indices_for_start_and_end_dates(alllines, startdate, enddate)
    if args.verbose:
        print('-d', args.range, startdate, enddate, startline, lastline)
elif args.range is not None:
    startdate = get_date_from_line(args.range[0])
    enddate = get_date_from_line(args.range[1])
    startline, lastline = get_indices_for_start_and_end_dates(alllines, startdate, enddate)
    if args.verbose:
        print('-r', args.range, startdate, enddate, startline, lastline)
elif args.prev is not None:
    enddate = datetime.now().date()
    startdate = enddate - timedelta(days=args.prev)
    startline, lastline = get_indices_for_start_and_end_dates(alllines, startdate, enddate)
    if args.verbose:
        print('-p', args.prev, startdate, enddate, startline, lastline)
else:  # if no date flag is set, use today's date
    enddate = datetime.now().date()
    startdate = enddate
    startline, lastline = get_indices_for_start_and_end_dates(alllines, startdate, enddate)
    if args.verbose:
        print('no date set', startdate, enddate, startline, lastline)

if args.all or os.path.basename(fname) == "todo.txt":
    print('Date Range: entire file')
else:
    print('Date Range:', startdate, 'to', enddate)

if args.verbose:
    print("start line and last line:", startline, lastline)
print('====================================================')

# Get lines within range of dates
if lastline is None:
    lines = alllines[startline:]
else:
    lines = alllines[startline:lastline + 1]
# print(lines)

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
    if args.include is not None:
        if project[1:] in args.include:
            add_line(project, jobs, line)
    elif args.exclude is not None:
        if project[1:] not in args.exclude:
            add_line(project, jobs, line)
    else:
        add_line(project, jobs, line)
    # if project not in jobs:
    #     jobs[project] = []
    # jobs[project].append(line)

# Sort and print items
for proj in sorted(jobs):
    # print('\n', indent1, proj, sep='')
    print(indent1, proj, sep='')
    for item in jobs[proj]:
        if ('(A)' in item):
            print(indent2, red.format(item))
        elif ('(B)' in item):
            print(indent2, blue.format(item))
        elif ('(C)' in item):
            print(indent2, green.format(item))
        else:
            print(indent2, item, sep='')
print('')
