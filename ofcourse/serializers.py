from collections import OrderedDict
from dataclasses import asdict
from dataclasses import fields
from ofcourse import models


def person_list_serializer(person_list):
    pass


def contact_list_serializer(contact_list):
    contact_list = sorted(contact_list, key=models.Contact.key)
    return OrderedDict(((c.channel, c.address) for c in contact_list))


def course_serializer(course):
    pass
