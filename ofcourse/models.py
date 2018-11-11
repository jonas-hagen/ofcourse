from dataclasses import dataclass
from dataclasses import field
import datetime
import typing
import phonenumbers


@dataclass
class Contact:
    channel: str
    address: str
    order: int = field(repr=False, default=0)

    def __post_init__(self):
        self.normalize()

    @property
    def is_phone(self):
        return self.channel in ("mobile", "phone", "emergency")

    @classmethod
    def _get_channel_order(cls):
        return ("mobile", "phone", "email", "emergency")

    @classmethod
    def key(cls, obj):
        return cls._get_channel_order().index(obj.channel), obj.order

    def normalize(self):
        if self.channel not in self._get_channel_order():
            raise ValueError("Unknown channel " + self.channel)
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
    country: str = field(default="CH")
    birthdate: datetime.date = field(default=None)
    gender: str = field(default="")
    contact: typing.List[Contact] = field(repr=False, default_factory=list)
    notes: typing.List[str] = field(repr=False, default_factory=list)

    def __post_init__(self):
        self.normalize()

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def identifier(self):
        return self.full_name.replace(" ", "_")

    @classmethod
    def key(cls, obj):
        return obj.full_name, obj.birthdate

    def normalize(self):
        if self.gender:
            if self.gender not in ("o", "f", "m"):
                raise ValueError("Unknown gender " + self.gender)
        if self.plz:
            if isinstance(self.plz, int):
                self.plz = str(self.plz)
            if "-" in self.plz:
                country, plz = self.plz.split("-")
                self.country = country
                self.plz = plz
            try:
                int(self.plz)
            except ValueError as e:
                raise ValueError("Invalid plz code " + self.plz)
        if self.notes:
            if not isinstance(self.notes, (tuple, list)):
                self.notes = [self.notes]


@dataclass
class Course:
    title: str
    first_date: datetime.date = field(default=None)
    last_date: datetime.date = field(default=None)
    number: int = field(repr=False, default=0)
    code: str = field(default="")
    notes: typing.List[str] = field(repr=False, default_factory=list)
    participants: typing.List[Person] = field(repr=False, default_factory=list)
    waitlist: typing.List[str] = field(repr=False, default_factory=list)
