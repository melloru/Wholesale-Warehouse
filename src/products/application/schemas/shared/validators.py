from typing import Annotated

from pydantic import BeforeValidator, Field


def convert_price_to_minor(value: int) -> int:
    pass


PriceMinor = Annotated[int, BeforeValidator(convert_price_to_minor), Field(gt=0)]
