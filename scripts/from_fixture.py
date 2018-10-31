#! /usr/bin/env python3
import click
import json
from docopt import docopt
from ruamel import yaml
from collections import defaultdict
from ofcourse import people
from datetime import datetime
import sys


@click.command()
@click.argument('filename')
def get_people(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    persons = {el['pk']: el['fields'] for el in data if el['model'] == 'kumi.person'}
    contacts = {el['pk']: el['fields'] for el in data if el['model'] == 'kumi.kontakt'}
    c_map = {
        'e': 'email',
        'e2': 'email2',
        'N': 'emergency',
        'm': 'mobile',
        'p': 'phone',
    }
    ps = list()
    for pk, p in persons.items():
        name = p['vorname'] + ' ' + p['nachname']
        pn = dict()
        pn['first_name'] = p['vorname']
        pn['last_name'] = p['nachname']
        pn['adress'] = p['adresse']
        pn['plz'] = p['plz']
        pn['city'] = p['ort']
        pn['birthdate'] = datetime.strptime(p['geburtsdatum'], '%Y-%m-%d').date()
        if p['geschlecht']:
            pn['gender'] = p['geschlecht']
        if p['bemerkungen']:
            pn['notes'] = p['bemerkungen']

        c_data = [el for el in contacts.values() if el['person'] == pk]
        c = defaultdict(list)
        for k in c_data:
           c[c_map[k['kanal']]].append(k['adresse'])
        # keep secondary email at end
        c['email'] += c.get('email2', [])
        if not c['email']:
            del c['email']
        if 'email2' in c:
            del c['email2']
        pn['contact'] = c

        try:
            ps.append(people.normalize_person(pn, name))
        except people.PersonError as e:
            print('While at {} -> {}:'.format(pk, name), file=sys.stderr)
            print(pn, file=sys.stderr)
            print('  ' + str(e), file=sys.stderr)

    people.dump(sys.stdout, dict(ps))


if __name__ == '__main__':
    get_people()
