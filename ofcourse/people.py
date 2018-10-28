import phonenumbers
import datetime


class PersonError(Exception):
    pass


def normalize_person(person, name=None):
    "Check and normalize a person."

    if "birthdate" in person:
        if not isinstance(person["birthdate"], datetime.date):
            raise PersonError("birthdate {} is not a valid date.".format(**person))

    if "contact" in person:
        for t, vs in person["contact"].items():
            if t not in ("mobile", "phone", "email", "emergency"):
                raise PersonError(f"unknown contact type {t}")
            if isinstance(vs, str):
                is_single = True
                vs = [vs]
            elif isinstance(vs, list):
                is_single = False
                pass
            else:
                raise PersonError(f"contact items must be strings or lists of strings.")

            valid_vs = []
            for v in vs:
                if t == "email":
                    if "@" not in v:
                        raise PersonError(f"invalid e-mail {v}")
                    valid_vs.append(v)
                else:  # phonenumber
                    phone = phonenumbers.parse(v, "CH")
                    if not phonenumbers.is_valid_number(phone):
                        raise PersonError(f"invalid phone number {v}")
                    valid_vs.append(
                        phonenumbers.format_number(
                            phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL
                        )
                    )
            person["contact"][t] = valid_vs[0] if is_single else valid_vs

    return name, person
