from typing import Annotated

from fastapi.params import Depends

from core.factories.helper_factory import helper_factory
from auth.helpers import TokenHelper


def get_token_helper() -> TokenHelper:
    return helper_factory.get_token_helper()


TokenHelperDep = Annotated[TokenHelper, Depends(get_token_helper)]
