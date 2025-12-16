from typing import Annotated

from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer


async def get_access_token_or_401(
    token: Annotated[str | None, Depends(HTTPBearer(auto_error=False))],
) -> str:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No access token provided",
        )

    return token.credentials


CurrentToken = Annotated[str, Depends(get_access_token_or_401)]
