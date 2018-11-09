from ruamel import yaml
from collections import OrderedDict
from ofcourse import serializers
from ofcourse import models
from dataclasses import asdict
import functools
import tabulate


def person_list_yaml_dumper(f, person_list, use_omap=False):
    y = yaml.YAML()
    if not use_omap:
        y.representer.add_representer(
            OrderedDict, yaml.representer.RoundTripRepresenter.represent_dict
        )
    p_list = serializers.person_list_serializer(person_list)
    for name, person in p_list.items():
        y.dump({name: person}, f)
        print("", file=f)


def course_text_dumper(f, course):
    def write(s=''):
        print(s, file=f)

    write(course.title)
    write('='*len(course.title))
    write()
    write('from {first_date} to {last_date}'.format(**asdict(course)))
    write()

    simple_list = [ ]
    for p in course.participants:
        ice = [c.address for c in sorted(p.contact, key=models.Contact.key) if c.channel == 'emergency']
        year = str(p.birthdate.year) if p.birthdate else ''
        simple_list.append((p.full_name, year, ' / '.join(ice)))
    write(tabulate.tabulate(simple_list, headers=['Name', 'Jg.', 'Notfallnummer']))
