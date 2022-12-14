import asyncio
import logging
from typing import Any, Literal

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.exceptions import HTTP400BadRequestException, HTTP404NotFoundException
from app.db.crud.crud_basin import crud_basin
from app.db.crud.crud_job import crud_job
from app.db.session import get_db
from app.enums.job import Status
from app.schemas.basin import BasinCreate
from app.schemas.http_errors import (
    HTTP400BadRequestContent,
    HTTP400BadRequestResponse,
    HTTP401UnauthorizedContent,
)
from app.schemas.job import JobCreate, JobDbCreate, JobDbUpdate, JobRead

dev_router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)


class HTTP401DevContent(HTTP401UnauthorizedContent):
    code: str = "DEV_01"
    msg: str = "Not authenticated"


class HTTP400DevContent(HTTP400BadRequestContent):
    code: str = "DEV_02"
    msg: str = "Dev 02 error"
    data: dict[str, Any] = {"k1": "v1", "k2": "v2"}


@dev_router.post(
    "/dev1",
    response_model=str,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HTTP401UnauthorizedContent,
            "description": "Error raised when app is not authenticated",
        },
    },
    include_in_schema=settings.DEBUG,
)
async def dev1(db: AsyncSession = Depends(get_db)) -> str:
    """Dev 1 endpoint."""
    return f"Done!"


@dev_router.post(
    "/dev2",
    response_model=str,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": HTTP400DevContent,
            "description": "A bad request error is raised when...",
        },
    },
    include_in_schema=settings.DEBUG,
)
async def dev2(
    db: AsyncSession = Depends(get_db),
) -> str:
    """Dev 2 endpoint."""

    raise HTTP400BadRequestException(
        response=HTTP400BadRequestResponse(
            content=HTTP400DevContent(data={"k55": "v55"})
        )
    )


@dev_router.post(
    "/dev3",
    response_model=str,
    status_code=status.HTTP_200_OK,
    include_in_schema=settings.DEBUG,
)
async def dev3(
    a: Literal["ola"],
    db: AsyncSession = Depends(get_db),
) -> str:
    """Dev 3 endpoint."""
    logger.info(" ======== Dev3 =========")

    logger.info(" =======================")
    return "Done!"
