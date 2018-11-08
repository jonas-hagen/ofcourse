#! /usr/bin/env python3
import click
from ofcourse import people
from ruamel import yaml
from tabulate import tabulate


@click.group()
def cli():
    pass


@cli.group("people")
def people_group():
    pass


@cli.group("course")
def course_group():
    pass


@people_group.command("normalize")
@click.argument("filename", default="./people.yml", type=click.Path(exists=True, dir_okay=False, writable=True))
def people_normalize(filename):
    y = yaml.YAML()
    with open(filename, 'r') as f:
        p = y.load(f)
    if p is None:
        exit()
    with open(filename, 'w') as f:
        people.dump(f, p)


@course_group.command("print")
@click.argument("filename", type=click.Path(exists=True, dir_okay=False))
@click.argument("people-file", default="./people.yml", type=click.Path(exists=True, dir_okay=False))
def course_print(filename, people_file):
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


if __name__ == '__main__':
    cli()
