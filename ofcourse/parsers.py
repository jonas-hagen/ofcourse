from ruamel import yaml
from ofcourse import models


def contacts_to_list(contacts):
    lst = list()
    for channel, adresses in contacts.items():
        if not isinstance(adresses, (list, tuple)):
            adresses = [adresses]
        for i, a in enumerate(adresses):
            lst.append(models.Contact(channel=channel, address=a, order=i))
    return lst


def person_list_parser(f):
    y = yaml.YAML()
    lst = list()
    for name, p_dict in y.load(f).items():
        if "contact" in p_dict:
            p_dict["contact"] = contacts_to_list(p_dict["contact"])
        if "first_name" not in p_dict:
            p_dict["first_name"] = name.split(" ")[0]
        if "last_name" not in p_dict:
            p_dict["last_name"] = name.split(" ")[-1]
        lst.append(models.Person(**p_dict))

    return lst


def course_parser(f, person_list):
    y = yaml.YAML()
    course_dict = y.load(f)
    person_dict = {p.full_name: p for p in person_list}
    course_dict["participants"] = [
        person_dict[name] for name in course_dict["participants"]
    ]
    course = models.Course(**course_dict)
    return course
