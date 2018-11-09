from ofcourse import parsers
import io


def test_contacts_to_list():
    contacts = {"email": "a@b.cd", "mobile": ["0791234567", "0791234567"]}
    lst = parsers.contacts_to_list(contacts)
    assert len(lst) == 3
    assert lst[2].order == 1


def test_parse_people():
    s = """
Alice Alma:
  adress: Albertstrasse 8
  city: Bern
  plz: '3000'
  birthdate: 2001-04-07
  gender: f
  contact:
    mobile: +41 79 987 65 43
    email: aline.alma@abc.ch
    emergency:
    - +41 79 123 45 67
    - +41 79 123 23 44
    - +41 31 768 83 38

David Dünk:
    birthdate: 1999-04-10
    """

    person_list = parsers.person_list_parser(io.StringIO(s))
    assert person_list[0].first_name == "Alice"
