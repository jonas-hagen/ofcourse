import pytest
from ofcourse import models


@pytest.mark.parametrize("kind", ["mobile", "phone", "emergency"])
def test_contact_phone(kind):
    c = models.Contact(kind, "0791234567")
    assert c.address == "+41 79 123 45 67"


def test_person():
    p = models.Person("Alice", "Alma", "Hüntzi 3", "Bern", "3007")


def test_course():
    c = models.Course(title='Laber Blubber')
