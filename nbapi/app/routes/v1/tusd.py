import io
import logging
import json
from typing import Literal

import boto3
from fastapi import APIRouter, Depends, Request, Response, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import oauth2_token_payload
from app.core.config import get_settings
from app.db.crud.crud_job import crud_job
from app.db.session import get_db
from app.enums.job import Status
from app.schemas.http_errors import HTTP401UnauthorizedContent, HTTP403ForbiddenContent
from app.services.job import JobDbUpdate, JobService, get_job_service
from app.schemas.tusd import HookBody

image_router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)


@image_router.post(
    "/tusd-webhook-notification",
    status_code=status.HTTP_204_NO_CONTENT,
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
async def tusd_webhook_notification(
    request: Request,
    hook_body: HookBody,
    hook_name: Literal["post-finish"] = Header(),
    # auth_token_payload: TokenPayload = Depends(oauth2_token_payload),
    db: AsyncSession = Depends(get_db),
    job_svc: JobService = Depends(get_job_service),
):
    """Creates image upload notification."""
    job_id = hook_body.upload.metadata["job_id"]
    image_type = hook_body.upload.metadata["image_type"]
    key = hook_body.upload.storage.key

    prefix = "th_" if image_type == "thumbnail" else "main_"
    new_file_key = f"{prefix}{job_id}.png"
    bucket = settings.S3_BUCKET_NAME
    s3_url = f"http://{settings.S3_HOST}:{settings.S3_PORT}"
    s3_newfile_url = f"{s3_url}/{bucket}/{new_file_key}"

    s3 = boto3.resource(
        "s3",
        endpoint_url=s3_url,
        region_name=settings.S3_REGION,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
    )
    client = s3.meta.client

    # update the file json content with the correct file name
    s3_response_object = client.get_object(Bucket=bucket, Key=f"{key}.info")
    object_content = s3_response_object["Body"].read()
    info = json.loads(object_content)
    info["Storage"]["Key"] = new_file_key
    info["ID"] = new_file_key
    info_encoded = json.dumps(info).encode()

    # remove the old file .info
    s3.Object(bucket, f"{key}.info").delete()

    # create a new one with the new content pointing to the correct file name
    with io.BytesIO(info_encoded) as f:
        client.upload_fileobj(f, bucket, f"{new_file_key}.info")

    # rename the data file
    s3.Object(bucket, new_file_key).copy_from(CopySource=f"{bucket}/{key}")
    s3.Object(bucket, key).delete()

    job = await crud_job.get_with_all_relationships(db=db, id=job_id)
    basin = job.basin
    job_update = JobDbUpdate()
    if image_type == "thumbnail":
        basin.thumbnail_url = s3_newfile_url
    else:
        basin.image_url = s3_newfile_url
        job_update.progr = 100
        job_update.status = Status.DONE

    updated_job = await crud_job.update_with_basin(
        db=db, db_obj=job, obj_in=job_update, basin=basin, commit=True
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
