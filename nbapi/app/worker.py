import asyncio
import logging
import uuid
from functools import wraps

from huey import RedisHuey

import app.services.basin as basin_service
import app.services.job as job_service
from app.db.session import async_session_factory, engine

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.handlers = []


huey = RedisHuey("nbapi", immediate=False, host="redis")


def run_on_new_event_loop(aio_func):
    @wraps(aio_func)
    def wrapper_decorator(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ret = loop.run_until_complete(aio_func(*args, **kwargs))
        loop.close()

        return ret

    return wrapper_decorator


@huey.task()
@run_on_new_event_loop
async def create_job_task(job_id: uuid.UUID):
    print(f"Running create job task with id: {job_id}")
    async with async_session_factory() as session:
        basin_svc = await basin_service.create_service(session)
        job_svc = await job_service.create_service(db=session, basin_svc=basin_svc)
        await job_svc.create_job_task(job_id=job_id)

    # await engine.dispose()
