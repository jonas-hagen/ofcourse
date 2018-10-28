#! /usr/bin/env python3
"""
Manage a course.

Usage:
  ofc.py people normalize <file>

"""
from docopt import docopt
from ofcourse import people
from ruamel import yaml


def people_normalize(filename):
    y = yaml.YAML()
    with open(filename, 'r') as f:
        p = y.load(f)
    people.dump(filename, p)


def main(args):
    if args['people']:
        if args['normalize']:
            people_normalize(args['<file>'])


if __name__ == '__main__':
    args = docopt(__doc__, version='OfCOurse 1.0')
    main(args)
