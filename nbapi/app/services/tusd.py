import uuid
from datetime import datetime

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from tusclient import client

from app import worker
from app.db.crud.crud_basin import crud_basin
from app.db.crud.crud_job import crud_job
from app.db.session import get_db
from app.enums.job import Status
from app.schemas.job import JobCreate, JobDbCreate, JobDbUpdate, JobRead, JobsRead
from app.services.base import BaseService
from app.services.basin import BasinService, get_basin_service
from app.services.job import JobService
from app.utils.basin_generator import BasinGenerator, BasinParams


class TusdService(BaseService):
    def __init__(self, db: AsyncSession, basin_svc: BasinService):
        super().__init__(db)
        self.basin_svc = basin_svc


# Facade #############################


async def create_service(db: AsyncSession, basin_svc: BasinService):
    job_svc = JobService(db=db, basin_svc=basin_svc)
    return job_svc


# Injectable Dependencies ############


async def get_job_service(
    db: AsyncSession = Depends(get_db),
    basin_svc: BasinService = Depends(get_basin_service),
):
    job_svc = await create_service(db=db, basin_svc=basin_svc)
    return job_svc
