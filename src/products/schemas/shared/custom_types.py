from typing import Annotated

from pydantic import StringConstraints

from products.constants import ProductsFieldLength


NAME_PATTERN = r"^[a-zA-Zа-яА-ЯёЁ0-9\s\-_]+$"

NameStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        max_length=ProductsFieldLength.NAME,
        pattern=NAME_PATTERN,
    ),
]
