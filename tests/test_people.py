from ofcourse import people


def test_normalize_person(named_person):
    name, person = named_person
    name, person = people.normalize_person(person, name)
    assert person["contact"]["mobile"] == "+41 79 987 65 43"
