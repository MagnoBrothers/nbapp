import logging
import uuid

from fastapi import APIRouter, Depends, status

from app.core.auth import oauth2_token_payload
from app.core.config import get_settings
from app.schemas.http_errors import HTTP401UnauthorizedContent, HTTP403ForbiddenContent
from app.schemas.job import JobCreate, JobRead, JobsRead
from app.services.job import JobService, get_job_service

job_router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)


@job_router.get(
    "/jobs",
    response_model=JobsRead,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HTTP401UnauthorizedContent,
            "description": "Not authenticated",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": HTTP403ForbiddenContent,
            "description": "Not enough privileges",
        },
    },
)
async def list_jobs(
    # auth_token_payload: TokenPayload = Depends(oauth2_token_payload),
    job_svc: JobService = Depends(get_job_service),
    skip: int = 0,
    limit: int = 10,
) -> JobsRead:
    """List jobs."""
    jobs_read = await job_svc.list_jobs(skip=skip, limit=limit)
    return jobs_read


@job_router.get(
    "/jobs/{job_id}",
    response_model=JobRead,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HTTP401UnauthorizedContent,
            "description": "Not authenticated",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": HTTP403ForbiddenContent,
            "description": "Not enough privileges",
        },
    },
)
async def retrieve_job(
    *,
    # auth_token_payload: TokenPayload = Depends(oauth2_token_payload),
    job_svc: JobService = Depends(get_job_service),
    job_id: uuid.UUID,
) -> JobsRead:
    """Retrieve job."""
    job_read = await job_svc.retrieve_job(job_id=job_id)
    return job_read


@job_router.post(
    "/jobs",
    status_code=status.HTTP_200_OK,
    response_model=JobRead,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HTTP401UnauthorizedContent,
            "description": "Not authenticated",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": HTTP403ForbiddenContent,
            "description": "Not enough privileges",
        },
    },
)
async def create_job(
    # auth_token_payload: TokenPayload = Depends(oauth2_token_payload),
    job_svc: JobService = Depends(get_job_service),
    *,
    job: JobCreate,
):
    """Creates job to generate basin image."""
    job_read = await job_svc.create_job(job=job)
    return job_read
