from collections import OrderedDict
from collections import defaultdict
from dataclasses import asdict
from dataclasses import fields
from ofcourse import models


def person_list_serializer(person_list):
    persons = OrderedDict()
    for p in sorted(person_list, key=models.Person.key):
        cs = contact_list_serializer(p.contact)
        ps = asdict(p, dict_factory=OrderedDict)
        ps["contact"] = cs
        persons[p.identifier] = ps
    return persons


def contact_list_serializer(contact_list):
    cs = defaultdict(list)
    for c in sorted(contact_list, key=models.Contact.key):
        cs[c.channel].append(c.address)
    cs = OrderedDict(
        sorted(
            cs.items(), key=lambda c: models.Contact._get_channel_order().index(c[0])
        )
    )
    return cs


def course_serializer(course):
    cs = asdict(course, dict_factory=OrderedDict)
    cs["participants"] = [p.identifier for p in course.participants]
    return cs
