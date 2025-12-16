from typing import Annotated

from pydantic import StringConstraints


PUBLIC_NAME_PATTERN = r"^[a-zA-Z0-9_\-\.]+$"
PASSWORD_PATTERN = r"^[a-zA-Z0-9!@#$%^&*()_\-+=\[\]{}|\\:;\"'<>,.?/~`]+$"
NAME_PATTERN = r"^[a-zA-Zа-яА-ЯёЁ'\-\s]+$"
PHONE_PATTERN = r"^\+?[1-9]\d{1,14}$"

PublicNameStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=3,
        max_length=50,
        pattern=PUBLIC_NAME_PATTERN,
    ),
]

NameStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=2,
        max_length=100,
        pattern=NAME_PATTERN,
    ),
]

PasswordStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=8,
        max_length=128,
        pattern=PASSWORD_PATTERN,
    ),
]

PhoneStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        pattern=PHONE_PATTERN,
    ),
]