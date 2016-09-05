#!/usr/bin/env python3.5
# See Rose Perrone's answer at
# http://stackoverflow.com/questions/2429511/why-do-people-write-usr-bin-env-python-on-the-first-line-of-a-python-script?rq=1

import sys
print('Is a TTY terminal?', sys.stdout.isatty())
print("Show terminal colors using escape codes\n")

colorred = "\033[01;31m{0}\033[00m"
colorgrn = "\033[1;32m{0}\033[00m"
coloryellow = "\033[1;33m{0}\033[00m"
colorblue = "\033[1;34m{0}\033[00m"
colormagenta = "\033[1;35m{0}\033[00m"
colorcyan = "\033[1;36m{0}\033[00m"

print(colorred.format("Warning! Reactor meltdown. Evacuate immediately!"))
print(colorgrn.format("Ha-ha, just kidding!"))
print(coloryellow.format("Test yellow. Test yellow. Test yellow. Test yellow."))
print(colorblue.format("Test blue. Test blue. Test blue. Test blue."))
print(colormagenta.format("Test magenta. Test magenta. Test magenta. Test magenta."))
print(colorcyan.format("Test cyan. Test cyan. Test cyan. Test cyan."))
