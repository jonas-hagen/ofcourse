from ofcourse import models
from ofcourse import serializers


def test_contact_list_serializer():
    c1 = models.Contact("emergency", "0774568293")
    c2 = models.Contact("mobile", "0791234567")
    c3 = models.Contact("email", "a@b.ef")

    d = serializers.contact_list_serializer([c1, c2, c3])

    assert tuple(d.keys()) == ("mobile", "email", "emergency")
