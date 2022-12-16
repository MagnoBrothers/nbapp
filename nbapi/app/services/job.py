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
from app.utils.basin_generator import BasinGenerator, BasinParams
from app.core.config import get_settings

settings = get_settings()


class JobService(BaseService):

    basin_svc: BasinService

    def __init__(self, db: AsyncSession, basin_svc: BasinService):
        super().__init__(db)
        self.basin_svc = basin_svc

    async def list_jobs(self, skip: int, limit: int) -> JobsRead:
        jobs, total = await crud_job.get_multi_with_all_relationships_and_count(
            db=self.db, skip=skip, limit=limit
        )
        jobs_read = JobsRead(total=total, data=[JobRead.parse_obj(job) for job in jobs])
        return jobs_read

    async def retrieve_job(self, job_id: uuid.UUID) -> JobRead:
        job = await crud_job.get_with_all_relationships(db=self.db, id=job_id)
        job_read = JobRead(**job.dict(), basin=job.basin)
        return job_read

    async def create_job(self, job: JobCreate):
        basin = await crud_basin.create(self.db, obj_in=job.basin.dict())
        new_job = await crud_job.create(
            self.db,
            basin=basin,
            obj_in=JobDbCreate(status=Status.PENDING, progr=0),
            commit=True,
        )
        job_read = JobRead.parse_obj(new_job)
        task_res = worker.create_job_task(job_id=new_job.id)
        # await self.create_job_task(job_id=job_read.id)
        return job_read

    async def create_job_task(self, job_id: uuid.UUID):
        job = await crud_job.get_with_all_relationships(db=self.db, id=job_id)
        if not job:
            raise ValueError(f"Unable to find job [{job_id=}]")

        thumbnail_params = BasinParams.parse_obj(job.basin)
        thumbnail_params.imw, thumbnail_params.imh = 128, 128
        thumbnail_basin_gen = BasinGenerator(params=thumbnail_params)
        for pct in thumbnail_basin_gen.pct_gen(step_threshold=100):
            ...

        url = (
            f"http://{settings.TUSD_HOST}:{settings.TUSD_PORT}{settings.TUSD_ENDPOINT}"
        )
        file = f"th_{job.id}.png"
        thumbnail_basin_gen.export_png(file=file)
        tusd_client = client.TusClient(url)
        uploader1 = tusd_client.async_uploader(
            file,
            chunk_size=settings.TUSD_UPLOAD_CHUNK,
            metadata={"job_id": str(job.id), "image_type": "thumbnail"},
        )
        await uploader1.upload()

        params = BasinParams.parse_obj(job.basin)
        basin_gen = BasinGenerator(params=params)
        for pct in basin_gen.pct_gen(step_threshold=10):
            status = Status.RUNNING if pct < 100 else Status.UPLOADING
            job_update = JobDbUpdate(progr=pct, status=status)
            updated_job = await crud_job.update(
                db=self.db, db_obj=job, obj_in=job_update, commit=True
            )

        file = f"im_{job.id}.png"
        basin_gen.export_png(file=file)
        tusd_client = client.TusClient(url)
        uploader2 = tusd_client.async_uploader(
            file,
            chunk_size=settings.TUSD_UPLOAD_CHUNK,
            metadata={"job_id": str(job.id), "image_type": "main"},
        )
        await uploader2.upload()


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
