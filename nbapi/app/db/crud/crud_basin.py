import logging
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import delete

from app.db.crud import CRUDBase
from app.db.crud.crud_base import CRUDBase, ModelType
from app.schemas.basin import BasinDb, BasinDbCreate, BasinDbUpdate

logger = logging.getLogger(__name__)


class CRUDBasin(CRUDBase[BasinDb, BasinDbCreate, BasinDbUpdate]):
    ...


crud_basin = CRUDBasin(BasinDb)
