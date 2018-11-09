from dataclasses import dataclass
import phonenumbers


@dataclass
class Person:
    pass


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
                raise ValueError("invalid phone number " + self.address)
            self.address = phonenumbers.format_number(
                phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )


@dataclass
class Course:
    pass
