#!/Users/nordin/anaconda3/bin/python

import sys


def hello(variable):
    print(variable)


data = sys.stdin.read()
# hello(data)

data = data.split('\n')

# f = open('/Users/nordin/Documents/Projects/todo/temp1.txt', 'w')

for line in data:
    line = line.strip()
    # f.write(line + '\n')
    if line.startswith('+'):
        line = "- " + line[1:]
        print(line)
    elif line.startswith('x'):
        line = "    - " + line[24:line.rfind('+')]
        print(line)

# f.close()
