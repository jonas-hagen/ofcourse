import pytest
from ofcourse import models
from dataclasses import asdict, fields
from collections import OrderedDict
import datetime


@pytest.mark.parametrize("kind", ["mobile", "phone", "emergency"])
def test_contact_phone(kind):
    c = models.Contact(kind, "0791234567")
    assert c.address == "+41 79 123 45 67"


def test_person():
    c = models.Contact("mobile", "0791234567")
    p = models.Person("Alice", "Alma", "Hüntzi 3", "Bern", "3007")
    p.contact.append(c)
    p.birthdate = datetime.date(2010, 1, 5)


def test_course():
    c = models.Course(title="Laber Blubber")
