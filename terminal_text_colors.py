#!/usr/bin/env python3.5
# See Rose Perrone's answer at
# http://stackoverflow.com/questions/2429511/why-do-people-write-usr-bin-env-python-on-the-first-line-of-a-python-script?rq=1

import sys
import json
print("hello, json")
print(sys.stdout.isatty())
print ('\033[1;30mGray like Ghost\033[0;30m')
print ('\033[1;31mRed like Radish\033[0;30m')
print("\033[1;32;40m Bright Green\033[0;30;47m")
print('\033[30m') # and reset to default color
