from ofcourse import models
from ofcourse import serializers


def test_contact_list_serializer():
    c1 = models.Contact("emergency", "0774568293")
    c2 = models.Contact("mobile", "0791234567")
    c3 = models.Contact("email", "a@b.ef")

    d = serializers.contact_list_serializer([c1, c2, c3])

    assert tuple(d.keys()) == ("mobile", "email", "emergency")
    assert isinstance(d["mobile"], list)


def test_person_list_serializer():
    c1 = models.Contact("emergency", "0774568293")
    c2 = models.Contact("mobile", "0791234567")
    c3 = models.Contact("email", "a@b.ef")

    p1 = models.Person("Aline", "Alma", contact=[c1, c2, c3])
    p2 = models.Person("David", "Düber")

    d = serializers.person_list_serializer([p2, p1])

    d_vals = list(d.values())
    assert list(d.keys()) == ["Aline Alma", "David Düber"]
    assert d_vals[0]["first_name"] == "Aline"
    assert isinstance(d_vals[0]["contact"]["mobile"], list)
