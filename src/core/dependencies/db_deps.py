from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.db_helper import db_helper


DbSession = Annotated[AsyncSession, Depends(db_helper.get_session)]
