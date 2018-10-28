import pytest
from ruamel import yaml
import datetime


@pytest.fixture(scope="module")
def named_person():
    p = {
        "adress": "Albertstrasse 8",
        "plz": "3000",
        "city": "Bern",
        "birthdate": datetime.date(2001, 4, 7),
        "gender": "f",
        "contact": {
            "mobile": "079987 65 43",
            "email": "aline.alma@abc.ch",
            "emergency": ["0791234567", "+41 79 123 23 44", "0041 31768 83 38"],
        },
    }
    return "Aline Alma", p


@pytest.fixture(scope="module")
def people():
    p = {
        "Aline Alma": {
            "adress": "Albertstrasse 8",
            "plz": "3000",
            "city": "Bern",
            "birthdate": datetime.date(2001, 4, 7),
            "contact": {
                "mobile": "079 987 65 43",
                "email": "aline.alma@abc.ch",
                "emergency": ["079 123 45 67"],
            },
        },
        "Basil Berger": {
            "adress": "Bühlstrasse 11",
            "plz": "3004",
            "city": "Bern",
            "birthdate": datetime.date(2004, 9, 7),
            "contact": {
                "mobile": "079 987 65 44",
                "email": ["basil@laber.ch", "hubert@laber.ch"],
                "emergency": ["079 123 45 67"],
            },
        },
    }
    return p


if __name__ == "__main__":
    p = people()
    y = yaml.YAML()
    with open("/tmp/people.yml", "w") as f:
        y.dump(p, f)
