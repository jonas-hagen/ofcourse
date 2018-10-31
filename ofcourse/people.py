import phonenumbers
from collections import OrderedDict
import datetime
from ruamel import yaml


class PersonError(Exception):
    pass


def dump(filename, people, use_omap=False):
    people = normalize_people(people)
    y = yaml.YAML()
    if not use_omap:
        y.representer.add_representer(
            OrderedDict, yaml.representer.RoundTripRepresenter.represent_dict)
    with open(filename, 'w') as f:
        y.dump(people, f)


def normalize_people(people):
    out = dict()
    for n, p in people.items():
        n, p = normalize_person(p, n)
        out[n] = p
    return OrderedDict(sorted(out.items()))


def normalize_person(person, name=None):
    "Check and normalize a person."

    fields = [
        'first_name', 'last_name', 'adress', 'city', 'plz', 'birthdate',
        'gender', 'contact', 'notes'
    ]
    for k in person:
        if k not in fields:
            raise PersonError(f'{name}: unknown field {k}')

    if 'first_name' in person and 'last_name' in person:
        if person['first_name'] + ' ' + person['last_name'] != name:
            raise PersonError("{}: inconsistent names".format(name))

    if "birthdate" in person:
        if not isinstance(person["birthdate"], datetime.date):
            raise PersonError("{}: birthdate {} is not a valid date.".format(
                name, person['birthdate']))

    if "contact" in person:
        c_fields = ("mobile", "phone", "email", "emergency")
        for t, vs in person["contact"].items():
            if t not in c_fields:
                raise PersonError(f"{name}: unknown contact type {t}")
            if isinstance(vs, str):
                is_single = True
                vs = [vs]
            elif isinstance(vs, list):
                is_single = False
                pass
            else:
                raise PersonError(
                    f"{name}: contact items must be strings or lists of strings."
                )

            valid_vs = []
            for v in vs:
                if t == "email":
                    if "@" not in v:
                        raise PersonError(f"{name}: invalid e-mail {v}")
                    valid_vs.append(v)
                else:  # phonenumber
                    phone = phonenumbers.parse(v, "CH")
                    if not phonenumbers.is_valid_number(phone):
                        raise PersonError(f"{name}: invalid phone number {v}")
                    valid_vs.append(
                        phonenumbers.format_number(
                            phone,
                            phonenumbers.PhoneNumberFormat.INTERNATIONAL))
            person["contact"][t] = valid_vs[0] if is_single else valid_vs
        person['contact'] = OrderedDict(
            sorted(
                person['contact'].items(),
                key=lambda it: c_fields.index(it[0])))

    if 'gender' in person:
        if person['gender'] not in ['m', 'f', 'o']:
            raise PersonError('unknown gender {gender}'.format(**person))

    # sorting
    person = OrderedDict(
        sorted(person.items(), key=lambda it: fields.index(it[0])))

    return name, person
