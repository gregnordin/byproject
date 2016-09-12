# Sunday, 2016-09-11

I need to implement the -i and -x flags (see below under Saturday, 2016-09-03). With these flags there are 3 possibilities:

1. Get all projects. This is currently what is implemented
2. Include only specified projects (-i flag)
3. Include all projects except specified projects (-x flag)

Item 1:

    if project not in jobs:
        jobs[project] = []
    jobs[project].append(line)

Item 2:

    if project in include_list:
        if project not in jobs:
            jobs[project] = []
        jobs[project].append(line)

Item 3:

    if project not in exclude_list:
        if project not in jobs:
            jobs[project] = []
        jobs[project].append(line)

So I need to make a function, `add_line` that does

    if project not in jobs:
        jobs[project] = []
    jobs[project].append(line)

and then I can structure the logic like this:

    if args.include != None:
        if project in args.include:
            add_line()
    elif args.exclude != None:
        if project not in args.exclude:
            add_line()
    else
        add_line()


# Saturday, 2016-09-03

Here is an alternate way of doing things:

    #----------------------------------------------------
    # Only one of these can be specified at a time
    #----------------------------------------------------
    # DONE: current items in todo.txt
    ./byproject.py
    # DONE: previous N days from today in done.txt
    ./byproject.py -p N
    # DONE: specific day in done.txt
    ./byproject.py -d 2016-08-21
    # DONE: all days in a week starting at specified date in done.txt
    ./byproject.py -w 2016-08-21
    # DONE: all days in a specified month in done.txt
    ./byproject.py -m 2016-08
    # DONE: all days in a specified date range in done.txt
    ./byproject.py -r 2016-08-07 2016-08-14
    # DONE: all days in done.txt
    ./byproject.py -a
    #----------------------------------------------------
    # These can be mixed with the above
    #----------------------------------------------------
    # DONE: Specify a different input file
    ./byproject.py -f filename
    # Create output in markdown format
    ./byproject.py --markdown
    # DONE: Include only the following projects
    ./byproject.py -i project1 project2 ...
    # DONE: Exclude the following projects
    ./byproject.py -x project1 project2 ...

Other items

- &#9989; Fix problem when specified date isn't present in file go to next nearest date after specified date.
- I also need to improve the visual formatting of the results (?)
- Perhaps change t xp 3 to show results by week, month, date range, etc. like above, as well as having the current behavior (?)
- Make the code a module too so can import it into other python scripts
- Check that done.txt is sorted by completion date (descending)

More ideas

- Heirarchy of todo files
    - todo.txt - immediate, today
    - soon.txt - needs done in the next days or week; review each morning
    - someday.txt - possibly do in the future
    - done.txt - finished items
    - notdone.txt - items that made it on the todo list but then were dropped off
- Only show todo's with priorities
- Have a secondary list?

### Final status today

I need to change `get_start_and_end_dates_indices(lines, startdate, enddate)` to handle corner cases

# Sunday, 2016-08-14

**<font color=red>Note: if the terminal window gets messed up, execute `tset` to reset it to default values</font>**

## Try curses for color output

### Resources

- [Python Curses - Johns Cool Things](https://www.ironalbatross.net/wiki/index.php?title=Python_Curses)
- [Curses Programming with Python - docs.python.org](https://docs.python.org/3/howto/curses.html#curses-howto)

### Conclusion

Curses is overkill for what I need. It wants you to clear the screen, write stuff to arbitrary positions on the screen, and when it's done clear the screen again. Go back to trying to use escape codes.

## Try escape codes with regular `print()` function - (use colorama)

### Resources

- [Print colored text in terminal](https://pythonadventures.wordpress.com/2011/03/16/print-colored-text-in-terminal/)
    - Nice shortcut by defining `colorred = "\033[01;31m{0}\033[00m"` and then using `print(colorred.format("Test red text..."))`
- [colorama](https://github.com/tartley/colorama) python package
    - Makes escape codes work on Windows as well as *nix OS's. Also provides shortcuts for escape codes (like `Fore.RED`).
    - This seems to be installed with anaconda python 3.5
- [blessings](https://github.com/erikrose/blessings) - A thin, practical wrapper around terminal capabilities in Python
    - I tried to conda install this package into anaconda python 3.5, but apparently there is some dependency conflict

### Conclusion

Use the colorama package since it is already installed with Anaconda. Make usage more concise with

    red = Fore.RED + '{0}' + Style.RESET_ALL
    print(red.format("This is red text."))

instead of

    print(Fore.RED + 'This is red text.' + Style.RESET_ALL)

## Be able to also use `done.txt` through command line arguments

Now I want to show the same sort of output except for `done.txt`, and I want to restrict how many days back results are shown.

Example usage:

    # Use todo.txt as default
    ./print_todo3.py
    # -d or --done for today through previous 3 days
    ./print_todo3.py -d 3
    # just today
    ./print_todo3.py -d 0

Ultimately, I would also like to do the following (which will require quite a bit of hacking with maybe a different solution than argparse):

    # all days in done.txt
    ./print_todo3.py -d all
    # all days in a specified month
    ./print_todo3.py -d 2016-08
    # all days in a specified date range
    ./print_todo3.py -d 2016-08-07 to 2016-08-14

After reading through the second resource below, I think it could be done like so:

    parser.add_argument('--done', '-d',
                        action='store_true',
                        help='use done.txt instead of todo.txt' )
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.done:
        filename = 'done.txt'
        # check if args.args is empty -> print only today
        # If it's a single integer include today back through that number of days
        # If it's a month date (2016-08), print that month
        # If it's a day date (2016-08-11), print that day
        # If it's two day dates (2016-08-14 and 2016-08-16), figure out
        #    which is the earlier and set it as the start date and the other
        #    as the end date and print between those dates

I could also add the capability to include only specified projects, or leave out specified projects.

### Resources

- [`docopt` - Command-line interface description language](http://docopt.org/) - <font color=red>Excellent!</font>
    - [`docopt` on github](https://github.com/docopt/docopt)
- [Python Argparse Cookbook](https://mkaz.tech/python-argparse-cookbook.html) - <font color=red>Excellent!</font>
- [Argparse Tutorial - docs.python.org](https://docs.python.org/3/howto/argparse.html)
- [argparse – Command line option and argument parsing; PyMOTW](https://pymotw.com/2/argparse/)

## How handle reading only certain dates in done.txt?

Can we assume that all of the items completed on a certain date are in a contiguous block, and that these blocks are consecutively date ordered? Yes, although it would probably be good to make a `sort_done.py` script to enforce this.

- How read first date in a line?
- How determine today's date?
- How compare dates?
- How specify a date range?

### Resources

- [Stack Overflow: Convert string into Date type on Python](http://stackoverflow.com/questions/9504356/convert-string-into-date-type-on-python)
- [Stack Overflow: Extracting date from a string in Python](http://stackoverflow.com/questions/3276180/extracting-date-from-a-string-in-python)

## Status

- `./print_todo4.py -d 5` will read all items from `done.txt` from 5 days ago to the present and print them organized by project
- `./print_todo4.py` will read all items from `todo.txt` and print them organized by project

# Saturday, 2016-08-13

## Objective

Make a `.py` file to develop a script to print todo.txt lines to the terminal in the following format:

- project1
    - item1 (earliest date)
    - item2 (next earliest date)
    - etc.
- project2
    - item1 (earliest date)
    - item2 (next earliest date)
    - etc.

If an item has a priority, don't change ordering, but do change its color [(Add Colour to Text in Python](http://ozzmaker.com/add-colour-to-text-in-python/), [Python colored output)](http://www.siafoo.net/snippet/88):

- \(A) = Red
- \(B) = Blue
- \(C) = Green
- anything else: lime green

Later, do the same for `done.txt` except specify optional argument specifying how many days back to include. Then be able to print from `done.txt` in the following format so I can look at what I got done on each day:

- date1
    - project1
        - item1
        - item2
        - etc.
    - project2
        - item1
        - item2
        - etc.
- date2
    - project1
        - item1
        - item2
        - etc.
    - project2
        - item1
        - item2
        - etc.

## Starting point

Stack Overflow question: [Sorting todo.txt lines by its properties](http://stackoverflow.com/questions/30501609/sorting-todo-txt-lines-by-its-properties)

## Make `.py` file executable

According to Rose Perrone's answer at [Stack Overflow (Why do people write #!/usr/bin/env python on the first line of a Python script?)](http://stackoverflow.com/questions/2429511/why-do-people-write-usr-bin-env-python-on-the-first-line-of-a-python-script?rq=1) put

    #!/usr/bin/env python3.5

as the first line in the script. Then at the command line execute

    chmod +x print_todo1.py

to make the file executable so it can be run as

    ./print_todo1.py

from the terminal (command line).
