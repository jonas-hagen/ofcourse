#! /usr/bin/env python3
"""
Manage a course.

Usage:
  ofc.py people normalize <file>
  ofc.py course print <course-file> [<people-file>]

"""
from docopt import docopt
from ofcourse import people
from ruamel import yaml
from tabulate import tabulate


def people_normalize(filename):
    y = yaml.YAML()
    with open(filename, 'r') as f:
        p = y.load(f)
    people.dump(filename, p)


def course_print(filename, people_file=None):
    people_file = people_file or 'people.yml'
    y = yaml.YAML()
    with open(filename, 'r') as f:
        c = y.load(f)
    with open(people_file, 'r') as f:
        ps = people.normalize_people(y.load(f))

    print(c['title'])
    print('='*len(c['title']))
    print()
    print('from {from} to {to}'.format(**c))
    print()

    simple_list = []
    for name in c['people']:
        p = ps[name]
        ice = p['contact']['emergency']
        ice = [ice] if isinstance(ice, str) else ice
        simple_list.append([name, str(p['birthdate'].year), ' / '.join(ice)])
    print(tabulate(simple_list, headers=['Name', 'Jg.', 'Notfallnummer']))


def main(args):
    if args['people']:
        if args['normalize']:
            people_normalize(args['<file>'])
    if args['course']:
        if args['print']:
            course_print(args['<course-file>'], args['<people-file>'])


if __name__ == '__main__':
    args = docopt(__doc__, version='OfCOurse 1.0')
    main(args)
