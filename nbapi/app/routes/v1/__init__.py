from fastapi import APIRouter

from .auth import auth_router
from .dev import dev_router
from .tusd import image_router
from .job import job_router

router_v1 = APIRouter()
router_v1.include_router(auth_router, prefix="/auth", tags=["auth"])
router_v1.include_router(job_router, prefix="", tags=["job"])
router_v1.include_router(image_router, prefix="", tags=["image"])
router_v1.include_router(dev_router, prefix="/dev", tags=["dev"])
