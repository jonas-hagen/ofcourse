from dataclasses import dataclass
from dataclasses import field
import datetime
import typing
import phonenumbers


@dataclass
class Contact:
    channel: str
    address: str

    def __post_init__(self):
        self.normalize()

    @property
    def is_phone(self):
        return self.channel in ("mobile", "phone", "emergency")

    def normalize(self):
        if self.is_phone:
            phone = phonenumbers.parse(self.address, "CH")
            if not phonenumbers.is_valid_number(phone):
                raise ValueError("Invalid phone number " + self.address)
            self.address = phonenumbers.format_number(
                phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )


@dataclass
class Person:
    first_name: str
    last_name: str
    adress: str = field(repr=False, default="")
    city: str = field(default="")
    plz: str = field(repr=False, default="")
    birthdate: datetime.date = field(default=None)
    gender: str = field(default="")
    contact: typing.List[Contact] = field(repr=False, default_factory=list)
    notes: typing.List[str] = field(repr=False, default_factory=list)

    def __post_init__(self):
        self.normalize()

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def normalize(self):
        if self.gender:
            if self.gender not in ("o", "f", "m"):
                raise ValueError("Unknown gender " + self.gender)
        if self.plz:
            try:
                if "-" in self.plz:
                    int(self.plz.split("-")[1])
                else:
                    int(self.plz)
            except ValueError as e:
                raise ValueError("Invalid plz code " + self.plz)


@dataclass
class Course:
    title: str
    start: datetime.date = field(default=None)
    end: datetime.date = field(default=None)
    number: int = field(repr=False, default=0)
    code: str = field(default="")
    participants: typing.List[Person] = field(repr=False, default_factory=list)
