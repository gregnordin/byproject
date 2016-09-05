#!/usr/bin/env python3.5
# See Rose Perrone's answer at
# http://stackoverflow.com/questions/2429511/why-do-people-write-usr-bin-env-python-on-the-first-line-of-a-python-script?rq=1

# Purpose: try colorama package to print colored text to terminal
# Greg Nordin
# 8/14/16

import sys
from colorama import init, deinit, Fore, Back, Style

init()

print('Is a TTY terminal?', sys.stdout.isatty())
print("Show terminal colors colorama package\n")

print(Fore.RED + 'RED, Red, red, ...' + Style.RESET_ALL)
print(Fore.BLUE + 'BLUE, Blue, blue, ...' + Style.RESET_ALL)
print(Fore.GREEN + 'GREEN, Green, green, ...' + Style.RESET_ALL)
print(Fore.MAGENTA + 'MAGENTA, Magenta, magenta ...' + Style.RESET_ALL)
print(Fore.CYAN + 'CYAN, Cyan, cyan, ...' + Style.RESET_ALL)
print(Fore.YELLOW + 'YELLOW, Yellow, yellow, ...' + Style.RESET_ALL)

print('\nNow the light versions of these colors:')
print(Fore.LIGHTRED_EX + 'RED, Red, red, ...' + Style.RESET_ALL)
print(Fore.LIGHTBLUE_EX + 'BLUE, Blue, blue, ...' + Style.RESET_ALL)
print(Fore.LIGHTGREEN_EX + 'GREEN, Green, green, ...' + Style.RESET_ALL)
print(Fore.LIGHTMAGENTA_EX + 'MAGENTA, Magenta, magenta ...' + Style.RESET_ALL)
print(Fore.LIGHTGREEN_EX + 'GREEN, Green, green, ...' + Style.RESET_ALL)
print(Fore.LIGHTYELLOW_EX + 'YELLOW, Yellow, yellow, ...' + Style.RESET_ALL)

red = Fore.RED + '{0}' + Style.RESET_ALL
blue = Fore.BLUE + '{0}' + Style.RESET_ALL
green = Fore.GREEN + '{0}' + Style.RESET_ALL
magenta = Fore.MAGENTA + '{0}' + Style.RESET_ALL
cyan = Fore.CYAN + '{0}' + Style.RESET_ALL
yellow = Fore.YELLOW + '{0}' + Style.RESET_ALL

print(red.format("Warning! Reactor meltdown. Evacuate immediately!"))
print(blue.format("Warning! Reactor meltdown. Evacuate immediately!"))
print(green.format("Warning! Reactor meltdown. Evacuate immediately!"))
print(magenta.format("Warning! Reactor meltdown. Evacuate immediately!"))
print(cyan.format("Warning! Reactor meltdown. Evacuate immediately!"))
print(yellow.format("Warning! Reactor meltdown. Evacuate immediately!"))


deinit()
