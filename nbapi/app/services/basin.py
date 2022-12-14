from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.base import BaseService


class BasinService(BaseService):
    def __init__(self, db: AsyncSession):
        super().__init__(db)


# Facade #############################


async def create_service(db: AsyncSession):
    basin_svc = BasinService(db)
    return basin_svc


# Injectable Dependencies ############


async def get_basin_service(db: AsyncSession = Depends(get_db)):
    basin_svc = await create_service(db)
    return basin_svc
