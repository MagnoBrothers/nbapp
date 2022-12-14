import logging
import uuid
from typing import Any, Dict, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.sql.expression import func, desc

from sqlmodel import delete

from app.db.crud import CRUDBase
from app.db.crud.crud_base import CRUDBase, ModelType
from app.schemas.basin import BasinDb
from app.schemas.job import JobDb, JobDbCreate, JobDbUpdate

logger = logging.getLogger(__name__)


class CRUDJob(CRUDBase[JobDb, JobDbCreate, JobDbUpdate]):
    async def create(
        self,
        db: AsyncSession,
        basin: BasinDb,
        obj_in: JobDbCreate,
        flush: bool = True,
        commit: bool = False,
    ) -> JobDb:
        job = JobDb(basin=basin, status=obj_in.status, progr=obj_in.progr)
        db.add(job)
        flush and await db.flush()
        commit and await db.commit()
        return job

    async def get_with_all_relationships(
        self, db: AsyncSession, id: uuid.UUID
    ) -> JobDb:
        stmt = (
            select(JobDb)
            .join(JobDb.basin)
            .options(joinedload(JobDb.basin, innerjoin=True))
        ).where(JobDb.id == id)

        result = await db.execute(stmt)
        job = result.scalar_one_or_none()
        return job

    async def get_multi_with_all_relationships_and_count(
        self, db: AsyncSession, skip: Optional[int] = 0, limit: Optional[int] = None
    ) -> tuple[list[JobDb], int]:
        stmt = (
            select(JobDb)
            .offset(skip)
            .join(JobDb.basin)
            .options(joinedload(JobDb.basin, innerjoin=True))
            .order_by(desc(JobDb.date))
        )
        if limit:
            stmt = stmt.limit(limit)

        total = await db.scalar(select(func.count(JobDb.id)))

        result = await db.execute(stmt)
        scalars = result.scalars()
        entries = scalars.all()
        return entries, total

    async def update_with_basin(
        self,
        db: AsyncSession,
        *,
        db_obj: JobDb,
        obj_in: Union[JobDbUpdate, Dict[str, Any]],
        basin: BasinDb,
        flush: bool = True,
        commit: bool = False
    ) -> ModelType:
        obj_data = db_obj.dict()
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj.basin = basin
        db.add(db_obj)
        flush and await db.flush()
        commit and await db.commit()
        return db_obj


crud_job = CRUDJob(JobDb)
