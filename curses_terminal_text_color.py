#!/usr/bin/env python3.5
# See Rose Perrone's answer at
# http://stackoverflow.com/questions/2429511/why-do-people-write-usr-bin-env-python-on-the-first-line-of-a-python-script?rq=1

import curses

# Start curses
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(True)

curses.addstr("Test string")

# Stop curses
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
# And return terminal to original settings
curses.endwin()
