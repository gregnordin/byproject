## byproject.py for todo.txt

### Purpose

Display `todo.txt` items by project instead of by date.

I discovered and began using [todo.txt](http://todotxt.com) in August 2016 to keep track of my to-do items in the context of various projects by tagging items with `+<projectname>`. My preferred method of interaction is the [todo.txt command line interface](https://github.com/ginatrapani/todo.txt-cli). I have found a number of [add-ons](https://github.com/ginatrapani/todo.txt-cli/wiki/Todo.sh-Add-on-Directory) to be useful, particularly [add](https://github.com/doegox/todo.txt-cli/blob/extras/todo.actions.d/add), [xp](https://github.com/gr0undzer0/xp), and [pri](https://github.com/tonipenya/todo.txt-cli/blob/addons/.todo.actions.d/pri). However, I often want to display items organized by project, and have not found an add-on that will do this. Hence this python script.

As a side note, Michael Descy's [Plaintext Productivity](http://plaintext-productivity.net/) has many useful ideas for text file-based personal organization and productivity.

### Installation

##### Requirements

- Python 3.x
    - I recommend installing [Anaconda](https://www.continuum.io/downloads) as the simplest, most hassle-free route to using python.
- Mac OS (Linux is probably fine too, but I haven't tested it)

##### Download

1. Download `byproject.py`. This is the only file you need. It uses the `colorama` package, which is included by default in the standard `Andaconda` install.
2. Copy `byproject.py` to any convenient directory in your file system.

##### Prepare `byproject.py` for use

1. Modify the shebang on line 1, `#!/usr/bin/env python3.5`, as needed to point to your python installation. It tells the operating system what to use to execute `byproject.py`. See answers to [this StackOverflow question](http://stackoverflow.com/questions/2429511/why-do-people-write-usr-bin-env-python-on-the-first-line-of-a-python-script) for an explanation.
2. Modify lines 233 and 235 to point to your `done.txt` and `todo.txt` files, respectively.
3. In Terminal, make the directory where you put `byproject.py` the current working directory and execute `chmod +x byproject.py`. This indicates to the operating system that `byproject.py` is a file that can be directly executed.

I find it convenient to define several aliases in my `.bash_profile`. Here is what I use:

    alias bp='~/Documents/Projects/todo/byproject.py'
    alias bpt='~/Documents/Projects/todo/byproject.py -p 0'  # Today's done items

### Usage

Given the first alias, executing `bp -h` prints the following help text:

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

### Examples

Show contents of `todo.txt` by project

    bp

Show items in `todo.txt` with project tags "proposals" and "whitepapers"

    bp -i projectname1 projectname2

Show items in `todo.txt` except for those with project tag "personal" and "home"

    bp -x projectname1 projectname2

Show items for today in `done.txt`

    bp -p 0

Show items for last 3 days in `done.txt`

    bp -p 3

Show items for last week in `temp.txt`

    bp -p 7 -f temp.txt

Show items for last week in `done.txt` with project tag "make3dprinter"

    bp -p 7 -i make3dprinter

Show items for last week in `temp.txt` with project tag "make3dprinter"

    bp -p 7 -i make3dprinter -f temp.txt

Show items for last week in `done.txt` except for those with project tag "groceries"

    bp -p 7 -x groceries

Show all items in `done.txt`

    bp -a

Show items for specified day in `done.txt`

    bp -d YYYY-MM-DD

Show items for week starting on specified day in `done.txt`

    bp -w YYYY-MM-DD

Show items for month in `done.txt`

    bp -m YYYY-MM

Show items in specified date range in `done.txt`

    bp -r YYYY-MM-DD YYYY-MM-DD

Show items in specified date range in `done.txt` with project tag "make3dprinter"

    bp -r YYYY-MM-DD YYYY-MM-DD -i make3dprinter

### Assumptions

I use only one project tag per todo item. `byproject.py` has been designed with this in mind.
