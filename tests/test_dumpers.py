from ofcourse import dumpers
from ofcourse import models
from ofcourse import parsers
import io


def test_dump_person_list():
    c1 = models.Contact("emergency", "0774568293")
    c2 = models.Contact("mobile", "0791234567")
    c3 = models.Contact("email", "a@b.ef")

    p1 = models.Person("Aline", "Alma", contact=[c1, c2, c3])
    p2 = models.Person("David", "Düber")

    f = io.StringIO()
    dumpers.person_list_yaml_dumper(f, [p1, p2])
    f.seek(0)
    lst = parsers.person_list_parser(f)

    assert len(lst) == 2
