"""Usage:
    arguments_example.py [-h]
    arguments_example.py [(-d NUMDAYS)]
    arguments_example.py [(-r DATE1 DATE2)]
#temp description.
Arguments:
  NUMDAYS        # number of previous days to include
  DATE1          # First date in a date range
  DATE2          # Second date in a date range
Options:
  -h --help
  -d --days      # Specify previous number of days
  -r --range     # Specify a date range
 """
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    print('--------------')
    #print(dir(arguments))
    print(arguments['Arguments:'])
    print(arguments.NUMDAYS)
    print(arguments.range)
