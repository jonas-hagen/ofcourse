import pytest
from ofcourse import models


@pytest.mark.parametrize("kind", ["mobile", "phone", "emergency"])
def test_contact_phone(kind):
    c = models.Contact(kind, "0791234567")
    assert c.address == "+41 79 123 45 67"
